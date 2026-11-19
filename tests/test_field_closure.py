from ehk_scci.pulsar_from_field_polynomial import (
    realizability_factor_polynomial,
    differential_coupling_polynomial,
)


def test_polynomial_closure_at_zero_field():
    assert realizability_factor_polynomial(0.0, 0.5) == 1.0


def test_zero_field_gives_zero_coupling():
    delta, _, _ = differential_coupling_polynomial(0.0, 0.0, 0.5)
    assert delta == 0.0


def test_polynomial_closure_positive():
    assert realizability_factor_polynomial(0.2, 1.0) == 1.04
