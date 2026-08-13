from __future__ import annotations
from dataclasses import dataclass

import csv
from pathlib import Path

from .dataset import det_seed, generate_particle_set
from collision.validation import  brute_force_collisions, brute_force_aabb_overlaps

@dataclass
class ExperimentConfig:
    particle_counts:tuple[int]
    datasets_per_count: int
    base_seed: int
    circle_radius: float
    coverage: float
    strategies: (tuple[str])
    create_plots: bool

    validate_against_brute_force: bool

    def validate(self):
        # TODO
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

    for particle_count in config.particle_counts:
        for dataset_id in range(config.datasets_per_count):

            dataset_seed = det_seed(config.base_seed,particle_count, dataset_id)

            particles, domain_side = generate_particle_set(particle_count, config.circle_radius, config.coverage, dataset_seed)

            reference_pairs = None
            reference_candidates = None

            if config.validate_against_brute_force:
                reference_pairs = brute_force_collisions(particles)
                reference_candidates = brute_force_aabb_overlaps(particles)

            for strategies in config.strategies:
                root = 

            