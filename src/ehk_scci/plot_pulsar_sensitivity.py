
"""
Visualisation de la sensibilité de la contribution dipolaire
à la décroissance orbitale en fonction du couplage différentiel
Delta alpha.

Le seuil horizontal représente une incertitude représentative
choisie pour l'analyse, et non une contrainte observationnelle
établie pour SCCI-2026.
"""

import csv
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_pulsar_sensitivity(
    csv_filename="pulsar_sweep_results.csv",
    output_image="pulsar_dipole_sensitivity.png",
    uncertainty=1.0e-13
):
    """
    Génère une figure log-log de |Pdot_b_dip| en fonction de Delta alpha.

    Paramètres
    ----------
    csv_filename : str
        Fichier CSV produit par pulsar_sweep.py.
    output_image : str
        Nom du fichier PNG généré.
    uncertainty : float
        Incertitude représentative sur Pdot_b, en s/s.
    """

    if not os.path.exists(csv_filename):
        raise FileNotFoundError(
            f"Fichier introuvable : {csv_filename}. "
            "Exécutez d'abord pulsar_sweep.py."
        )

    alpha_values = []
    dipole_values = []
    ratio_values = []

    with open(
        csv_filename, mode="r", newline="", encoding="utf-8"
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            alpha_values.append(
                float(row["delta_alpha"])
            )
            dipole_values.append(
                abs(float(row["dP_dt_dipole"]))
            )
            ratio_values.append(
                float(row["ratio_dipole_GR"])
            )

    if not alpha_values:
        raise ValueError("Aucune donnée valide trouvée dans le CSV.")

    alpha_values = np.array(alpha_values)
    dipole_values = np.array(dipole_values)
    ratio_values = np.array(ratio_values)

    # Première valeur de la grille atteignant ou dépassant le seuil.
    transition_index = np.argmax(dipole_values >= uncertainty)
    transition_alpha = alpha_values[transition_index]
    transition_dipole = dipole_values[transition_index]
    transition_ratio = ratio_values[transition_index]

    fig, ax = plt.subplots(
        figsize=(8.5, 6),
        dpi=300
    )

    ax.loglog(
        alpha_values,
        dipole_values,
        marker="o",
        markersize=5,
        linewidth=2.0,
        color="#1f77b4",
        label=r"Contribution dipolaire $|\dot P_b^{\mathrm{dip}}|$"
    )

    ax.axhline(
        uncertainty,
        color="#ff3b30",
        linestyle="--",
        linewidth=2.0,
        label=(
            r"Incertitude représentative "
            r"$\sigma_{\dot P_b}=10^{-13}\ \mathrm{s/s}$"
        )
    )

    ax.axvline(
        transition_alpha,
        color="#ff9500",
        linestyle=":",
        linewidth=2.0,
        label=(
            r"Transition de grille : "
            r"$\Delta\alpha\approx5{,}62\times10^{-3}$"
        )
    )

    ax.scatter(
        [transition_alpha],
        [transition_dipole],
        color="#ff9500",
        s=70,
        zorder=5,
        label="Point de transition méthodologique"
    )

    ax.annotate(
        r"$|\dot P_b^{\mathrm{dip}}|/\dot P_b^{\mathrm{GR}}"
        r"\approx0{,}108$",
        xy=(transition_alpha, transition_dipole),
        xytext=(transition_alpha * 0.35, transition_dipole * 3.0),
        arrowprops=dict(
            arrowstyle="->",
            color="#444444",
            lw=1.2
        ),
        fontsize=10,
        color="#333333"
    )

    ax.set_title(
        "Sensibilité de la contribution dipolaire\n"
        r"à la décroissance orbitale $|\dot P_b^{\mathrm{dip}}|(\Delta\alpha)$",
        fontsize=12,
        fontweight="bold",
        pad=12
    )

    ax.set_xlabel(
        r"Couplage différentiel $\Delta\alpha$",
        fontsize=11
    )
    ax.set_ylabel(
        r"$|\dot P_b^{\mathrm{dip}}|$ (s/s)",
        fontsize=11
    )

    ax.grid(
        True,
        which="both",
        linestyle="--",
        alpha=0.35
    )

    ax.legend(
        loc="upper left",
        fontsize=9,
        framealpha=0.9
    )

    fig.text(
        0.5,
        0.01,
        "Note : le seuil horizontal est une incertitude représentative "
        "choisie pour l’analyse, et non une contrainte observationnelle "
        "établie pour SCCI-2026.",
        ha="center",
        fontsize=8.5,
        style="italic",
        color="#333333"
    )

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(output_image)
    plt.close(fig)

    print(f"[*] Figure générée avec succès : {output_image}")
    print(f"[*] Nombre de points : {len(alpha_values)}")
    print(
        f"[*] Transition méthodologique : "
        f"Delta alpha = {transition_alpha:.4e}"
    )
    print(
        f"[*] Rapport dipolaire / GR à la transition : "
        f"{transition_ratio:.4e}"
    )
    print(
        "[*] Ce seuil est méthodologique, et non une contrainte "
        "observationnelle établie."
    )

    return output_image


if __name__ == "__main__":
    plot_pulsar_sensitivity()

