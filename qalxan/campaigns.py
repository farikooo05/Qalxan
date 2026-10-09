"""Group scam messages into campaigns: shared infrastructure (domain/phone) or near-identical wording."""
import itertools
import time

SIM_THRESHOLD = 0.45
MAX_MEMBERS = 40


class CampaignTracker:
    def __init__(self, vectorize):
        self.vectorize = vectorize
        self.campaigns: dict[int, dict] = {}
        self._ids = itertools.count(1)

    def _match(self, result, vec):
        domains, phones = set(result["domains"]), set(result["phones"])
        for c in self.campaigns.values():
            if domains & c["domains"] or phones & c["phones"]:
                return c
        for c in self.campaigns.values():
            # same impersonated brand within 10 minutes = same wave, even with rotated domains
            if result["brand"] and c["brand"] == result["brand"] and time.time() - c["last_seen"] < 600:
                return c
            # brandless schemes ("mom, new number"): same scheme within 10 minutes = same wave
            if not result["brand"] and not c["brand"] and c["scam_type"] == result["scam_type"] \
                    and time.time() - c["last_seen"] < 600:
                return c
        best, best_sim = None, 0.0
        for c in self.campaigns.values():
            sim = max((float((vec @ m.T).toarray()[0, 0]) for m in c["_vectors"]), default=0.0)
            if c["scam_type"] == result["scam_type"]:
                sim += 0.1  # same scheme: slightly easier to join
            if sim > best_sim:
                best, best_sim = c, sim
        return best if best_sim >= SIM_THRESHOLD else None

    def add(self, result: dict) -> dict | None:
        """Attach a scam result to a campaign (creating one if needed). Returns the campaign."""
        if result["verdict"] != "scam":
            return None
        vec = self.vectorize(result["text"])
        now = time.time()
        c = self._match(result, vec)
        if c is None:
            cid = next(self._ids)
            c = {"id": cid, "scam_type": result["scam_type"], "brand": result["brand"], "domains": set(),
                 "hosts": set(), "phones": set(), "count": 0, "keyword_hits": 0, "first_seen": now, "last_seen": now,
                 "status": "active", "warned": 0, "samples": [], "timeline": [], "_vectors": [], "_types": {}}
            self.campaigns[cid] = c
        c["_types"][result["scam_type"]] = c["_types"].get(result["scam_type"], 0) + 1
        c["scam_type"] = max(c["_types"], key=c["_types"].get)
        c["domains"] |= set(result["domains"])
        c["hosts"] |= set(result.get("hosts", []))
        c["phones"] |= set(result["phones"])
        c["count"] += 1
        c["keyword_hits"] += 1 if result["keyword_filter_hit"] else 0
        c["last_seen"] = now
        c["brand"] = c["brand"] or result["brand"]
        c["samples"] = ([result["text"]] + c["samples"])[:5]
        c["timeline"].append(now)
        if len(c["_vectors"]) < MAX_MEMBERS:
            c["_vectors"].append(vec)
        return c

    @staticmethod
    def public(c: dict) -> dict:
        now = time.time()
        return {
            "id": c["id"], "scam_type": c["scam_type"], "brand": c["brand"], "domains": sorted(c["domains"]),
            "hosts": sorted(c["hosts"]),
            "phones": sorted(c["phones"]), "count": c["count"], "keyword_hits": c["keyword_hits"],
            "first_seen": c["first_seen"], "last_seen": c["last_seen"], "status": c["status"], "warned": c["warned"],
            "samples": c["samples"], "per_minute": sum(1 for t in c["timeline"] if now - t < 60),
        }

    def all_public(self):
        return sorted((self.public(c) for c in self.campaigns.values()), key=lambda x: -x["last_seen"])
