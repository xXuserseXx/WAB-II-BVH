import matplotlib.pyplot as plt

import csv
from pathlib import Path

def create_plots(raw_csv_path: Path, output_plot_path: Path):

    strategies = {}

    with raw_csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            particle_count = int(row["particle_count"])
            strategy = row["strategy"]

            bvh_checks = int(row["bounding_volume_checks"])
            primitive_checks = int(row["primitive_checks"])

            if strategy not in strategies:
                strategies[strategy] = {}

            if particle_count not in strategies[strategy]:
                strategies[strategy][particle_count] = {"bvh_checks": [],"primitive_checks": []}

            strategies[strategy][particle_count]["bvh_checks"].append(bvh_checks)
            strategies[strategy][particle_count]["primitive_checks"].append(primitive_checks)

        plt.figure(figsize=(8,5))

        for strategy, results in strategies.item():
            particle_counts = sorted(results.keys())
            means = []

            for particle_count in particle_counts:
                checks = results[particle_count]["bvh_checks"]
                mean = sum(checks) / len(checks)

                means.append(mean)

            plt.plot(particle_counts, means, marker="o", label=strategy)

            plt.xlabel("Partcle count")
    plt.ylabel("Mean bounding volume checks")
    plt.title("Mean BVH checks per run")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_plot_path / "mean_bvh_checks.png",dpi=300)

    plt.close()

    # Mean primitive checks
    plt.figure(figsize=(8, 5))

    for strategy, results in strategies.items():
        particle_counts = sorted(results.keys())
        means = []

        for particle_count in particle_counts:
            checks = results[particle_count]["primitive_checks"]
            mean = sum(checks) / len(checks)

            means.append(mean)

        plt.plot(particle_counts,means,marker="o",label=strategy)

    plt.xlabel("Partcle count")
    plt.ylabel("Mean primitive checks")
    plt.title("Mean primitive checks per run")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_plot_path / "mean_primitive_checks.png",dpi=300)

    plt.close()