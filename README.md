# RP-T15 Reproduction Package: The Stale Gate

Accompanies "The Stale Gate: Pricing Calibration Drift and Guarding Score-Gated Deployment with
Anytime-Valid Monitors." Every number in the paper recomputes from the records here.

| Component | Location |
|---|---|
| Source code | `code/RP-T15-stale-gate-study.ipynb` (all experiments, figures, records) |
| Executed outputs | `executed/RP-T15-executed.ipynb` |
| Raw records | `results/` (regret sweep, delay sweep, 400-deployment null world with per-stream seeds, staleness run, canonical threshold bowl, adjudication) |
| Per-seed records | `results/null_world_trips.csv` (per-stream seeds); seed rules in `results/summary.json` |
| Configuration | `results/summary.json` and `results/summary_extended.json` (cost model, drift catalog, guard tuning) |
| Verification script | `verify_results.py` (recomputes the quadratic regret with its chi-square comparison, delay accuracy, false-trip interval, threshold bowl, and alarm timing) |
| Expected-output manifest | `expected_outputs.json` |
| One-command reproduction | `./repro.sh` (free, no API; deterministic under recorded seeds) |
| Paper source and PDF | `paper/` |
| Checksums | `CHECKSUMS.txt` | License | set at de-anonymization | Citation | `CITATION.cff` |
