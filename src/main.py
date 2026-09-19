from experiment.experiment import ExperimentConfig, run_experiment
from plyer import notification



def main():
  config = ExperimentConfig(
    #particle_counts=(25, 50, 100, 200, 500, 1000),
    particle_counts=(2,5,10,20),
    datasets_per_count=50,
    base_seed=42,
    circle_radius=1.0,
    coverage=(0.05, 0.1, 0.2),
    strategies=("top_down", "bottom_up", "incremental"),
    create_plots=True,
    validate_against_brute_force=True,
  )

  rows = run_experiment(
    config,
    "results"
  )

  print(f"Experiment finished with {len(rows)} runs.")

  
  notification.notify(title="BVH Experiment fertig",message= f"Der Experiment run mit{len(rows)} runs ist durchgelaufen",app_name="BVH Experiment", timeout=10)


if __name__ == "__main__":
  main()