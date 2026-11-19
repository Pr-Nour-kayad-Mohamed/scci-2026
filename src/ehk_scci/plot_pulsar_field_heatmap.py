
"""
Génération d'une carte de chaleur logarithmique de la contribution
dipolaire |Pdot_b_dip| dans le plan (kappa_R, alpha_star).

L'isocontour à 1e-13 s/s représente un critère interne de
sensibilité paramétrique, et non une contrainte observationnelle
établie pour SCCI-2026.
"""

import csv
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def generate_pulsar_field_heatmap(
    csv_filename="pulsar_field_sweep_results.csv",
    output_image="pulsar_field_sensitivity_heatmap.png",
    threshold_dipole=1.0e-13,
    grid_decimals=6
):
    """
    Génère une carte de chaleur logarithmique de |Pdot_b_dip|.
    """

    if not os.path.exists(csv_filename):
        raise FileNotFoundError(
            f"Fichier introuvable : {csv_filename}. "
            "Exécutez d'abord pulsar_field_sweep.py."
        )

    data = {}

    with open(
        csv_filename, mode="r", newline="", encoding="utf-8"
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            alpha_star = round(
                float(row["alpha_star"]),
                grid_decimals
            )
            kappa_r = round(
                float(row["kappa_R"]),
                grid_decimals
            )
            dipole_val = abs(
                float(row["dP_dt_dipole"])
            )

            data[(alpha_star, kappa_r)] = dipole_val

    if not data:
        raise ValueError("Aucune donnée valide trouvée dans le CSV.")

    alpha_unique = sorted({key[0] for key in data})
    kappa_unique = sorted({key[1] for key in data})

    alpha_index = {
        value: index
        for index, value in enumerate(alpha_unique)
    }

    kappa_index = {
        value: index
        for index, value in enumerate(kappa_unique)
    }

    Z = np.full(
        (len(alpha_unique), len(kappa_unique)),
        np.nan,
        dtype=float
    )

    for (alpha_star, kappa_r), value in data.items():
        i = alpha_index[alpha_star]
        j = kappa_index[kappa_r]
        Z[i, j] = value

    if np.isnan(Z).any():
        missing = int(np.isnan(Z).sum())
        raise ValueError(
            f"Grille incomplète : {missing} valeur(s) manquante(s)."
        )

    K_grid, Alpha_grid = np.meshgrid(
        kappa_unique,
        alpha_unique
    )

    fig, ax = plt.subplots(
        figsize=(8.5, 6),
        dpi=300
    )

    # Normalisation logarithmique de la couleur
    norm = LogNorm(
        vmin=max(Z.min(), 1.0e-18),
        vmax=Z.max()
    )

    contourf = ax.contourf(
        K_grid,
        Alpha_grid,
        Z,
        levels=25,
        cmap="plasma",
        norm=norm,
        extend="both"
    )

    cbar = fig.colorbar(
        contourf,
        ax=ax,
        pad=0.02
    )

    cbar.set_label(
        r"Contribution dipolaire "
        r"$|\dot P_b^{\mathrm{dip}}|$ (s/s)",
        fontsize=11
    )

    # Isocontour au seuil méthodologique
    contour = ax.contour(
        K_grid,
        Alpha_grid,
        Z,
        levels=[threshold_dipole],
        colors=["#00ffff"],
        linewidths=2.2,
        linestyles="--"
    )

    ax.clabel(
        contour,
        inline=True,
        fontsize=9,
        fmt=r"$10^{-13}\ \mathrm{s/s}$"
    )

    # Hachurage de la région au-delà du seuil méthodologique
    ax.contourf(
        K_grid,
        Alpha_grid,
        Z,
        levels=[threshold_dipole, np.inf],
        colors="none",
        hatches=["///"]
    )

    ax.set_title(
        "Sensibilité paramétrique du champ de phase\n"
        r"$|\dot P_b^{\mathrm{dip}}|(\alpha_\star,\kappa_R)$",
        fontsize=12,
        fontweight="bold",
        pad=12
    )

    ax.set_xlabel(
        r"Paramètre de réalisabilité $\kappa_R$",
        fontsize=11
    )

    ax.set_ylabel(
        r"Couplage fondamental $\alpha_\star$",
        fontsize=11
    )

    fig.text(
        0.5,
        0.01,
        "Note : le contour représente un critère interne de "
        "sensibilité paramétrique, et non une contrainte "
        "observationnelle de pulsar établie.",
        ha="center",
        fontsize=8.5,
        style="italic",
        color="#333333"
    )

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(output_image)
    plt.close(fig)

    print(
        f"[*] Carte de chaleur générée avec succès : {output_image}"
    )
    print(
        f"[*] Grille : {len(alpha_unique)} x {len(kappa_unique)}"
    )
    print(
        f"[*] Seuil méthodologique : "
        f"{threshold_dipole:.3e} s/s"
    )

    return output_image


if __name__ == "__main__":
    generate_pulsar_field_heatmap()

