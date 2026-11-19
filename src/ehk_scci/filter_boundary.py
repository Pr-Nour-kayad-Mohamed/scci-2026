
"""
Post-traitement du balayage paramétrique de l'ombre.

Ce script applique un seuil de sensibilité méthodologique,
et non une contrainte observationnelle EHT établie.

Il sépare les configurations selon |delta| <= seuil, puis
identifie les points proches de la frontière choisie.
"""

import csv
import os


def analyze_shadow_boundary(
    filename="shadow_sweep_results.csv",
    output_filename="shadow_boundary_results.csv",
    sensitivity_threshold_percent=10.0,
    boundary_tolerance_percent=0.7
):
    """
    Analyse le CSV produit par export_sweep.py.

    Paramètres
    ----------
    filename : str
        Fichier CSV d'entrée.
    output_filename : str
        Fichier CSV contenant les points proches de la frontière.
    sensitivity_threshold_percent : float
        Seuil méthodologique en pourcentage, par exemple 10.0.
    boundary_tolerance_percent : float
        Tolérance autour du seuil pour identifier la frontière.
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"Fichier introuvable : {filename}. "
            "Exécutez d'abord export_sweep.py."
        )

    threshold = abs(sensitivity_threshold_percent)

    allowed_count = 0
    beyond_threshold_count = 0
    boundary_points = []

    fieldnames = [
        "phi0",
        "r_scale",
        "deviation_percent",
        "distance_to_threshold_percent",
        "classification"
    ]

    with open(
        filename, mode="r", newline="", encoding="utf-8"
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            phi0 = float(row["phi0"])
            r_scale = float(row["r_scale"])
            deviation = float(row["deviation_percent"])

            absolute_deviation = abs(deviation)
            distance = abs(absolute_deviation - threshold)

            if absolute_deviation <= threshold:
                classification = "within_sensitivity_threshold"
                allowed_count += 1
            else:
                classification = "beyond_sensitivity_threshold"
                beyond_threshold_count += 1

            if distance <= boundary_tolerance_percent:
                boundary_points.append({
                    "phi0": phi0,
                    "r_scale": r_scale,
                    "deviation_percent": deviation,
                    "distance_to_threshold_percent": distance,
                    "classification": classification
                })

    total = allowed_count + beyond_threshold_count

    if total == 0:
        raise ValueError("Aucune configuration valide trouvée dans le CSV.")

    allowed_fraction = 100.0 * allowed_count / total
    beyond_fraction = 100.0 * beyond_threshold_count / total

    print("=" * 70)
    print("ANALYSE DE SENSIBILITÉ DU RAYON CRITIQUE DE L'OMBRE")
    print("=" * 70)
    print(f"[*] Fichier d'entrée : {filename}")
    print(
        f"[*] Seuil méthodologique : "
        f"|delta| <= {threshold:.2f}%"
    )
    print(f"[*] Total de configurations : {total}")
    print(
        f"[*] Dans le seuil : {allowed_count} "
        f"({allowed_fraction:.1f}%)"
    )
    print(
        f"[*] Au-delà du seuil : {beyond_threshold_count} "
        f"({beyond_fraction:.1f}%)"
    )

    print("\n[+] Points proches de la frontière méthodologique :")
    print(
        f"{'phi0':>10} | "
        f"{'r_scale':>10} | "
        f"{'delta (%)':>12} | "
        f"{'distance (%)':>14}"
    )
    print("-" * 55)

    boundary_points.sort(
        key=lambda point: point["distance_to_threshold_percent"]
    )

    for point in boundary_points[:20]:
        print(
            f"{point['phi0']:>10.4f} | "
            f"{point['r_scale']:>10.4f} | "
            f"{point['deviation_percent']:>+12.4f}% | "
            f"{point['distance_to_threshold_percent']:>14.4f}"
        )

    with open(
        output_filename, mode="w", newline="", encoding="utf-8"
    ) as output_file:
        writer = csv.DictWriter(
            output_file,
            fieldnames=fieldnames
        )
        writer.writeheader()

        for point in boundary_points:
            writer.writerow({
                "phi0": f"{point['phi0']:.6f}",
                "r_scale": f"{point['r_scale']:.6f}",
                "deviation_percent":
                    f"{point['deviation_percent']:.6f}",
                "distance_to_threshold_percent":
                    f"{point['distance_to_threshold_percent']:.6f}",
                "classification": point["classification"]
            })

    print("-" * 55)
    print(f"[*] Frontière exportée : {output_filename}")
    print(
        "[*] Ces résultats décrivent un seuil méthodologique, "
        "et non une contrainte observationnelle EHT établie."
    )

    return {
        "total": total,
        "allowed_count": allowed_count,
        "beyond_threshold_count": beyond_threshold_count,
        "boundary_points": boundary_points,
        "output_filename": output_filename
    }


if __name__ == "__main__":
    analyze_shadow_boundary()

