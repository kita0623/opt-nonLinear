import pandas as pd
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 100)

from pulp import *

from logging import getLogger, Formatter, FileHandler, DEBUG, INFO
formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = FileHandler("./opt-prototype-piesewiselinear.log")
file_handler.setFormatter(formatter)
logger = getLogger(__name__)
logger.addHandler(file_handler)
logger.setLevel(DEBUG)

# LpProblem
prob = LpProblem("test", LpMaximize)

# Variable
Z_SKU_PT = {}
for sku in ["sku1","sku2"]:
    Z_SKU_PT[sku] = {}
    for pt in ["pt0","pt1","pt2"]:
        Z_SKU_PT[sku][pt] = LpVariable(f'Z_{sku}_{pt}', lowBound=0, upBound=None, cat=LpContinuous)

Y_SKU_BT = {}
for sku in ["sku1","sku2"]:
    Y_SKU_BT[sku] = {}
    for bt in ["bt0","bt1"]:
        Y_SKU_BT[sku][bt] = LpVariable(f'Y_{sku}_{bt}', lowBound=0, upBound=1, cat=LpBinary)

# Objective Function
prob += 0*Z_SKU_PT["sku1"]["pt0"] + 3000*Z_SKU_PT["sku1"]["pt1"] + 3500*Z_SKU_PT["sku1"]["pt2"] + 0*Z_SKU_PT["sku2"]["pt0"] + 2500*Z_SKU_PT["sku2"]["pt1"] + 4000*Z_SKU_PT["sku2"]["pt2"]

# Constraints
prob += 0*Z_SKU_PT["sku1"]["pt0"] + 1000*Z_SKU_PT["sku1"]["pt1"] + 2000*Z_SKU_PT["sku1"]["pt2"] + 0*Z_SKU_PT["sku2"]["pt0"] + 1000*Z_SKU_PT["sku2"]["pt1"] + 2000*Z_SKU_PT["sku2"]["pt2"] <= 2500
# prob += 0*Z_SKU_PT["sku1"]["pt0"] + 1000*Z_SKU_PT["sku1"]["pt1"] + 2000*Z_SKU_PT["sku1"]["pt2"] <= 2500
# prob += 0*Z_SKU_PT["sku2"]["pt0"] + 1000*Z_SKU_PT["sku2"]["pt1"] + 2000*Z_SKU_PT["sku2"]["pt2"] <= 2500

prob += Z_SKU_PT["sku1"]["pt0"] <= Y_SKU_BT["sku1"]["bt0"]
prob += Z_SKU_PT["sku1"]["pt1"] <= Y_SKU_BT["sku1"]["bt0"] + Y_SKU_BT["sku1"]["bt1"]
prob += Z_SKU_PT["sku1"]["pt2"] <= Y_SKU_BT["sku1"]["bt1"]
prob += lpSum(Z_SKU_PT["sku1"][pt] for pt in ["pt0","pt1","pt2"]) == 1
prob += lpSum(Y_SKU_BT["sku1"][pt] for pt in ["bt0","bt1"]) == 1

prob += Z_SKU_PT["sku2"]["pt0"] <= Y_SKU_BT["sku2"]["bt0"]
prob += Z_SKU_PT["sku2"]["pt1"] <= Y_SKU_BT["sku2"]["bt0"] + Y_SKU_BT["sku2"]["bt1"]
prob += Z_SKU_PT["sku2"]["pt2"] <= Y_SKU_BT["sku2"]["bt1"]
prob += lpSum(Z_SKU_PT["sku2"][pt] for pt in ["pt0","pt1","pt2"]) == 1
prob += lpSum(Y_SKU_BT["sku2"][pt] for pt in ["bt0","bt1"]) == 1

# Solve Problem
status = prob.solve()
print('Status:', LpStatus[status])

# Result
obj_value = prob.objective.value()
print('obj_value', f'{obj_value:,.0f}')
logger.debug('obj_value - {} - {}'.format(type(obj_value), obj_value))
for v in prob.variables():
    print(v.name, "=", v.varValue)
    logger.debug('v.name - {} - {}'.format(type(v.name), v.name))
    logger.debug('v.varValue - {} - {}'.format(type(v.varValue), v.varValue))