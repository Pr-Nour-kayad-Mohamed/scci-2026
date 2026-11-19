# SCCI-2026

Cadre méthodologique, balayages de sensibilité dipolaire et couplage TOV--champ.

## Garde-fou épistémologique

- Les CSV et figures quantifient la sensibilité numérique du pipeline relativement au repère interne de 1e-13 s/s.
- Elles ne constituent pas des contraintes observationnelles établies.
- Pour la paramétrisation polynomiale R(Phi) = 1 + eta * Phi^2, les bornes perturbatives sont eta * Phi_max^2 <= 0.1 et |Delta alpha| <= 0.1.
- L'identification R == Z_A est une hypothèse conditionnelle.
- La dérivation ab initio complète de R, sigma_i, N_Phi et G_dip reste à établir.
- Toute contrainte observationnelle exige des éphémérides réelles, une soustraction cinématique, une comparaison à la relativité générale et une dérivation ab initio contrôlée.

## Reproduction

    make test
    make results
    make metadata
    make manuscript
