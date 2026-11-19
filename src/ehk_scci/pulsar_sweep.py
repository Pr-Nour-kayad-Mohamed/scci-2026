
"""
Balayage du couplage differentiel Delta alpha et exportation CSV.

Le module estime la contribution dipolaire phenomenologique a la
decroissance orbitale et identifie le point de transition par
rapport a une incertitude representative choisie.

Attention methodologique :
- La contribution dipolaire est phenomenologique.
- Elle n'est pas encore derivee d'une solution auto-consistante
  du champ SCCI-2026.
- Le fichier produit une carte de sensibilite, et non une
  contrainte observationnelle EHT ou de pulsar etablie.
"""

import csv
import numpy as np

from ehk_scci.pulsar_decay import estimate_dipole_pulsar_decay


def sweep_pulsar_coupling(
    filename="pulsar_sweep_results.csv",
    alpha_min=1.0e-4,
    alpha_max=1.0e-1,
    alpha_steps=25,
    m1=1.4,
    m2=1.0,
    P_b_days=0.102,
    eccentricity=0.088,
    observed_dP_b_uncertainty=1.0e-13
):
    """
    Balaye Delta alpha sur une échelle logarithmique et exporte
    les résultats dans un fichier CSV.
    """

    alpha_values = np.logspace(
        np.log10(alpha_min),
        np.log10(alpha_max),
        alpha_steps
    )

    fieldnames = [
        "delta_alpha",
        "dP_dt_GR",
        "dP_dt_dipole",
        "dP_dt_total",
        "ratio_dipole_GR",
        "dipole_significance",
        "coupling_status",
        "detectability_status"
    ]

    print("=" * 70)
    print("BALAYAGE DU COUPLAGE DIFFERENTIEL DELTA ALPHA")
    print("=" * 70)
    print(f"[*] Fichier de sortie : {filename}")
    print(f"[*] Nombre de points : {len(alpha_values)}")
    print(
        f"[*] Incertitude representative : "
        f"{observed_dP_b_uncertainty:.3e} s/s"
    )
    print("-" * 70)
    print(
        f"{'Delta alpha':>12} | "
        f"{'Pdot_dip (s/s)':>14} | "
        f"{'Ratio dip/GR':>14} | "
        f"{'Significance':>14} | "
        f"{'Statut':>35}"
    )
    print("-" * 70)

    transition_alpha = None
    previous_significance = None

    with open(
        filename, mode="w", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for delta_alpha in alpha_values:
            result = estimate_dipole_pulsar_decay(
                m1=m1,
                m2=m2,
                P_b_days=P_b_days,
                eccentricity=eccentricity,
                alpha_coupling=delta_alpha,
                observed_dP_b_uncertainty=observed_dP_b_uncertainty
            )

            significance = result["dipole_significance"]

            writer.writerow({
                "delta_alpha": f"{delta_alpha:.8e}",
                "dP_dt_GR": f"{result['dP_dt_GR']:.8e}",
                "dP_dt_dipole": f"{result['dP_dt_dipole']:.8e}",
                "dP_dt_total": f"{result['dP_dt_total']:.8e}",
                "ratio_dipole_GR":
                    f"{result['ratio_dipole_GR']:.8e}",
                "dipole_significance": f"{significance:.8e}",
                "coupling_status": result["coupling_status"],
                "detectability_status":
                    result["detectability_status"]
            })

            if transition_alpha is None:
                if significance >= 1.0:
                    transition_alpha = delta_alpha

            print(
                f"{delta_alpha:>12.4e} | "
                f"{result['dP_dt_dipole']:>14.4e} | "
                f"{result['ratio_dipole_GR']:>14.4e} | "
                f"{significance:>14.4e} | "
                f"{result['detectability_status']:>35}"
            )

    print("-" * 70)

    if transition_alpha is not None:
        print(
            f"[*] Premiere valeur de Delta alpha atteignant ou "
            f"depassant l'incertitude : {transition_alpha:.4e}"
        )
    else:
        print(
            "[*] Aucune valeur de Delta alpha dans la grille "
            "n'atteint l'incertitude choisie."
        )

    print(f"[*] Export termine : {filename}")
    print(
        "[*] Ces resultats decrivent une sensibilite phenomenologique, "
        "et non une contrainte observationnelle etablie."
    )

    return {
        "filename": filename,
        "transition_alpha": transition_alpha,
        "alpha_values": alpha_values
    }


if __name__ == "__main__":
    sweep_pulsar_coupling()

