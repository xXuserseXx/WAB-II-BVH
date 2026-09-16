from experiment.experiment import ExperimentConfig, run_experiment


def main():
  config = ExperimentConfig(
    #particle_counts=(25, 50, 100, 200, 500, 1000),
    particle_counts=(2,5,10,20),
    datasets_per_count=50,
    base_seed=42,
    circle_radius=1.0,
    coverage=0.1,
    strategies=("top_down", "bottom_up", "incremental"),
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