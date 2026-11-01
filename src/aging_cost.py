
import math


def cycle_stress(delta: float) -> float:
    """
    Calculate fractional battery cycle-life loss
    for a specified cycle depth.

    delta: cycle depth expressed as a fraction (0 to 1).
    """

    if not math.isfinite(delta) or not 0.0 <= delta <= 1.0:
        raise ValueError("Delta must be between 0 and 1.")

    return 5.24e-4 * delta ** 2.03


def segment_marginal_cost(
    j: int,
    J: int,
    replacement_cost: float,
    eta_dis: float,
    energy_capacity: float
) -> float:
    """
    Calculate the marginal aging cost of segment j.

    j: segment number, starting at 1.
    J: total number of segments.
    replacement_cost: total battery replacement cost ($).
    eta_dis: discharge efficiency.
    energy_capacity: rated battery energy (MWh).

    Returns: marginal aging cost ($/MWh).
    """

    if not isinstance(j, int) or isinstance(j, bool):
        raise TypeError("Segment number j must be an integer.")

    if not isinstance(J, int) or isinstance(J, bool):
        raise TypeError("Number of segments J must be an integer.")

    if J < 1:
        raise ValueError("J must be at least 1.")

    if not 1 <= j <= J:
        raise ValueError("j must be between 1 and J.")

    if replacement_cost <= 0:
        raise ValueError("Replacement cost must be positive.")

    if not 0 < eta_dis <= 1:
        raise ValueError("Discharge efficiency must be in (0, 1].")

    if energy_capacity <= 0:
        raise ValueError("Energy capacity must be positive.")

    # Calculate segment boundaries.
    delta_lower = (j - 1) / J
    delta_upper = j / J

    # Calculate the degradation increment.
    stress_increment = (
        cycle_stress(delta_upper)
        - cycle_stress(delta_lower)
    )

    # Calculate marginal aging cost.
    cost = (
        replacement_cost
        / (eta_dis * energy_capacity)
        * J
        * stress_increment
    )

    return cost
