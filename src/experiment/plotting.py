import csv
from pathlib import Path

import matplotlib.pyplot as plt


def create_plots(raw_csv_path: Path, output_plot_path: Path):
    strategies_by_coverage = {}
    with raw_csv_path.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            coverage = float(row["coverage"])
            results = strategies_by_coverage.setdefault(coverage, {}).setdefault(
                row["strategy"], {}
            ).setdefault(int(row["particle_count"]), {"bvh_checks": [], "primitive_checks": []})
            results["bvh_checks"].append(int(row["bounding_volume_checks"]))
            results["primitive_checks"].append(int(row["primitive_checks"]))

    for coverage, strategies in strategies_by_coverage.items():
        label = f"{coverage:g}"
        suffix = label.replace(".", "_")
        for metric, ylabel, prefix in (
            ("bvh_checks", "Mean bounding volume checks", "mean_bvh_checks"),
            ("primitive_checks", "Mean primitive checks", "mean_primitive_checks"),
        ):
            plt.figure(figsize=(8, 5))
            for strategy, results in strategies.items():
                counts = sorted(results)
                means = [sum(results[n][metric]) / len(results[n][metric]) for n in counts]
                plt.plot(counts, means, marker="o", label=strategy)
            plt.xlabel("Particle count")
            plt.ylabel(ylabel)
            plt.title(f"{ylabel} per run (coverage={label})")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(output_plot_path / f"{prefix}_coverage_{suffix}.png", dpi=300)
            plt.close()

            # Boxplots show the distribution across datasets, including min/max.
            plt.figure(figsize=(8, 5))
            positions = []
            labels = []
            plot_data = []
            position = 1
            for strategy, results in strategies.items():
                for particle_count in sorted(results):
                    plot_data.append(results[particle_count][metric])
                    positions.append(position)
                    labels.append(f"{strategy}\n{particle_count}")
                    position += 1

            plt.boxplot(plot_data, positions=positions, showmeans=True, whis=(0, 100))
            plt.xticks(positions, labels, rotation=45, ha="right")
            plt.xlabel("Strategy and particle count")
            plt.ylabel(ylabel)
            plt.title(f"{ylabel} distribution (coverage={label})")
            plt.grid(True, axis="y")
            plt.tight_layout()
            plt.savefig(
                output_plot_path / f"{prefix}_boxplot_coverage_{suffix}.png",
                dpi=300,
            )
            plt.close()
