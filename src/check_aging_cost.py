from aging_cost import cycle_stress

depths = [0.0, 0.1, 0.3, 0.5, 0.8, 1.0]

for depth in depths:

    result = cycle_stress(depth)

    print(
        f"Depth: {depth:.2f} | "
        f"Stress: {result:.10f}"
    )
