import csv
from pathlib import Path

@dataclass
class ExperimentConfig:
    particle_counts:tuple[int]
    datasets_per_count: int
    circle_radius: float
    coverage: float
    strategies: tuple[str]
    create_plots: bool

    def validate(self):
        pass

def _write_raw_results_csv(path: Path, rows: list[dict[str]]) -> None:
    fieldnames = [
        "particle_count",
        "dataset_id",
        "domain_side",
        "coverage",
        "radius",
        "strategy",
        "bounding_volume_checks",
        "primitive_checks",
        "tree-height",
        "total_aabb_area",
    ]
    with path.open("w", encoding="utf-8") as w:
        writer = csv.DictWriter(w, fieldnames=fieldnames)
        writer.writeheader
        writer.writerows(rows)

def run_experiment(config: ExperimentConfig, output_dir: Path):
    config.validate
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    #Config speichern

    