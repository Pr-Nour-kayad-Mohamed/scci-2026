"""
Calcul de la décroissance orbitale à partir d'un couplage
différentiel polynomial issu de l'action effective minimale :
    R(Phi) = 1 + eta * Phi^2
    alpha(Phi) = (2 * eta * Phi) / (1 + eta * Phi^2)
    Delta alpha = alpha(Phi_B) - alpha(Phi_A)
"""

import numpy as np
from ehk_scci.pulsar_from_field import phi_profile
from ehk_scci.pulsar_decay import estimate_dipole_pulsar_decay

def realizability_factor_polynomial(phi, eta):
    """Facteur de réalisabilité polynomial : R(Phi) = 1 + eta * Phi^2"""
    return 1.0 + eta * (phi ** 2)

def local_coupling_polynomial(phi, eta):
    """Fonction de couplage local alpha(Phi) = d/dPhi ln(R)"""
    r_val = realizability_factor_polynomial(phi, eta)
    if r_val <= 0:
        raise ValueError("Le facteur R(Phi) doit rester strictement positif.")
    return (2.0 * eta * phi) / r_val

def differential_coupling_polynomial(phi_A, phi_B, eta):
    """Couplage différentiel polynomial Delta alpha = alpha_B - alpha_A"""
    alpha_A = local_coupling_polynomial(phi_A, eta)
    alpha_B = local_coupling_polynomial(phi_B, eta)
    delta_alpha = alpha_B - alpha_A
    return delta_alpha, alpha_A, alpha_B

def pulsar_decay_from_field_polynomial(
    M=1.0,
    phi0=0.10,
    r_scale=10.0,
    eta=1.0,
    r_A=3.0,
    r_B=10.0,
    m1=1.4,
    m2=1.0,
    P_b_days=0.102,
    eccentricity=0.088,
    observed_dP_b_uncertainty=1.0e-13
):
    phi_A = phi_profile(r_A, M, phi0, r_scale)
    phi_B = phi_profile(r_B, M, phi0, r_scale)

    delta_alpha, alpha_A, alpha_B = differential_coupling_polynomial(
        phi_A=phi_A, phi_B=phi_B, eta=eta
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
    print("COUPLAGE DIFFERENTIEL POLYNOMIAL (ACTION MINIMALE)")
    print("=" * 70)
    print(f"[*] Phi_A = {phi_A:.6f}")
    print(f"[*] Phi_B = {phi_B:.6f}")
    print(f"[*] eta = {eta:.6f}")
    print(f"[*] alpha_A = {alpha_A:.6e}")
    print(f"[*] alpha_B = {alpha_B:.6e}")
    print(f"[*] Delta alpha = {delta_alpha:.6e}")
    print("-" * 70)

    result["phi_A"] = phi_A
    result["phi_B"] = phi_B
    result["alpha_A"] = alpha_A
    result["alpha_B"] = alpha_B
    result["delta_alpha"] = delta_alpha

    return result

if __name__ == "__main__":
    pulsar_decay_from_field_polynomial()
