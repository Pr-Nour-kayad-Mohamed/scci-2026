
"""
Balayage paramétrique et exportation CSV du rayon critique de l'ombre.

Ce module réutilise les fonctions de shadow_calc.py afin de garantir
la cohérence entre le test unitaire et le balayage paramétrique.

Le profil Phi(r) reste un choix exploratoire. Les résultats ne
constituent pas une contrainte observationnelle EHT tant que la
solution du champ n'est pas auto-consistante.
"""

import csv
import numpy as np

from ehk_scci.shadow_calc import shadow_conformal


def export_sweep_to_csv(
    filename="shadow_sweep_results.csv",
    phi0_min=0.01,
    phi0_max=0.50,
    phi0_steps=15,
    r_scale_min=2.0,
    r_scale_max=20.0,
    r_scale_steps=15,
    M=1.0
):
    """
    Effectue un balayage sur (phi0, r_scale) et exporte les résultats.

    Colonnes du CSV :
        phi0
        r_scale
        r_ph
        b_cr
        deviation_percent
    """

    phi0_values = np.linspace(phi0_min, phi0_max, phi0_steps)
    r_scale_values = np.linspace(r_scale_min, r_scale_max, r_scale_steps)

    fieldnames = [
        "phi0",
        "r_scale",
        "r_ph",
        "b_cr",
        "deviation_percent"
    ]

    print("=" * 70)
    print("BALAYAGE PARAMÉTRIQUE : ÉCART DU RAYON CRITIQUE DE L'OMBRE")
    print("=" * 70)
    print(f"[*] Fichier de sortie : {filename}")
    print(f"[*] Nombre de points  : {len(phi0_values) * len(r_scale_values)}")
    print("-" * 70)
    print(
        f"{'phi0':>10} | "
        f"{'r_scale':>10} | "
        f"{'r_ph (M)':>12} | "
        f"{'b_cr (M)':>12} | "
        f"{'deviation (%)':>15}"
    )
    print("-" * 70)

    count_valid = 0
    count_failed = 0

    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for phi0 in phi0_values:
            for r_scale in r_scale_values:
                try:
                    r_ph, b_cr, deviation = shadow_conformal(
                        M=M,
                        phi0=phi0,
                        r_scale=r_scale
                    )

                    deviation_percent = deviation * 100.0

                    writer.writerow({
                        "phi0": f"{phi0:.6f}",
                        "r_scale": f"{r_scale:.6f}",
                        "r_ph": f"{r_ph:.6f}",
                        "b_cr": f"{b_cr:.6f}",
                        "deviation_percent": f"{deviation_percent:.6f}"
                    })

                    count_valid += 1

                    print(
                        f"{phi0:>10.4f} | "
                        f"{r_scale:>10.4f} | "
                        f"{r_ph:>12.6f} | "
                        f"{b_cr:>12.6f} | "
                        f"{deviation_percent:>+14.4f}%"
                    )

                except Exception as error:
                    count_failed += 1
                    print(
                        f"[*] Échec pour phi0={phi0:.4f}, "
                        f"r_scale={r_scale:.4f} : {error}"
                    )

    print("-" * 70)
    print(f"[*] Points valides   : {count_valid}")
    print(f"[*] Points échoués   : {count_failed}")
    print(f"[*] Export terminé   : {filename}")

    return filename


if __name__ == "__main__":
    export_sweep_to_csv()

