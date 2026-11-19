from ehk_scci.pulsar_field_sweep_polynomial import within_perturbative_bounds


def test_perturbative_bounds_acceptance_and_rejection():
    assert within_perturbative_bounds(0.05, 0.08) is True
    assert within_perturbative_bounds(0.1, 0.1) is True
    assert within_perturbative_bounds(0.11, 0.05) is False
    assert within_perturbative_bounds(0.05, 0.11) is False
