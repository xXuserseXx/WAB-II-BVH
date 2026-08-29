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
        "tree_height",
        "total_aabb_area",
    ]
    with path.open("w", encoding="utf-8") as w:
        writer = csv.DictWriter(w, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def run_experiment(
    config: ExperimentConfig,
    output_dir: str | Path,
) -> list[dict[str]]:
    config.validate()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    raw_rows: list[dict[str]] = []

    for particle_count in config.particle_counts:
        for dataset_id in range(config.datasets_per_count):

            dataset_seed = det_seed(
                config.base_seed,
                particle_count,
                dataset_id,
            )

            particles, domain_side = generate_particle_set(
                particle_count,
                config.circle_radius,
                config.coverage,
                dataset_seed,
            )

            reference_pairs = None
            reference_candidates = None

            if config.validate_against_brute_force:
                reference_pairs = brute_force_collisions(particles)
                reference_candidates = brute_force_aabb_overlaps(particles)

            # Alle Strategien erhalten exakt denselben Datensatz.
            for strategy in config.strategies:

                root = BUILDERS[strategy](particles) # TODO

                result = detect_all_pairs( 
                    root,
                    particles,
                ) #TODO Hierfür brauche ich noch mindestens einen builder, das kommt als nächstes

                if (
                    reference_candidates is not None
                    and result.candidate_pairs != reference_candidates
                ):
                    missing = sorted(
                        reference_candidates - result.candidate_pairs
                    )[:10]

                    unexpected = sorted(
                        result.candidate_pairs - reference_candidates
                    )[:10]

                    raise AssertionError(
                        f"Candidate mismatch for {strategy}, "
                        f"n={particle_count}, dataset={dataset_id}; "
                        f"missing={missing}, "
                        f"unexpected={unexpected}"
                    )

                if (
                    reference_pairs is not None
                    and result.collision_pairs != reference_pairs
                ):
                    missing = sorted(
                        reference_pairs - result.collision_pairs
                    )[:10]

                    unexpected = sorted(
                        result.collision_pairs - reference_pairs
                    )[:10]

                    raise AssertionError(
                        f"Collision mismatch for {strategy}, "
                        f"n={particle_count}, dataset={dataset_id}; "
                        f"missing={missing}, "
                        f"unexpected={unexpected}"
                    )

                raw_rows.append(
                    {
                        "particle_count": particle_count,
                        "dataset_id": dataset_id,
                        "domain_side": domain_side,
                        "coverage": config.coverage,
                        "radius": config.circle_radius,
                        "strategy": strategy,
                        "bounding_volume_checks": result.bounding_volume_checks,
                        "primitive_checks": result.primitive_checks,
                        # Die beiden muss ich noch implementieren, ich will aber erstmal was ans laufen kriegen
                        # "tree_height": tree_height(root),
                        # "total_aabb_area": total_internal_aabb_area(root),
                    }
                )

            print(
                f"completed n={particle_count}, "
                f"dataset={dataset_id + 1}/"
                f"{config.datasets_per_count}"
            )

    raw_path = output_path / "raw_results.csv"

    _write_raw_results_csv(
        raw_path,
        raw_rows,
    )

    return raw_rows