
"""
Calcul de la décroissance orbitale à partir d'un couplage
différentiel dérivé d'un profil phénoménologique du champ
de phase SCCI-2026.

Hypothèses explicites :
    alpha_i = alpha_star * [1 - R(Phi_i)]
    R(Phi) = exp(-kappa_R * Phi^2)
    Delta alpha = alpha_star * [R(Phi_B) - R(Phi_A)]

Ces relations sont des hypothèses de couplage phénoménologiques.
Elles ne sont pas encore dérivées de la variation complète de
l'action SCCI-2026.
"""

import numpy as np

from ehk_scci.pulsar_decay import estimate_dipole_pulsar_decay


def phi_profile(r, M, phi0, r_scale):
    """
    Profil exploratoire du champ de phase.

    phi(r) = phi0 pour r <= 2M
    phi(r) = phi0 * exp(-(r - 2M) / r_scale) pour r > 2M
    """
    r_h = 2.0 * M

    if r <= r_h:
        return phi0

    return phi0 * np.exp(-(r - r_h) / r_scale)


def realizability_factor(phi, kappa_R):
    """
    Hypothèse phénoménologique de réalisabilité :

        R(Phi) = exp(-kappa_R * Phi^2)

    avec 0 < R <= 1.
    """
    return np.exp(-kappa_R * phi ** 2)


def differential_coupling(
    phi_A,
    phi_B,
    alpha_star,
    kappa_R
):
    """
    Couplage différentiel phénoménologique :

        Delta alpha = alpha_star * [R(Phi_B) - R(Phi_A)]

    La limite R_A = R_B donne Delta alpha = 0.
    """

    R_A = realizability_factor(phi_A, kappa_R)
    R_B = realizability_factor(phi_B, kappa_R)

    delta_alpha = alpha_star * (R_B - R_A)

    return delta_alpha, R_A, R_B


def pulsar_decay_from_field(
    M=1.0,
    phi0=0.10,
    r_scale=10.0,
    alpha_star=0.05,
    kappa_R=1.0,
    r_A=3.0,
    r_B=10.0,
    m1=1.4,
    m2=1.0,
    P_b_days=0.102,
    eccentricity=0.088,
    observed_dP_b_uncertainty=1.0e-13
):
    """
    Calcule Delta alpha à partir du champ de phase, puis estime
    la décroissance orbitale dipolaire.
    """

    phi_A = phi_profile(r_A, M, phi0, r_scale)
    phi_B = phi_profile(r_B, M, phi0, r_scale)

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
        observed_dP_b_uncertainty=observed_dP_b_uncertainty
    )

    print("=" * 70)
    print("COUPLAGE DIFFERENTIEL ISSU DU CHAMP DE PHASE")
    print("=" * 70)
    print(f"[*] Phi_A = {phi_A:.6f}")
    print(f"[*] Phi_B = {phi_B:.6f}")
    print(f"[*] R_A = {R_A:.6f}")
    print(f"[*] R_B = {R_B:.6f}")
    print(f"[*] alpha_star = {alpha_star:.6f}")
    print(f"[*] kappa_R = {kappa_R:.6f}")
    print(f"[*] Delta alpha = {delta_alpha:.6e}")
    print("-" * 70)
    print(
        "[*] Ces relations sont des hypotheses phenomenologiques, "
        "non des consequences demontrees des equations de champ."
    )
    print("=" * 70)

    result["phi_A"] = phi_A
    result["phi_B"] = phi_B
    result["R_A"] = R_A
    result["R_B"] = R_B
    result["delta_alpha"] = delta_alpha

    return result


if __name__ == "__main__":
    pulsar_decay_from_field()

