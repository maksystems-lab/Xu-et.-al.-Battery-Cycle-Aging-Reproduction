import pyomo.environ as pyo

# Create an optimisation model.
model = pyo.ConcreteModel()

# Define decision variables.
model.x = pyo.Var(domain=pyo.NonNegativeReals)
model.y = pyo.Var(domain=pyo.Binary)

# Define the objective function.
model.objective = pyo.Objective(
    expr=model.x + 3 * model.y,
    sense=pyo.minimize
)

# Define the constraint.
model.constraint = pyo.Constraint(
    expr=model.x >= 4 * (1 - model.y)
)

# Select the HiGHS solver.
solver = pyo.SolverFactory("appsi_highs")

# Check solver availability.
print("Solver available:",
      solver.available(exception_flag=False))

# Solve the mathematical problem.
results = solver.solve(model)

# Display the results.
print("Termination condition:",
      results.solver.termination_condition)

print("x =", pyo.value(model.x))
print("y =", pyo.value(model.y))
print("Objective =", pyo.value(model.objective))