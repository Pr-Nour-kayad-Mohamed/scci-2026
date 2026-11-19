
"""
Génération d'une carte de chaleur de la déviation relative
delta(phi0, r_scale), avec isocontour à |delta| = 10%.

Le contour à 10% représente un critère interne de sensibilité
paramétrique, et non une borne observationnelle EHT établie.
"""

import csv
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm


def generate_shadow_heatmap(
    csv_filename="shadow_sweep_results.csv",
    output_image="shadow_sensitivity_heatmap.png",
    threshold=10.0,
    grid_decimals=6
):
    """
    Génère une carte de chaleur de |delta(phi0, r_scale)|.

    Paramètres
    ----------
    csv_filename : str
        Fichier CSV produit par export_sweep.py.
    output_image : str
        Nom du fichier PNG généré.
    threshold : float
        Seuil méthodologique en pourcentage.
    grid_decimals : int
        Nombre de décimales utilisé pour reconstruire la grille.
    """

    if not os.path.exists(csv_filename):
        raise FileNotFoundError(
            f"Fichier introuvable : {csv_filename}. "
            "Exécutez d'abord export_sweep.py."
        )

    data = {}

    with open(
        csv_filename, mode="r", newline="", encoding="utf-8"
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            phi0 = round(float(row["phi0"]), grid_decimals)
            r_scale = round(float(row["r_scale"]), grid_decimals)
            deviation = abs(float(row["deviation_percent"]))

            data[(phi0, r_scale)] = deviation

    if not data:
        raise ValueError("Aucune donnée valide trouvée dans le CSV.")

    phi0_unique = sorted({key[0] for key in data})
    r_scale_unique = sorted({key[1] for key in data})

    phi0_index = {
        value: index for index, value in enumerate(phi0_unique)
    }
    r_scale_index = {
        value: index for index, value in enumerate(r_scale_unique)
    }

    Z = np.full(
        (len(phi0_unique), len(r_scale_unique)),
        np.nan,
        dtype=float
    )

    for (phi0, r_scale), deviation in data.items():
        i = phi0_index[phi0]
        j = r_scale_index[r_scale]
        Z[i, j] = deviation

    if np.isnan(Z).any():
        missing = int(np.isnan(Z).sum())
        raise ValueError(
            f"Grille incomplète : {missing} valeur(s) manquante(s). "
            "Vérifiez que le CSV contient une grille complète."
        )

    R_grid, Phi_grid = np.meshgrid(
        r_scale_unique,
        phi0_unique
    )

    fig, ax = plt.subplots(
        figsize=(8.5, 6),
        dpi=300
    )

    levels = np.linspace(
        0.0,
        max(threshold, np.nanmax(Z)) * 1.05,
        25
    )

    contourf = ax.contourf(
        R_grid,
        Phi_grid,
        Z,
        levels=levels,
        cmap="viridis",
        extend="max"
    )

    cbar = fig.colorbar(
        contourf,
        ax=ax,
        pad=0.02
    )
    cbar.set_label(
        r"Déviation relative $|\delta|$ (%)",
        fontsize=11
    )

    ax.contour(
        R_grid,
        Phi_grid,
        Z,
        levels=[threshold],
        colors=["#ff3b30"],
        linewidths=2.2,
        linestyles="--"
    )

    ax.contourf(
        R_grid,
        Phi_grid,
        Z,
        levels=[threshold, np.inf],
        colors="none",
        hatches=["///"]
    )

    ax.text(
        0.60, 0.20,
        "Région dans le seuil\n"
        r"$|\delta| \leq 10\%$",
        transform=ax.transAxes,
        color="white",
        fontsize=10,
        fontweight="bold",
        ha="center",
        bbox=dict(
            boxstyle="round,pad=0.3",
            facecolor="black",
            alpha=0.45,
            edgecolor="none"
        )
    )

    ax.text(
        0.72, 0.78,
        "Au-delà du seuil\n"
        r"$|\delta| > 10\%$",
        transform=ax.transAxes,
        color="white",
        fontsize=10,
        fontweight="bold",
        ha="center",
        bbox=dict(
            boxstyle="round,pad=0.3",
            facecolor="#b00020",
            alpha=0.75,
            edgecolor="none"
        )
    )

    ax.set_title(
        "Sensibilité paramétrique du rayon critique de l'ombre\n"
        r"$b_{\mathrm{cr}}(\Phi_0,r_{\mathrm{scale}})$",
        fontsize=12,
        fontweight="bold",
        pad=12
    )

    ax.set_xlabel(
        r"Portée radiale caractéristique $r_{\mathrm{scale}}$ ($M$)",
        fontsize=11
    )
    ax.set_ylabel(
        r"Amplitude centrale du champ de phase $\Phi_0$",
        fontsize=11
    )

    fig.text(
        0.5,
        0.01,
        "Note : le contour à 10 % représente un critère interne de "
        "sensibilité paramétrique, et non une borne observationnelle EHT.",
        ha="center",
        fontsize=8.5,
        style="italic",
        color="#333333"
    )

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(output_image)
    plt.close(fig)

    print(f"[*] Carte de chaleur générée avec succès : {output_image}")
    print(f"[*] Grille : {len(phi0_unique)} x {len(r_scale_unique)}")
    print(f"[*] Seuil méthodologique : |delta| = {threshold:.1f}%")

    return output_image


if __name__ == "__main__":
    generate_shadow_heatmap()

