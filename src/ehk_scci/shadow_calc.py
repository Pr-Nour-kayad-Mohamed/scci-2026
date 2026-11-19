
"""
Calcul du rayon critique de l'ombre pour une métrique statique sphérique.

Cas 1 : métrique de Schwarzschild modifiée par un facteur conforme
        dépendant du rayon :
        g_tilde = C(r) * g_Schwarzschild
        avec C(r) = cosh(2 * phi(r)).

Cas 2 : modification non conforme exploratoire de f(r).

Méthode :
Pour une métrique statique sphérique
    ds² = -A(r) dt² + B(r) dr² + r² dOmega²,
la sphère photonique est déterminée par :
    d/dr [ r² / A(r) ] = 0.
Le rayon critique de l'ombre est alors :
    b_cr = r_ph / sqrt(A(r_ph)).

Le cas 2 n'est pas une conséquence établie de SCCI-2026.
Il sert uniquement à illustrer la méthode de falsification.
"""

import numpy as np
from scipy.optimize import minimize_scalar


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


def conformal_factor(r, M, phi0, r_scale):
    """
    Facteur conforme C(r) = cosh(2 phi(r)).
    """
    return np.cosh(2.0 * phi_profile(r, M, phi0, r_scale))


def schwarzschild_metric(r, M):
    """
    Métrique de Schwarzschild en unités G = c = 1.

    f(r) = 1 - 2M/r
    A(r) = f(r)
    B(r) = 1/f(r)
    """
    f = 1.0 - 2.0 * M / r
    A = f
    B = 1.0 / f
    return A, B


def find_photon_sphere(A, r_min, r_max):
    """
    Trouve le rayon de la sphère photonique en minimisant r² / A(r).

    La condition de sphère photonique est :
        d/dr [ r² / A(r) ] = 0.
    """

    def objective(r):
        if r <= r_min:
            return 1e12
        return (r ** 2) / A(r)

    result = minimize_scalar(
        objective,
        bounds=(r_min, r_max),
        method="bounded"
    )

    return result.x


def shadow_conformal(M, phi0, r_scale):
    """
    Cas conforme pur :

        g_tilde = C(r) * g_Schwarzschild

    donc :

        A_tilde(r) = C(r) * f(r)
        B_tilde(r) = C(r) / f(r)

    La sphère photonique est obtenue à partir de A_tilde(r).
    """

    def A_tilde(r):
        A, _ = schwarzschild_metric(r, M)
        C = conformal_factor(r, M, phi0, r_scale)
        return C * A

    r_ph = find_photon_sphere(A_tilde, 2.01 * M, 20.0 * M)

    A_phys = A_tilde(r_ph)
    b_cr = r_ph / np.sqrt(A_phys)

    b_gr = 3.0 * np.sqrt(3.0) * M
    deviation = (b_cr - b_gr) / b_gr

    return r_ph, b_cr, deviation


def shadow_nonconformal(M, phi0, r_scale, coupling=1.0):
    """
    Cas phénoménologique exploratoire :

        f_eff(r) = f(r) * exp(-coupling * phi(r)²)

    Ce choix n'est pas dérivé des équations de champ SCCI-2026.
    Il sert uniquement à illustrer comment une modification non
    conforme de la géométrie peut modifier le rayon de l'ombre.
    """

    def f_eff(r):
        phi = phi_profile(r, M, phi0, r_scale)
        return (1.0 - 2.0 * M / r) * np.exp(-coupling * phi ** 2)

    def A_eff(r):
        return f_eff(r)

    r_ph = find_photon_sphere(A_eff, 2.01 * M, 20.0 * M)

    A_phys = A_eff(r_ph)
    b_cr = r_ph / np.sqrt(A_phys)

    b_gr = 3.0 * np.sqrt(3.0) * M
    deviation = (b_cr - b_gr) / b_gr

    return r_ph, b_cr, deviation


def main():
    M = 1.0
    phi0 = 0.10
    r_scale = 10.0

    print("=" * 70)
    print("TEST DU RAYON CRITIQUE DE L'OMBRE")
    print("=" * 70)

    r_ph, b_cr, deviation = shadow_conformal(M, phi0, r_scale)

    print("\n[1] Métrique conforme pure")
    print(f"    phi_0                 = {phi0}")
    print(f"    r_scale               = {r_scale}")
    print(f"    r_ph                  = {r_ph:.6f} M")
    print(f"    b_cr                  = {b_cr:.6f} M")
    print(f"    b_cr Schwarzschild    = {3.0 * np.sqrt(3.0) * M:.6f} M")
    print(f"    deviation relative    = {deviation:+.3e}")

    r_ph2, b_cr2, deviation2 = shadow_nonconformal(
        M, phi0, r_scale, coupling=1.0
    )

    print("\n[2] Modification non conforme exploratoire")
    print(f"    coupling              = 1.0")
    print(f"    r_ph                  = {r_ph2:.6f} M")
    print(f"    b_cr                  = {b_cr2:.6f} M")
    print(f"    deviation relative    = {deviation2:+.3e}")

    print("\nConclusion méthodologique :")
    print("Le rayon de la sphère photonique est déterminé par la")
    print("métrique physique effective A_eff(r), et non par le seul")
    print("profil du champ Phi(r).")
    print("Une déviation observable exige une solution auto-consistante")
    print("de Phi(r), f(r) et R(r) issue des équations de champ.")


if __name__ == "__main__":
    main()

