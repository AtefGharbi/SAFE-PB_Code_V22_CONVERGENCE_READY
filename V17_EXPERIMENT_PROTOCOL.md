# SAFE-PB publication experiment protocol

The main runner enforces the complete protocol used for the paper. Its default
arguments equal the published configuration (10 seeds, 400 training episodes,
16 updates per episode, 10 held-out days per profile, binding profile with
`--stress-base-scale 0.25 --stress-homes-candidates 4`).

## Required design

- The default seed range is `0:10`. A run with fewer than 10 unique training
  seeds stops unless `--allow-fewer-seeds` is supplied for engineering tests.
- Every trained policy is evaluated on matched nominal and binding-voltage
  profiles. The binding profile is calibrated once, then frozen across all
  methods and seeds. The run fails if the SAFE-PB projection never activates.
- `episode_results.csv` records candidate actions, applied actions, projection
  deltas, candidate voltages, post-projection voltages, active projection
  steps, slack, and AC violations.
- The common comparison includes SAFE-PB ablations, No-DR, TOU, an approximate
  tabular Q-learning reconstruction, and a causal rolling-horizon price MPC.
- Training alternates nominal and binding-voltage days. Default objective
  weights are `beta_r=0.20` and `beta_f=2000`; their realized contributions are
  checked against a declared minimum fraction and written to
  `objective_diagnostics.json`. Select final weights on validation data only.
- Evaluation days are averaged inside each training seed. Paired tests,
  bootstrap confidence intervals, Holm correction, and paired Cohen's `d_z`
  are then calculated across training seeds. Evaluation days are not treated
  as independent replicates. The paired table includes CVaR90 and normalized
  discomfort variance, so the risk and fairness ablations have direct,
  objective-aligned contrasts.
- Batteries are excluded from discomfort-fairness indices because they have no
  requested-service discomfort. Structural zero values are not inserted into
  the fairness population.

## Installation and validation

```bash
pip install -r requirements.txt
pytest tests/ -q
```

## Short engineering run

This checks mechanics only and is deliberately marked non-publication:

```bash
python scripts/run_v17_experiments.py \
  --seeds 0:2 --allow-fewer-seeds \
  --train-episodes 50 --risk-warmup 10 \
  --q-train-episodes 100 --eval-days 2
```

## Publication run

The defaults select all methods, both scenario profiles and the published settings:

```bash
python scripts/run_v17_experiments.py
```

The default uses up to four worker processes. On Windows PowerShell:

```powershell
.\scripts\run_publication_fast.ps1 -Workers 4
```

The runner resumes matching completed method/seed jobs automatically. Each
cache entry carries a fingerprint of the scientific arguments, configuration,
environment, feeder, metrics, and trainer code. A mismatch stops rather than
combining incompatible evidence.

To increase the training budget while retaining the same protocol:

```bash
python scripts/run_v17_experiments.py \
  --seeds 0:10 --train-episodes 1000 \
  --updates-per-episode 24 --eval-days 20
```

The runner writes `episode_results.csv`, `publication_summary.csv`,
`per_seed_means.csv`, `paired_statistics.csv`, `objective_diagnostics.json`,
per-seed training logs, `progress.csv`, `results_digest.md`, six generated
figures, and `run_manifest.json` under
`results/publication_experiments/`. Checkpoints are optional because saving
every seed and ablation is large; add `--save-checkpoints` when required.

Runtime optimization does not replace AC validation. During training, the
candidate schedule's AC solve is omitted because that diagnostic enters no
reward, action, projection, transition, or observation. The applied schedule's
AC voltage is still computed because it enters the next observation. During
held-out evaluation, both candidate and applied schedules are independently
checked with the full AC power flow and written to the audit trail.

A run is complete when `run_manifest.json` reports `"status": "passed"`,
`"safety_activation_verified": true`, and both objective-signal checks are
true; `"publication_eligible": true` additionally requires that the run was not
launched with `--allow-fewer-seeds`. See the README for the status of the stored
runs in `results/`.
