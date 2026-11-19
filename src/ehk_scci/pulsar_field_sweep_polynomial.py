"""
Balayage polynomial (eta, phi0) avec deux filtres :
1. Validite perturbative du facteur de jauge : eta * phi_max^2 <= 0.1
2. Validite perturbative du couplage differentiel : |Delta alpha| <= 0.1
"""

import csv
import numpy as np
from ehk_scci.pulsar_from_field_polynomial import (
    pulsar_decay_from_field_polynomial
)

def run_polynomial_sweep():
    eta_values = np.logspace(-1, 2, 15)
    phi0_values = np.linspace(0.01, 0.5, 15)

    filename = "pulsar_field_sweep_polynomial_results.csv"

    print("=" * 70)
    print("BALAYAGE POLYNOMIAL AVEC FILTRES PERTURBATIFS")
    print("=" * 70)

    fieldnames = [
        "eta",
        "phi0",
        "phi_max",
        "eta_phi2_max",
        "delta_alpha",
        "dP_dt_dipole",
        "dP_dt_total",
        "ratio_dipole_GR",
        "dipole_significance",
        "status"
    ]

    with open(
        filename, mode="w", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for eta in eta_values:
            for phi0 in phi0_values:
                res = pulsar_decay_from_field_polynomial(
                    eta=eta,
                    phi0=phi0,
                    observed_dP_b_uncertainty=1.0e-13
                )

                phi_max = max(
                    abs(res["phi_A"]),
                    abs(res["phi_B"]),
                    abs(phi0)
                )

                eta_phi2_max = eta * phi_max**2
                delta_alpha = abs(res["delta_alpha"])

                if eta_phi2_max > 0.1:
                    status = "hors_domaine_perturbatif"
                elif delta_alpha > 0.1:
                    status = "couplage_non_perturbatif"
                else:
                    if abs(res["dP_dt_dipole"]) >= 1.0e-13:
                        status = "au_dela_du_seuil_methodologique"
                    else:
                        status = "dans_le_seuil_methodologique"

                writer.writerow({
                    "eta": f"{eta:.6e}",
                    "phi0": f"{phi0:.6e}",
                    "phi_max": f"{phi_max:.6e}",
                    "eta_phi2_max": f"{eta_phi2_max:.6e}",
                    "delta_alpha": f"{delta_alpha:.6e}",
                    "dP_dt_dipole": f"{res['dP_dt_dipole']:.6e}",
                    "dP_dt_total": f"{res['dP_dt_total']:.6e}",
                    "ratio_dipole_GR": f"{res['ratio_dipole_GR']:.6e}",
                    "dipole_significance": f"{res['dipole_significance']:.4e}",
                    "status": status
                })

    print(
        f"[*] Balayage polynomial termine. Fichier genere : {filename}"
    )


if __name__ == "__main__":
    run_polynomial_sweep()


def within_perturbative_bounds(
    eta_phi_max_sq: float,
    abs_delta_alpha: float,
) -> bool:
    """Vérifie les deux bornes perturbatives de la paramétrisation polynomiale."""
    return (
        eta_phi_max_sq <= 0.1
        and abs_delta_alpha <= 0.1
    )
