from ehk_scci.pulsar_decay import estimate_dipole_pulsar_decay


def test_zero_delta_alpha_gives_zero_dipole_decay():
    result = estimate_dipole_pulsar_decay(
        m1=1.4,
        m2=1.0,
        P_b_days=0.102,
        eccentricity=0.088,
        alpha_coupling=0.0,
        observed_dP_b_uncertainty=1.0e-13,
    )
    assert abs(result["dP_dt_dipole"]) == 0.0


def test_quadratic_scaling_with_delta_alpha():
    result_small = estimate_dipole_pulsar_decay(
        m1=1.4,
        m2=1.0,
        P_b_days=0.102,
        eccentricity=0.088,
        alpha_coupling=0.02,
        observed_dP_b_uncertainty=1.0e-13,
    )

    result_large = estimate_dipole_pulsar_decay(
        m1=1.4,
        m2=1.0,
        P_b_days=0.102,
        eccentricity=0.088,
        alpha_coupling=0.06,
        observed_dP_b_uncertainty=1.0e-13,
    )

    ratio = abs(result_large["dP_dt_dipole"]) / abs(
        result_small["dP_dt_dipole"]
    )

    assert ratio == 9.0
