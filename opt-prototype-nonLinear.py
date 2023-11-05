# - 目的関数
# max (-3.7e-6x1^2 + 5.16x1^1 + 6.3e5 -5.72e-6x2^2 + 10x2^1 + -9.93e5)

# - 制約条件
# ・x1>=0
# ・x2>=0
# ・x1+x2<=800000

import pyomo.environ as pyo
from pyomo.opt import SolverFactory

from logging import getLogger, Formatter, FileHandler, DEBUG, INFO
formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = FileHandler("./opt-prototype-nonLinear.log")
file_handler.setFormatter(formatter)
logger = getLogger(__name__)
logger.addHandler(file_handler)
logger.setLevel(DEBUG)

model = pyo.ConcreteModel()

# Variables
model.x1 = pyo.Var(within=pyo.NonNegativeReals)
model.x2 = pyo.Var(within=pyo.NonNegativeReals)

# Objective
def obj_rule(model):
    return (-3.7e-6 * model.x1**2 + 5.16 * model.x1 + 6.3e5 - 5.72e-6 * model.x2**2 + 10 * model.x2 - 9.93e5)
model.obj = pyo.Objective(rule=obj_rule, sense=pyo.maximize)

# Constrains
model.con1 = pyo.Constraint(expr=model.x1 >= 0)
model.con2 = pyo.Constraint(expr=model.x2 >= 0)
model.con3 = pyo.Constraint(expr=model.x1 + model.x2 <= 800000)

# Solver
solver = SolverFactory('ipopt')
results = solver.solve(model)

# Result
x1_value = model.x1()
x2_value = model.x2()
objective_value = model.obj()
logger.debug('x1_value - {} - {}'.format(type(x1_value), x1_value))
logger.debug('x2_value - {} - {}'.format(type(x2_value), x2_value))
logger.debug('objective_value - {} - {}'.format(type(objective_value), objective_value))