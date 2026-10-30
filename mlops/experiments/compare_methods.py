"""Compare matching methods and weight settings; log every run to MLflow.

Run from the project root:
    python mlops/experiments/compare_methods.py            # TF-IDF + skills
    python mlops/experiments/compare_methods.py --sbert    # also SBERT (needs sentence-transformers)
View the results:
    mlflow ui --backend-store-uri sqlite:///mlflow.db      # then open http://127.0.0.1:5000
"""
import argparse
import itertools
import json
from pathlib import Path

from sklearn.metrics import roc_auc_score

from resumeiq_nlp.matching import DEFAULT_WEIGHTS, score_components

DATA = Path(__file__).resolve().parents[1] / "data" / "sample_pairs.json"
TRACKING_URI = "sqlite:///mlflow.db"
EXPERIMENT = "resumeiq-matching"


def load_scores(use_sbert: bool):
    """Raw TF-IDF / SBERT / skills scores for every (job, resume) pair."""
    data = json.loads(DATA.read_text(encoding="utf-8"))
    corpus = [r["text"] for r in data["resumes"]] + [j["text"] for j in data["jobs"]]  # IDF from the whole corpus
    pairs, sbert_ok = [], use_sbert
    for job in data["jobs"]:
        for res in data["resumes"]:
            c = score_components(res["text"], job["title"], job["text"], use_sbert=use_sbert, corpus=corpus)
            if use_sbert and c["sbert"] is None:
                sbert_ok = False
            pairs.append({
                "job": job["id"], "resume": res["id"],
                "tfidf": c["tfidf"], "sbert": c["sbert"] or 0.0, "skills": c["skills"],
                "label": int(res["id"] in data["relevant"][job["id"]]),
            })
    return pairs, sbert_ok, [j["id"] for j in data["jobs"]]


def combine(pair, w):
    return w["tfidf"] * pair["tfidf"] + w["sbert"] * pair["sbert"] + w["skills"] * pair["skills"]


def evaluate(pairs, job_ids, w):
    scored = [(p["job"], p["label"], combine(p, w)) for p in pairs]
    auc = roc_auc_score([s[1] for s in scored], [s[2] for s in scored])
    rr, top1 = [], []
    for job in job_ids:
        ranked = sorted((s for s in scored if s[0] == job), key=lambda s: -s[2])
        first = next(i for i, s in enumerate(ranked, start=1) if s[1] == 1)
        rr.append(1 / first)
        top1.append(1 if first == 1 else 0)
    return {"roc_auc": auc, "mrr": sum(rr) / len(rr), "top1_accuracy": sum(top1) / len(top1)}


def weight_grid(sbert_ok: bool, step: int = 4):
    for i, j, k in itertools.product(range(step + 1), repeat=3):
        if i + j + k == step and (sbert_ok or j == 0):
            yield {"tfidf": i / step, "sbert": j / step, "skills": k / step}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sbert", action="store_true", help="include SBERT scores")
    args = ap.parse_args()

    import mlflow

    pairs, sbert_ok, job_ids = load_scores(args.sbert)
    if args.sbert and not sbert_ok:
        print("SBERT could not be loaded; running without it.")
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT)

    default = dict(DEFAULT_WEIGHTS)
    if not sbert_ok:
        rest = default["tfidf"] + default["skills"]
        default = {"tfidf": default["tfidf"] / rest, "sbert": 0.0, "skills": default["skills"] / rest}
    named = {"tfidf_only": {"tfidf": 1, "sbert": 0, "skills": 0}, "skills_only": {"tfidf": 0, "sbert": 0, "skills": 1},
             "hybrid_default": default}
    if sbert_ok:
        named["sbert_only"] = {"tfidf": 0, "sbert": 1, "skills": 0}

    runs = [(name, "baseline", w) for name, w in named.items()]
    runs += [(f"grid_t{w['tfidf']:.2f}_s{w['sbert']:.2f}_k{w['skills']:.2f}", "grid", w) for w in weight_grid(sbert_ok)]

    best = None
    for name, kind, w in runs:
        m = evaluate(pairs, job_ids, w)
        with mlflow.start_run(run_name=name):
            mlflow.log_params({"w_tfidf": round(w["tfidf"], 3), "w_sbert": round(w["sbert"], 3), "w_skills": round(w["skills"], 3),
                               "sbert_available": sbert_ok, "n_pairs": len(pairs)})
            mlflow.log_metrics({k: round(v, 4) for k, v in m.items()})
            mlflow.set_tags({"kind": kind, "dataset": DATA.name})
        key = (m["mrr"], m["roc_auc"])
        if best is None or key > best[0]:
            best = (key, name, w, m)
    print(f"Logged {len(runs)} runs to {TRACKING_URI} (experiment '{EXPERIMENT}').")
    print(f"Best by MRR then AUC: {best[1]}  weights={best[2]}  metrics={ {k: round(v, 3) for k, v in best[3].items()} }")


if __name__ == "__main__":
    main()