"""Our own scam classifier, trained on CPU in seconds.

Inputs: normalized text (character n-grams survive letter swaps and typos, word n-grams carry meaning)
plus rule signals from features.py. Two heads: scam probability and scam type.
"""
from pathlib import Path

import joblib
import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from .features import extract, feature_vector
from .normalize import normalize

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "qalxan.joblib"
RULE_WEIGHT = 2.0


class QalxanModel:
    def __init__(self, use_rules=True, use_words=True):
        self.use_rules = use_rules
        self.use_words = use_words
        self.char_vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, sublinear_tf=True,
                                        max_features=60000)
        self.word_vec = TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=2, sublinear_tf=True,
                                        token_pattern=r"(?u)\b\w+\b", max_features=30000)
        self.clf = LogisticRegression(C=4.0, class_weight="balanced", max_iter=3000)
        self.type_clf = LogisticRegression(C=4.0, max_iter=3000)

    def _matrix(self, texts, fit=False):
        norm = [normalize(t) for t in texts]
        parts = [self.char_vec.fit_transform(norm) if fit else self.char_vec.transform(norm)]
        if self.use_words:
            parts.append(self.word_vec.fit_transform(norm) if fit else self.word_vec.transform(norm))
        if self.use_rules:
            rules = np.array([feature_vector(extract(t)) for t in texts]) * RULE_WEIGHT
            parts.append(csr_matrix(rules))
        return hstack(parts).tocsr()

    def fit(self, texts, labels, schemes):
        X = self._matrix(texts, fit=True)
        y = np.array(labels)
        self.clf.fit(X, y)
        scam_idx = np.where(y == 1)[0]
        self.type_clf.fit(X[scam_idx], np.array(schemes)[scam_idx])
        return self

    def predict(self, texts):
        """Return list of (scam_probability, scam_type, type_confidence)."""
        X = self._matrix(texts)
        probs = self.clf.predict_proba(X)[:, 1]
        tprobs = self.type_clf.predict_proba(X)
        out = []
        for p, tp in zip(probs, tprobs):
            k = int(np.argmax(tp))
            out.append((float(p), str(self.type_clf.classes_[k]), float(tp[k])))
        return out

    def vectorize(self, text):
        """Character n-gram vector used to group messages into campaigns (L2-normalized)."""
        return self.char_vec.transform([normalize(text)])

    def save(self, path=MODEL_PATH):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)

    @staticmethod
    def load(path=MODEL_PATH):
        return joblib.load(path)
