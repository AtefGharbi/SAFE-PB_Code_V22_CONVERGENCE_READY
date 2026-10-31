# SAFE-PB: power-flow-corrected safety projection for hierarchical multi-agent pricing

Code, configuration and results for the paper *Power-Flow-Corrected Safety
Projection for Hierarchical Multi-Agent Reinforcement Learning in
Network-Constrained Residential Dynamic Pricing* (A. Gharbi and A. Alshammari).

The package contains:

- **The proposed safety layer** (`safe_pb/safety_projection.py`):
  - `lexicographic_project`: Stage 1 minimum-slack LP (HiGHS), then Stage 2
    minimum-distance QP (SLSQP) with the slack vector fixed;
  - `ac_corrected_project`: the lexicographic projection repeated with a
    per-bus bias `V_AC - V_lin` measured by AC power flow at the current
    iterate, up to `max_corrections = 4`;
  - `authority_certificate`: one AC power flow with every device at its lower
    power bound, used to label violations;
  - `project`: the conventional soft-penalty projection (`SLACK_PENALTY = 1e4`),
    kept as the reference method (`EnvConfig(projection_mode="soft")`).
- **The hierarchical controller**: a utility soft actor-critic agent setting
  tariff-category prices and parameter-shared household agents with
  centralised training and decentralised execution (`safe_pb/sac_trainer.py`,
  `safe_pb/sac_networks.py`, `safe_pb/environment.py`).
- **Baselines**: No-DR, time-of-use pricing, a reconstruction of the tabular
  Q-learning pricing method of Wan *et al.* (2022) and a causal rolling-horizon
  price MPC (`safe_pb/baselines.py`, `safe_pb/baseline_evaluation.py`).
- **Experiment runners and the stored results** behind every table and figure
  in the paper (`scripts/`, `paper_scripts/`, `results/`).

## Terminology: code vs. paper

| Code / CSV column | Paper |
|---|---|
| `controllable_violation_minutes` | controllable violation minutes |
| `exogenous_violation_minutes` | **state-infeasible** violation minutes: no device-feasible action meets the voltage floor at the realised state (which may itself reflect earlier control actions, e.g. storage depletion) |
| `authority_feasible` | authority-feasible step (the certificate passes) |
| `Tabular_Q_learning` | Q-learning baseline |

The authority certificate is exact for the linearised (LinDistFlow) model. For
the AC model it is an empirically validated screen: voltage monotonicity in
consumption was verified on the studied IEEE 33-bus feeder, not proven in
general.

## Requirements and installation

Python 3.12 or 3.13.

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` pins the versions used for the paper. If a pin does not
resolve on your platform, remove the `==x.y.z` suffixes; the code depends only
on stable APIs of numpy, scipy, pandas, matplotlib, pandapower, PyYAML and
PyTorch.

## Tests

```bash
pytest tests/ -q
```

`tests/test_core.py` covers the household, EV, battery, PV and feeder models
and the projection properties; `tests/test_v23_projection.py` covers the
lexicographic and AC-corrected projection and the authority certificate;
`tests/test_sac_training.py` covers the SAC/CTDE training mechanics (requires
PyTorch); `tests/test_publication_protocol.py` covers the experiment runner
and the statistics pipeline.

## Reproducing the paper

1. **Projection stress test (168 cases; Table and figure of the stress-set
   results).** Runs in a few minutes on one CPU core.

   ```bash
   python scripts/run_safety_revalidation.py
   ```

   Writes `results/safety_revalidation_cases.csv` and
   `results/safety_revalidation_summary.json`.

2. **Closed-loop experiment (10 training seeds x 9 methods, 10 held-out days
   per profile).** The runner's defaults equal the published configuration:

   ```bash
   python scripts/run_v17_experiments.py --output-dir results/publication_v23
   ```

   which is equivalent to

   ```bash
   python scripts/run_v17_experiments.py --seeds 0:10 --train-episodes 400 \
       --updates-per-episode 16 --eval-days 10 --stress-base-scale 0.25 \
       --stress-homes-candidates 4 --output-dir results/publication_v23
   ```

   Each 400-episode training run took 3.5-13 min on one CPU core. Use
   `--workers N` to run independent method/seed jobs in parallel; completed
   jobs are cached under `job_cache/` and resumed automatically.

3. **Untrained-policy reference.**

   ```bash
   python scripts/run_v17_experiments.py --train-episodes 0 --methods SAFE-PB,No-DR \
       --output-dir results/untrained_reference_v23
   ```

4. **Tables and figures.**

   ```bash
   python paper_scripts/make_results.py results/publication_v23
   python paper_scripts/fig_safety.py
   python paper_scripts/fig_arch.py
   ```

   Outputs go to `paper_outputs/`.

## Stored results

- `results/safety_revalidation_*`: the 168-case stress test.
- `results/publication_v23/`: the closed-loop run reported in the paper
  (`per_seed_means.csv`, `paired_statistics.csv`, `episode_results.csv`,
  per-seed training logs, `objective_diagnostics.json`, `run_manifest.json`).
- `results/untrained_reference_v23/`: the untrained-policy reference.

**About the stored manifests.**

- `results/publication_v23/run_manifest.json` reports `"status": "passed"` but
  `"publication_eligible": false`. This flag only records that the run was
  launched with `--allow-fewer-seeds` while the runner's default minimum was
  20 seeds. The default minimum is now 10, so the command in step 2 (without
  that flag) repeats the same configuration and marks it eligible. The
  scientific settings and results are unaffected.
- `results/untrained_reference_v23/run_manifest.json` reports
  `"status": "failed"`. All evaluation outputs (`per_seed_means.csv`,
  `episode_results.csv`, ...) were written before the failure, which occurred
  afterwards in the training-objective diagnostic because a zero-episode run
  has no training log. The diagnostic now skips zero-episode runs.

## Repository layout

```
safe_pb/
  data_loader.py            scenario construction (benchmark parameters + synthetic demand traces)
  household_models.py       flexible and non-dispatchable loads
  ev_model.py               EV model with availability window and terminal target
  battery_model.py          stationary battery (SoC dynamics, degradation cost)
  pv_model.py               rooftop PV as a network injection
  feeder_model.py           IEEE 33-bus feeder, LinDistFlow model, AC power flow (pandapower)
  safety_projection.py      soft-penalty, lexicographic and AC-corrected projections; authority certificate
  environment.py            SafePBEnv: hierarchical pricing environment, every step routed through the projection
  sac_networks.py, sac_trainer.py   hierarchical SAC with CTDE, CVaR and fairness terms
  baselines.py, baseline_evaluation.py   No-DR, TOU, tabular Q-learning, MPC
  episode_metrics.py, metrics.py, statistical_analysis.py   metrics, paired tests, bootstrap CIs, Holm correction
  publication_reporting.py, plotting.py, evaluation.py      summaries and figures
config/tier_a_wan2022.yaml  all scenario parameters, each tagged [TABLE], [APPROX] or [SAFE-PB EXTENSION]
scripts/                    experiment runners (stress test, closed-loop protocol, convergence study, demos)
paper_scripts/              scripts that build the paper's tables and figures
tests/                      unit and protocol tests
results/                    stored results used in the paper
```

## Parameter provenance

Every non-obvious number in `config/tier_a_wan2022.yaml` is tagged `[TABLE]`
(taken from the tables of Wan *et al.*, 2022), `[APPROX]` (synthetic
reconstruction of a published shape, with no claim of numerical fidelity) or
`[SAFE-PB EXTENSION]` (not in the source benchmark, e.g. batteries and PV).

## Limitations

These match the limitations stated in the paper.

- Demand traces are synthetic; the controllable population is small (14
  agents, replicated per bus); only the IEEE 33-bus feeder is studied.
- Only undervoltage is enforced by the certificate; overvoltage requires the
  analogous upper-bound test. Line and transformer thermal limits are not
  enforced because the test case's line ratings are not meaningful.
- The AC correction has no convergence guarantee; the authority certificate
  relies on voltage monotonicity verified empirically for this feeder.
- Training used 400 episodes and had not converged; the economic comparison
  is indicative. `scripts/run_convergence_study.py` runs longer budgets.
- The per-step projection is myopic with respect to storage.
- Battery power is billed at the general-dispatchable price; PV is modelled as
  a network injection only (no self-consumption or export economics).

## Reference

Y. Wan, J. Qin, X. Yu, T. Yang, and Y. Kang, "Price-based residential demand
response management in smart grids: A reinforcement learning-based
approach," *IEEE/CAA Journal of Automatica Sinica*, vol. 9, no. 1,
pp. 123-134, 2022.
