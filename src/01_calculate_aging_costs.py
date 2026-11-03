
from pathlib import Path
import math

import pandas as pd
import matplotlib.pyplot as plt

from aging_cost import cycle_stress, segment_marginal_cost



# 1. Project paths


ROOT = Path(__file__).resolve().parents[1]

FIGURE_DIR = ROOT / "results" / "figures"
TABLE_DIR = ROOT / "results" / "tables"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(parents=True, exist_ok=True)



# 2. Published case-study parameters


REPLACEMENT_COST = 3_750_000
DISCHARGE_EFFICIENCY = 0.95
ENERGY_CAPACITY = 12.5


# 3. Verify the stress function


stress_at_80 = cycle_stress(0.80)
reference_stress = 1 / 3000

print("STRESS FUNCTION CHECK")
print("Phi(0.8):", stress_at_80)
print("1/3000:", reference_stress)

print(
    "Relative difference:",
    abs(stress_at_80 - reference_stress)
    / reference_stress * 100,
    "%"
)


# 4. Calculate marginal costs for J = 1 and J = 16

rows = []

for J in [1, 16]:

    for j in range(1, J + 1):

        cost = segment_marginal_cost(
            j=j,
            J=J,
            replacement_cost=REPLACEMENT_COST,
            eta_dis=DISCHARGE_EFFICIENCY,
            energy_capacity=ENERGY_CAPACITY
        )

        rows.append({
            "number_of_segments": J,
            "segment": j,
            "lower_depth": (j - 1) / J,
            "upper_depth": j / J,
            "marginal_cost_usd_per_mwh": cost
        })



results = pd.DataFrame(rows)



# 5. Save the numerical results

output_csv = TABLE_DIR / "marginal_aging_costs.csv"

results.to_csv(output_csv, index=False)

print("\nMARGINAL AGING COST RESULTS")
print(results.to_string(index=False))

print("\nSaved results to:", output_csv)



# 6. Verify selected values independently


expected_values = [
    (1, 1, 165.47368421052633),
    (16, 1, 9.516677544620425),
    (16, 16, 325.1062876190277)
]

print("\nNUMERICAL VERIFICATION")

for J, j, expected in expected_values:

    actual = segment_marginal_cost(
        j, J,
        REPLACEMENT_COST,
        DISCHARGE_EFFICIENCY,
        ENERGY_CAPACITY
    )

    assert math.isclose(
        actual,
        expected,
        rel_tol=1e-9,
        abs_tol=1e-9
    )

    print(
        f"J={J}, segment={j}: "
        f"{actual:.6f} $/MWh - PASS"
    )




fig, ax = plt.subplots(figsize=(10, 6))

for J in [1, 16]:

    subset = results[
        results["number_of_segments"] == J
    ]

    edges = [
        0.0
    ] + subset["upper_depth"].tolist()

    costs = subset[
        "marginal_cost_usd_per_mwh"
    ].tolist()

    # Repeat the final value so the step plot
    # extends to the end of the final segment.
    step_values = costs + [costs[-1]]

    ax.step(
        edges,
        step_values,
        where="post",
        label=f"{J} segment(s)"
    )

ax.set_xlabel("Cycle depth")
ax.set_ylabel("Marginal aging cost ($/MWh)")
ax.set_title("Piecewise-linear battery aging cost")
ax.legend()
ax.grid(True, alpha=0.3)

fig.tight_layout()

plot_path = FIGURE_DIR / "marginal_aging_cost.png"

fig.savefig(plot_path, dpi=200)
plt.close(fig)

print("\nSaved figure to:", plot_path)
print("\nAll mathematical checks passed.")
