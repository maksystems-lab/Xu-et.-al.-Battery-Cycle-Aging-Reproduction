import pyomo.environ as pyo


model = pyo.ConcreteModel()

#  decision variables.
model.x = pyo.Var(domain=pyo.NonNegativeReals)
model.y = pyo.Var(domain=pyo.Binary)

#  the objective function.
model.objective = pyo.Objective(
    expr=model.x + 3 * model.y,
    sense=pyo.minimize
)

#  the constraint.
model.constraint = pyo.Constraint(
    expr=model.x >= 4 * (1 - model.y)
)

#   HiGHS solver.
solver = pyo.SolverFactory("appsi_highs")

#  solver availability.
print("Solver available:",
      solver.available(exception_flag=False))

# Solve .
results = solver.solve(model)

#  results.
print("Termination condition:",
      results.solver.termination_condition)

print("x =", pyo.value(model.x))
print("y =", pyo.value(model.y))
print("Objective =", pyo.value(model.objective))

