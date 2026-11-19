
"""
Estimation de la décroissance orbitale d'un système binaire
avec une contribution dipolaire phénoménologique attribuée
au secteur de phase SCCI-2026.

Formule dipolaire utilisée :
    Pdot_b_dip = -(2 pi / P_b) * (G M_chirp / c^3) * (Delta alpha)^2 * F_dip(e)

Cette forme est dimensionnellement cohérente et reproduit la
dépendance attendue en (Delta alpha)^2 * (c/v_orb)^2 par rapport
au terme quadrupolaire de la relativité générale.

Attention méthodologique :
- La contribution dipolaire est phénoménologique.
- Elle n'est pas encore dérivée d'une solution auto-consistante
  du champ SCCI-2026.
- Le seuil de couplage dépend du modèle et ne peut pas être
  transposé automatiquement depuis une théorie scalaire-tensorielle.
- Le script ne déclare pas de falsification observationnelle.
"""

import numpy as np


def estimate_dipole_pulsar_decay(
    m1=1.4,
    m2=1.0,
    P_b_days=0.102,
    eccentricity=0.088,
    alpha_coupling=0.005,
    alpha_threshold=6.0e-3,
    observed_dP_b_uncertainty=1.0e-13
):
    """
    Estime la décroissance orbitale quadrupolaire GR et une
    contribution dipolaire phénoménologique.
    """

    # Constantes SI
    G = 6.67430e-11
    c = 2.99792458e8
    M_sun = 1.98847e30

    m1_kg = m1 * M_sun
    m2_kg = m2 * M_sun
    M_total = m1_kg + m2_kg

    P_b = P_b_days * 86400.0
    e = eccentricity

    # Moyen mouvement
    n = 2.0 * np.pi / P_b

    # Demi-grand axe par la troisième loi de Kepler
    a = (G * M_total / n ** 2) ** (1.0 / 3.0)

    # Vitesse orbitale caractéristique
    v_orb = n * a
    beta = v_orb / c

    # Masse de chirp
    chirp_mass = (m1_kg * m2_kg) ** 0.6 / M_total ** 0.2

    # Fonction d'excentricité quadrupolaire
    F_quad = (
        1.0
        + (73.0 / 24.0) * e ** 2
        + (37.0 / 96.0) * e ** 4
    ) / (1.0 - e ** 2) ** 3.5

    # Décroissance quadrupolaire GR
    dP_dt_GR = (
        -(192.0 * np.pi / 5.0)
        * ((2.0 * np.pi * G * chirp_mass) / (c ** 3 * P_b)) ** (5.0 / 3.0)
        * F_quad
    )

    # Fonction d'excentricité dipolaire.
    # Pour e faible, le terme dominant est 1.
    F_dipole = (1.0 + 0.5 * e ** 2) / (1.0 - e ** 2) ** 2.5

    # Différence effective de couplage.
    delta_alpha = alpha_coupling

    # Contribution dipolaire phénoménologique normalisée.
    dP_dt_dipole = (
        -(2.0 * np.pi / P_b)
        * (G * chirp_mass / c ** 3)
        * delta_alpha ** 2
        * F_dipole
    )

    dP_dt_total = dP_dt_GR + dP_dt_dipole

    ratio_dipole_GR = abs(dP_dt_dipole / dP_dt_GR)

    # Estimation du rapport d'échelle attendu.
    scaling_estimate = delta_alpha ** 2 / beta ** 2

    # Comparaison à une incertitude observationnelle représentative.
    dipole_significance = abs(dP_dt_dipole) / observed_dP_b_uncertainty

    # Classification méthodologique, non observationnelle.
    if alpha_coupling > alpha_threshold:
        coupling_status = "au-dela_du_seuil_methodologique"
    else:
        coupling_status = "dans_le_seuil_methodologique"

    if dipole_significance >= 1.0:
        detectability_status = (
            "contribution_dipolaire_superieure_a_l_incertitude"
        )
    else:
        detectability_status = (
            "contribution_dipolaire_inferieure_a_l_incertitude"
        )

    print("=" * 70)
    print("ESTIMATION DE LA DECROISSANCE ORBITALE AVEC TERME DIPOLAIRE")
    print("=" * 70)
    print(f"[*] Systeme : m1 = {m1:.3f} Msun, m2 = {m2:.3f} Msun")
    print(f"[*] Periode orbitale : {P_b_days:.6f} jours")
    print(f"[*] Excentricite : {e:.6f}")
    print(f"[*] Masse de chirp : {chirp_mass / M_sun:.6f} Msun")
    print(f"[*] Demi-grand axe : {a:.6e} m")
    print(f"[*] Vitesse orbitale : {v_orb:.6e} m/s")
    print(f"[*] beta = v_orb / c : {beta:.6e}")
    print(f"[*] Couplage differentiel teste : Delta alpha = {delta_alpha:.6f}")
    print("-" * 70)
    print(f"[*] Pdot_b GR quadrupolaire : {dP_dt_GR:.6e} s/s")
    print(f"[*] Pdot_b dipolaire SCCI   : {dP_dt_dipole:.6e} s/s")
    print(f"[*] Pdot_b total            : {dP_dt_total:.6e} s/s")
    print(f"[*] Ratio dipolaire / GR    : {ratio_dipole_GR:.6e}")
    print(f"[*] Estimation d'echelle (Delta alpha)^2 / beta^2 : {scaling_estimate:.6e}")
    print(f"[*] Incertitude representative : {observed_dP_b_uncertainty:.3e} s/s")
    print(f"[*] Significance dipolaire / incertitude : {dipole_significance:.3e}")
    print("-" * 70)
    print(f"[*] Statut du couplage : {coupling_status}")
    print(f"[*] Statut de detectabilite : {detectability_status}")
    print("-" * 70)
    print(
        "[*] Ce resultat ne constitue pas une falsification "
        "observationnelle de SCCI-2026."
    )
    print(
        "[*] Une contrainte reelle exige la derivation du couplage "
        "dans le modele et la comparaison a des donnees de pulsar "
        "specifiques, avec leurs incertitudes et correlations."
    )
    print("=" * 70)

    return {
        "dP_dt_GR": dP_dt_GR,
        "dP_dt_dipole": dP_dt_dipole,
        "dP_dt_total": dP_dt_total,
        "ratio_dipole_GR": ratio_dipole_GR,
        "scaling_estimate": scaling_estimate,
        "dipole_significance": dipole_significance,
        "coupling_status": coupling_status,
        "detectability_status": detectability_status
    }


if __name__ == "__main__":
    estimate_dipole_pulsar_decay()

