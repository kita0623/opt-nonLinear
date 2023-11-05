# https://www.youtube.com/watch?v=0zP74EdmN0w&t=20s
# https://www.youtube.com/watch?v=HgAY2AoomWM
# IP with Piecewise Linear Functions, hard textbook page 492
# https://itslearningakarmazyan.files.wordpress.com/2015/09/operation-research-aplications-and-algorithms.pdf

from pulp import *

count = 0
array = []
while count <= 500:
    array += [25*count]
    count += 1

count2 = 501
while count2 <= 1000:
    array += [(20*count2) + 2500]
    count2 += 1

count3 = 1001
while count3 <= 1500:
    array += [(15*count3) + 7500]
    count3 += 1

#Define sets
GAS = [1,2]
OIL = [1,2]
zset = [1,2,3,4]
yset = [1,2,3]

#prob variable
prob = LpProblem("Piecewise", LpMaximize)

#Decision Variables
amount_vars = LpVariable("amount", 0, None, LpInteger)
gas_vars = LpVariable.dicts("oilgas", [(i, j) for i in OIL for j in GAS], 0, None, LpInteger)
z_vars = LpVariable.dicts("zset", zset, 0)
y_vars = LpVariable.dicts("yset", yset, 0, 1, LpBinary)

#Objective Function
# prob += lpSum(12*gas_vars[(i,1)] for i in OIL) + lpSum(14*gas_vars[(i,2)] for i in OIL) - (z_vars[1]*array[0]) - (z_vars[2]*array[500]) - (z_vars[3]*array[1000]) - (z_vars[4]*array[1500])
prob += lpSum(12*gas_vars[(i,1)] for i in OIL) + lpSum(14*gas_vars[(i,2)] for i in OIL) - (z_vars[1]*0) - (z_vars[2]*12500) - (z_vars[3]*22500) - (z_vars[4]*30000)

#Constraints
prob += lpSum(gas_vars[(1,j)] for j in GAS) <= amount_vars + 500
prob += lpSum(gas_vars[(2,j)] for j in GAS) <= 1000
prob += (0.5*gas_vars[(1,1)]) - (0.5*gas_vars[(2,1)]) >= 0
prob += (0.4*gas_vars[(1,2)]) - (0.6*gas_vars[(2,2)]) >= 0
prob += amount_vars == (0.2*z_vars[1])+(500*z_vars[2])+(1000*z_vars[3])+(1500*z_vars[4])
prob += z_vars[1] == y_vars[1]
prob += z_vars[2] <= y_vars[1] + y_vars[2]
prob += z_vars[3] <= y_vars[2] + y_vars[3]
prob += z_vars[4] <= y_vars[3]
prob += lpSum(y_vars[i] for i in yset) == 1
prob += lpSum(z_vars[k] for k in zset) == 1

#Solve Problem
prob.solve()
for v in prob.variables():
    print(v.name, "=", v.varValue)
    
print("Total Profit:", value(prob.objective))