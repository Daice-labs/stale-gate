#!/usr/bin/env python3
"""Verify the shipped T15 records against the expected-output manifest.
Recomputes the quadratic regret shape with its chi-square comparison, the delay
estimate's accuracy, the null-world false-trip rate with its interval, the
canonical threshold bowl, and the staleness-run alarm timing from raw records."""
import json, math, sys
import numpy as np, pandas as pd
import scipy.stats as st

exp = json.load(open("expected_outputs.json")); fail = []
def check(name, got, want, tol=1e-4):
    ok = (abs(got - want) <= tol) if isinstance(want, float) else (got == want)
    print(("  OK   " if ok else "  FAIL ") + f"{name}: {round(got,6) if isinstance(got,float) else got} (expected {want})")
    if not ok: fail.append(name)

reg = pd.read_csv("results/regret_linearity.csv")
eps, r, se = reg.eps.values, reg.regret.values, reg.regret_se.values
quad = np.polyfit(eps, r, 2); lin = np.polyfit(eps, r, 1)
chi_q = float((((r - np.polyval(quad, eps)) / se) ** 2).sum())
chi_l = float((((r - np.polyval(lin, eps)) / se) ** 2).sum())
check("quadratic_curvature", float(quad[0]), exp["quad_a"], 0.05)
check("quadratic_R2", 1 - ((r - np.polyval(quad, eps)) ** 2).sum() / ((r - r.mean()) ** 2).sum(), exp["quad_R2"], 1e-3)
check("chi2_rejects_linear", chi_l > 11.34 and chi_q < 1.0, True)

dly = pd.read_csv("results/guard_delay.csv")
ratios = dly.mean_delay.values / dly.predicted_scale.values
check("delay_ratio_min", float(ratios.min()), exp["delay_ratio_min"], 0.01)
check("delay_ratio_max", float(ratios.max()), exp["delay_ratio_max"], 0.01)

nw = pd.read_csv("results/null_world_trips.csv")
k, n = int(nw.tripped.sum()), len(nw)
check("null_world_trips", k, exp["null_trips"]); check("null_world_n", n, exp["null_n"])
lo = st.beta.ppf(0.025, k, n - k + 1); hi = st.beta.ppf(0.975, k + 1, n - k)
check("false_trip_CI_low", float(lo), exp["cp_low"], 5e-4)
check("false_trip_CI_high", float(hi), exp["cp_high"], 5e-4)

bowl = json.load(open("results/threshold_bowl.json"))
check("bowl_cost_at_060", float(bowl["0.60"]["cost"]), exp["bowl_060"], 1e-4)
check("bowl_flat_within_MC", max(abs(bowl[t]["rise_vs_060"]) for t in bowl) <= exp["bowl_max_rise"] + 1e-6, True)

sta = pd.read_csv("results/staleness.csv")
alarm = int(sta.loc[sta.guard_logE >= math.log(1 / 0.05), "epoch"].iloc[0])
check("staleness_alarm_epoch", alarm, exp["alarm_epoch"])
fcr0 = float(sta[sta.epoch < 8].FCR.mean()); fcrpk = float(sta[sta.epoch >= 8].FCR.max())
check("fcr_baseline", fcr0, exp["fcr_baseline"], 3e-3)
check("fcr_peak_after_onset", fcrpk, exp["fcr_peak"], 3e-3)

s = json.load(open("results/summary_extended.json"))
check("theory_curvature_half_Lf", float(s["regret_shape"]["theory_curvature"]["half_L_f"]), exp["half_Lf"], 0.05)
print("\n" + ("ALL CHECKS PASSED" if not fail else f"{len(fail)} CHECK(S) FAILED"))
sys.exit(0 if not fail else 1)
