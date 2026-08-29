from experiment.experiment import ExperimentConfig, run_experiment


def main():
  config = ExperimentConfig(
    particle_counts=(10, 100),
    datasets_per_count=2,
    base_seed=42,
    circle_radius=1.0,
    coverage=0.1,
    strategies=("top_down",),
    create_plots=False,
    validate_against_brute_force=True,
  )

  rows = run_experiment(
    config,
    "results"
  )

  print(f"Experiment finished with {len(rows)} runs.")


if __name__ == "__main__":
  main()