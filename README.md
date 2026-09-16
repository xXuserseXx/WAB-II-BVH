# BVH Construction Strategy Comparison

This repository contains the implementation and experiment runner for comparing three Bounding Volume Hierarchy (BVH) construction strategies for static 2D collision detection:

- Top-down
- Bottom-up
- Incremental

The accompanying paper contains the full methodology, theoretical background and evaluation. This README only covers what is needed to run and use the implementation.

## Requirements

- Python 3.10 or newer
- `matplotlib`

Create and activate a virtual environment if desired.

### Windows

```powershell
python -m venv myenv
.\myenv\Scripts\activate
pip install matplotlib
```

### Linux / macOS

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install matplotlib
```

## Project Structure

```text
.
├── results/
├── src/
│   ├── basic_geometry/
│   ├── collision/
│   ├── experiment/
│   ├── tree_construction/
│   └── main.py
└── paper/
```

Relevant implementation files:

```text
src/basic_geometry/
    aabb.py
    primitive.py
    vec2.py

src/tree_construction/
    node.py
    top_down.py
    bottom_up.py
    incremental.py

src/collision/
    traversal.py
    validation.py

src/experiment/
    dataset.py
    experiment.py
    plotting.py
```

## Running the Experiment

Run the project from the repository root:

```powershell
python src/main.py
```

Do not run `src/experiment/experiment.py` directly.

The imports currently assume that `src` is used as the Python import root. Running the experiment module directly can therefore result in errors such as:

```text
ModuleNotFoundError: No module named 'tree_construction'
```

Starting the program through `src/main.py` avoids this.

## Experiment Configuration

Experiment parameters are configured in `src/main.py`.

Example:

```python
config = ExperimentConfig(
    particle_counts=(25, 50, 100, 200, 500, 1000),
    datasets_per_count=50,
    base_seed=42,
    circle_radius=1.0,
    coverage=0.1,
    strategies=("top_down", "bottom_up", "incremental"),
    create_plots=True,
    validate_against_brute_force=True,
)
```

### Parameters

| Parameter | Description |
|---|---|
| `particle_counts` | Particle counts that should be tested |
| `datasets_per_count` | Number of independently generated datasets per particle count |
| `base_seed` | Base value used to generate deterministic dataset seeds |
| `circle_radius` | Radius of all particles |
| `coverage` | Approximate fraction of the domain covered by particles |
| `strategies` | BVH construction strategies to execute |
| `create_plots` | Enables creation of result plots after the run |
| `validate_against_brute_force` | Compares BVH results against brute-force reference results |

Available strategy names are:

```python
("top_down", "bottom_up", "incremental")
```

## Output

Experiment results are written to the `results` directory.

The raw data is stored in:

```text
results/raw_results.csv
```

The CSV contains one row per strategy and dataset and includes:

```text
particle_count
dataset_id
domain_side
coverage
radius
strategy
bounding_volume_checks
primitive_checks
```

Additional columns may be present for supplementary metrics.

If plotting is enabled, the generated figures are stored in the same directory:

```text
results/mean_bvh_checks.png
results/mean_primitive_checks.png
```

The plots show the mean number of checks for each particle count and construction strategy.

## Validation

When `validate_against_brute_force=True`, each dataset is checked against brute-force reference calculations.

The experiment verifies:

- AABB candidate pairs
- Actual circle-circle collision pairs

The BVH structure can additionally be validated with `validate_bvh()` before traversal.

A failed validation raises an assertion error and stops the experiment.

For a final experiment run, validation should normally remain enabled.

## Reproducibility

Dataset generation is deterministic.

The seed for each dataset is derived from:

- `base_seed`
- particle count
- dataset ID

Running the same configuration again therefore generates the same datasets.

All construction strategies receive the same dataset for a given particle count and dataset ID.

## Plot Generation Only

If an experiment has already completed and `raw_results.csv` exists, plots can be generated again without rerunning the full experiment.

Example:

```python
from pathlib import Path
from experiment.plotting import create_plots

create_plots(
    Path("results/raw_results.csv"),
    Path("results"),
)
```

When running this as a separate script, make sure `src` is on the Python import path or place the call inside the existing project execution flow.

## Notes on Runtime

The bottom-up construction is significantly more expensive than the other construction strategies because it repeatedly searches for the best pair of active nodes to merge.

Large particle counts can therefore take substantially longer, especially when many datasets are used.

A short pilot run can be useful before starting a full experiment, for example:

```python
particle_counts=(1000,)
datasets_per_count=1
```

## Typical Workflow

1. Configure the experiment in `src/main.py`.
2. Enable validation.
3. Enable plots if desired.
4. Run:

```powershell
python src/main.py
```

5. Wait for all configured datasets to finish.
6. Inspect:

```text
results/raw_results.csv
results/mean_bvh_checks.png
results/mean_primitive_checks.png
```

The detailed interpretation of the experiment and its results is part of the accompanying paper.
