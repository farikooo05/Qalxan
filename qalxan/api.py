"""FastAPI backend: analysis API, live event stream, campaign actions and the demo traffic simulator.

Run: uvicorn qalxan.api:app --reload
"""
import asyncio
import itertools
import json
import random
import time
from collections import deque
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import llm
from .campaigns import CampaignTracker
from .features import extract
from .pipeline import Analyzer
from .synth import SCAM, campaign_messages, legit_stream

WEB = Path(__file__).resolve().parent.parent / "web"

app = FastAPI(title="Qalxan", description="Scam campaign radar for telecom operators")
analyzer = Analyzer()
tracker = CampaignTracker(analyzer.model.vectorize)
recent: deque = deque(maxlen=80)
subscribers: set[asyncio.Queue] = set()
stats = {"processed": 0, "flagged": 0, "scams_true": 0, "qalxan_caught": 0, "keyword_caught": 0,
         "false_alarms": 0, "blocked": 0, "warned": 0, "reports": 0}
sim = {"running": False, "rate": 2.0, "pending": deque(), "rng": random.Random(42)}
sim["legit"] = legit_stream(sim["rng"])
_ids = iter(range(1, 10**9))
# One demo subscriber's phone (web/phone.html): what actually reaches them.
phone = {"inbox": deque(maxlen=40), "blocked": 0, "campaigns": set(), "rng": random.Random(7)}


class AnalyzeIn(BaseModel):
    text: str
    sender: str | None = None


class LaunchIn(BaseModel):
    scheme: str = "bank_card_block"
    n: int = 60


def broadcast(kind: str, data):
    payload = json.dumps({"type": kind, "data": data}, ensure_ascii=False, default=list)
    for q in list(subscribers):
        try:
            q.put_nowait(payload)
        except asyncio.QueueFull:
            pass


def sender_for(row, rng):
    if row["label"] == 1:
        return rng.choice([f"+994{rng.choice(['50', '55', '70', '77', '10'])}{rng.randint(1000000, 9999999)}",
                           "INFO", "Bank-AZ", "Bonus", f"+44{rng.randint(10**9, 10**10 - 1)}"])
    # genuine messages come from the sender they name ("Kapital Bank: ...", "Wolt: ...")
    head = row["text"].split(":")[0].strip()
    if ":" in row["text"] and 2 <= len(head) <= 22 and "*" not in head and not any(c.isdigit() for c in head):
        return head
    brand = extract(row["text"])["brand"]
    return brand or f"+99450{rng.randint(1000000, 9999999)}"


async def process(text: str, sender: str, truth: int | None, source: str, use_llm: bool):
    res = await asyncio.to_thread(analyzer.analyze, text, use_llm)
    camp = tracker.add(res)
    blocked = bool(camp and camp["status"] == "blocked")
    msg = {"id": next(_ids), "ts": time.time(), "sender": sender, "origin": source, "truth": truth,
           "campaign_id": camp["id"] if camp else None, "blocked": blocked, **res}
    stats["processed"] += 1
    stats["flagged"] += 1 if res["verdict"] == "scam" else 0
    stats["blocked"] += 1 if blocked else 0
    if truth is not None:
        stats["scams_true"] += truth
        stats["qalxan_caught"] += 1 if truth == 1 and res["verdict"] == "scam" else 0
        stats["keyword_caught"] += 1 if truth == 1 and res["keyword_filter_hit"] else 0
        stats["false_alarms"] += 1 if truth == 0 and res["verdict"] == "scam" else 0
    if source == "report":
        stats["reports"] += 1
    recent.appendleft(msg)
    broadcast("message", msg)
    if camp:
        broadcast("campaign", tracker.public(camp))
    broadcast("stats", stats)
    phone_deliver(msg)
    return msg


def phone_push(item):
    phone["inbox"].appendleft(item)
    broadcast("phone", item)


def phone_deliver(msg):
    """Decide what the demo subscriber's phone receives for a network message."""
    if msg["origin"] != "network":
        return
    r, cid = phone["rng"], msg["campaign_id"]
    if msg["truth"] == 1 and cid:
        if msg["blocked"]:
            if r.random() < 0.5:  # this subscriber was one of the campaign's targets
                phone["blocked"] += 1
                broadcast("phone", {"kind": "blocked", "count": phone["blocked"], "campaign_id": cid})
            return
        if cid not in phone["campaigns"] or r.random() < 0.3:
            phone["campaigns"].add(cid)
            phone_push({"kind": "sms", "id": msg["id"], "ts": msg["ts"], "sender": msg["sender"],
                        "text": msg["text"], "campaign_id": cid, "scam": True})
    elif msg["truth"] == 0 and r.random() < 0.15:
        phone_push({"kind": "sms", "id": msg["id"], "ts": msg["ts"], "sender": msg["sender"],
                    "text": msg["text"], "campaign_id": None, "scam": False})


async def simulator_loop():
    rng = sim["rng"]
    while True:
        if sim["running"]:
            if sim["pending"] and rng.random() < 0.55:
                row = sim["pending"].popleft()
            else:
                row = next(sim["legit"])
            await process(row["text"], sender_for(row, rng), row["label"], "network", use_llm=False)
            await asyncio.sleep(1.0 / sim["rate"])
        else:
            await asyncio.sleep(0.2)


@app.on_event("startup")
async def _start():
    asyncio.create_task(simulator_loop())

    async def bot_report(text, sender):
        return await process(text, sender, None, "report", use_llm=True)

    from .bot import run_bot
    asyncio.create_task(run_bot(bot_report))


@app.post("/api/analyze")
async def analyze(body: AnalyzeIn):
    if not body.text.strip():
        raise HTTPException(400, "empty text")
    return await process(body.text.strip(), body.sender or "subscriber report", None, "report", use_llm=True)


@app.get("/api/state")
async def state():
    return {"stats": stats, "campaigns": tracker.all_public(), "recent": list(recent),
            "sim": {"running": sim["running"], "rate": sim["rate"], "pending": len(sim["pending"])},
            "schemes": [s for s in SCAM], "llm": llm.available()}


@app.get("/api/events")
async def events():
    q: asyncio.Queue = asyncio.Queue(maxsize=500)
    subscribers.add(q)

    async def gen():
        try:
            yield "retry: 2000\n\n"
            while True:
                try:
                    payload = await asyncio.wait_for(q.get(), timeout=15)
                    yield f"data: {payload}\n\n"
                except asyncio.TimeoutError:
                    yield ": ping\n\n"
        finally:
            subscribers.discard(q)

    return StreamingResponse(gen(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.post("/api/sim/start")
async def sim_start(rate: float = 2.0):
    sim["running"], sim["rate"] = True, max(0.5, min(rate, 20.0))
    return {"running": True, "rate": sim["rate"]}


@app.post("/api/sim/stop")
async def sim_stop():
    sim["running"] = False
    return {"running": False}


@app.post("/api/sim/launch")
async def sim_launch(body: LaunchIn):
    if body.scheme not in SCAM:
        raise HTTPException(400, f"unknown scheme {body.scheme}")
    camp, msgs = campaign_messages(body.scheme, max(5, min(body.n, 300)), sim["rng"])
    sim["pending"].extend(msgs)
    sim["running"] = True
    return {"queued": len(msgs), "domains": camp["urls"], "phones": camp["phones"]}


@app.post("/api/sim/reset")
async def sim_reset():
    sim["running"] = False
    sim["pending"].clear()
    tracker.campaigns.clear()
    tracker._ids = itertools.count(1)
    phone["inbox"].clear()
    phone["campaigns"].clear()
    phone["blocked"] = 0
    recent.clear()
    for k in stats:
        stats[k] = 0
    broadcast("reset", {})
    return {"ok": True}


@app.post("/api/campaigns/{cid}/block")
async def block(cid: int):
    c = tracker.campaigns.get(cid)
    if not c:
        raise HTTPException(404, "campaign not found")
    c["status"] = "blocked"
    broadcast("campaign", tracker.public(c))
    return tracker.public(c)


@app.post("/api/campaigns/{cid}/warn")
async def warn(cid: int):
    c = tracker.campaigns.get(cid)
    if not c:
        raise HTTPException(404, "campaign not found")
    new = c["count"] - c["warned"]
    c["warned"] = c["count"]
    stats["warned"] += new
    if cid in phone["campaigns"]:
        brand = c["brand"] or "a bank"
        host = sorted(c["hosts"])[0] if c["hosts"] else "the link"
        phone_push({"kind": "warning", "id": next(_ids), "ts": time.time(), "sender": "Azercell · Qalxan",
                    "campaign_id": cid,
                    "text": f"⚠ Diqqət! {brand} adından gələn SMS fırıldaqdır. {host} linkinə keçməyin.\n"
                            f"Warning: the SMS from \"{brand}\" is a scam. Do not open {host} and never share "
                            f"card data or codes."})
    broadcast("campaign", tracker.public(c))
    broadcast("stats", stats)
    return {"warned_now": new, **tracker.public(c)}


@app.get("/api/health")
async def health():
    return {"ok": True, "llm": llm.available()}


@app.get("/api/phone")
async def phone_state():
    return {"inbox": list(phone["inbox"]), "blocked": phone["blocked"]}


@app.get("/")
async def index():
    return FileResponse(WEB / "index.html")


@app.get("/phone")
async def phone_page():
    return FileResponse(WEB / "phone.html")


app.mount("/static", StaticFiles(directory=WEB), name="static")
