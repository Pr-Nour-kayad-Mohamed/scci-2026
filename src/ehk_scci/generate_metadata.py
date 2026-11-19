from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    repo_root = Path(__file__).resolve().parents[2]
    processed_dir = repo_root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    checksums = {}
    for csv_path in sorted(processed_dir.glob("*.csv")):
        rel_key = csv_path.relative_to(repo_root).as_posix()
        checksums[rel_key] = sha256_file(csv_path)

    metadata = {
        "dataset_id": "scci-2026-pulsar-sensitivity",
        "generated_at_utc": datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "code_version": "scci-2026-v1.0",
        "epistemic_status": "parametric_sensitivity_benchmark_only",
        "not_an_observational_constraint": True,
        "methodological_reference_threshold": {
            "value": 1e-13,
            "unit": "s s^-1",
            "role": "internal_numerical_sensitivity_benchmark",
        },
        "perturbative_bounds_polynomial": {
            "closure": "R(Phi) = 1 + eta * Phi^2",
            "identification_hypothesis": "R == Z_A",
            "max_eta_phi_max_sq": 0.1,
            "max_abs_delta_alpha": 0.1,
        },
        "grids": {
            "standard_sweep": {
                "parameters": ["alpha_star", "kappa_R"],
                "description": "Grille parametrique standard sur (alpha_star, kappa_R)",
                "present": (processed_dir / "pulsar_field_sweep_results.csv").exists(),
            },
            "polynomial_sweep": {
                "parameters": ["eta", "phi_0"],
                "description": "Grille parametrique de la fermeture polynomiale sur (eta, phi_0)",
                "present": (processed_dir / "pulsar_field_sweep_polynomial_results.csv").exists(),
            },
        },
        "sha256_checksums": checksums,
    }

    out_path = processed_dir / "metadata.json"
    out_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"[*] Metadonnees generees : {out_path}")


if __name__ == "__main__":
    main()
