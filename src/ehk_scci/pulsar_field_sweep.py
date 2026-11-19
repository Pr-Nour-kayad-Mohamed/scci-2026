
"""
Balayage combine des hyper-parametres de couplage :

    (alpha_star, kappa_R)

pour cartographier la contribution dipolaire a la decroissance
orbitale, a partir d'un profil phenomenologique du champ de phase.

Hypotheses explicites :
    alpha_i = alpha_star * [1 - R(Phi_i)]
    R(Phi) = exp(-kappa_R * Phi^2)
    Delta alpha = alpha_star * [R(Phi_B) - R(Phi_A)]

Ces relations sont des hypotheses de fermeture phenomenologiques.
Elles ne constituent pas une contrainte observationnelle etablie.
"""

import csv
import numpy as np

from ehk_scci.pulsar_from_field import (
    phi_profile,
    realizability_factor,
    differential_coupling,
    estimate_dipole_pulsar_decay
)


def sweep_pulsar_field_coupling(
    filename="pulsar_field_sweep_results.csv",
    alpha_star_min=1.0e-3,
    alpha_star_max=1.0e-1,
    alpha_star_steps=15,
    kappa_R_min=0.1,
    kappa_R_max=10.0,
    kappa_R_steps=15,
    M=1.0,
    phi0=0.10,
    r_scale=10.0,
    r_A=3.0,
    r_B=10.0,
    m1=1.4,
    m2=1.0,
    P_b_days=0.102,
    eccentricity=0.088,
    observed_dP_b_uncertainty=1.0e-13
):
    """
    Balaye (alpha_star, kappa_R) et exporte les resultats.
    """

    alpha_star_values = np.linspace(
        alpha_star_min,
        alpha_star_max,
        alpha_star_steps
    )

    kappa_R_values = np.linspace(
        kappa_R_min,
        kappa_R_max,
        kappa_R_steps
    )

    phi_A = phi_profile(r_A, M, phi0, r_scale)
    phi_B = phi_profile(r_B, M, phi0, r_scale)

    fieldnames = [
        "alpha_star",
        "kappa_R",
        "phi_A",
        "phi_B",
        "R_A",
        "R_B",
        "delta_alpha",
        "dP_dt_GR",
        "dP_dt_dipole",
        "dP_dt_total",
        "ratio_dipole_GR",
        "dipole_significance",
        "detectability_status"
    ]

    print("=" * 70)
    print("BALAYAGE COMBINE : ALPHA_STAR ET KAPPA_R")
    print("=" * 70)
    print(f"[*] Fichier de sortie : {filename}")
    print(f"[*] Nombre de points : "
          f"{len(alpha_star_values) * len(kappa_R_values)}")
    print(f"[*] Phi_A = {phi_A:.6f}")
    print(f"[*] Phi_B = {phi_B:.6f}")
    print(
        f"[*] Incertitude representative : "
        f"{observed_dP_b_uncertainty:.3e} s/s"
    )
    print("-" * 70)
    print(
        f"{'alpha_star':>12} | "
        f"{'kappa_R':>10} | "
        f"{'Delta alpha':>14} | "
        f"{'Pdot_dip (s/s)':>16} | "
        f"{'Significance':>14}"
    )
    print("-" * 70)

    count_valid = 0
    count_failed = 0

    with open(
        filename, mode="w", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for alpha_star in alpha_star_values:
            for kappa_R in kappa_R_values:
                try:
                    delta_alpha, R_A, R_B = differential_coupling(
                        phi_A=phi_A,
                        phi_B=phi_B,
                        alpha_star=alpha_star,
                        kappa_R=kappa_R
                    )

                    result = estimate_dipole_pulsar_decay(
                        m1=m1,
                        m2=m2,
                        P_b_days=P_b_days,
                        eccentricity=eccentricity,
                        alpha_coupling=abs(delta_alpha),
                        observed_dP_b_uncertainty=(
                            observed_dP_b_uncertainty
                        )
                    )

                    writer.writerow({
                        "alpha_star": f"{alpha_star:.8e}",
                        "kappa_R": f"{kappa_R:.8e}",
                        "phi_A": f"{phi_A:.8e}",
                        "phi_B": f"{phi_B:.8e}",
                        "R_A": f"{R_A:.8e}",
                        "R_B": f"{R_B:.8e}",
                        "delta_alpha": f"{delta_alpha:.8e}",
                        "dP_dt_GR":
                            f"{result['dP_dt_GR']:.8e}",
                        "dP_dt_dipole":
                            f"{result['dP_dt_dipole']:.8e}",
                        "dP_dt_total":
                            f"{result['dP_dt_total']:.8e}",
                        "ratio_dipole_GR":
                            f"{result['ratio_dipole_GR']:.8e}",
                        "dipole_significance":
                            f"{result['dipole_significance']:.8e}",
                        "detectability_status":
                            result["detectability_status"]
                    })

                    count_valid += 1

                    print(
                        f"{alpha_star:>12.4e} | "
                        f"{kappa_R:>10.4e} | "
                        f"{delta_alpha:>14.4e} | "
                        f"{abs(result['dP_dt_dipole']):>16.4e} | "
                        f"{result['dipole_significance']:>14.4e}"
                    )

                except Exception as error:
                    count_failed += 1
                    print(
                        f"[*] Echec pour alpha_star={alpha_star:.4e}, "
                        f"kappa_R={kappa_R:.4e} : {error}"
                    )

    print("-" * 70)
    print(f"[*] Points valides : {count_valid}")
    print(f"[*] Points echoues : {count_failed}")
    print(f"[*] Export termine : {filename}")
    print(
        "[*] Ces resultats decrivent une sensibilite phenomenologique, "
        "et non une contrainte observationnelle etablie."
    )

    return {
        "filename": filename,
        "count_valid": count_valid,
        "count_failed": count_failed
    }


if __name__ == "__main__":
    sweep_pulsar_field_coupling()

