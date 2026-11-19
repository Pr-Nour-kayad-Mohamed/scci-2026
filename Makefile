.RECIPEPREFIX = >

PYTHON ?= python3
export PYTHONPATH := src

.PHONY: all results metadata manuscript test clean

all: results metadata manuscript

results:
>$(PYTHON) src/ehk_scci/pulsar_field_sweep.py
>$(PYTHON) src/ehk_scci/pulsar_field_sweep_polynomial.py
>$(PYTHON) src/ehk_scci/plot_pulsar_field_heatmap.py
>$(PYTHON) src/ehk_scci/plot_pulsar_field_heatmap_polynomial.py
>cp results/pulsar_field_sweep_results.csv data/processed/pulsar_field_sweep_results.csv
>cp results/pulsar_field_sweep_polynomial_results.csv data/processed/pulsar_field_sweep_polynomial_results.csv
>cp results/*.png manuscript/figures/

metadata:
>$(PYTHON) src/ehk_scci/generate_metadata.py

manuscript:
>cd manuscript && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex

test:
>$(PYTHON) -m pytest tests/

clean:
>rm -rf results/*.png results/*.csv data/processed/metadata.json manuscript/main.aux manuscript/main.log manuscript/main.out manuscript/main.pdf
