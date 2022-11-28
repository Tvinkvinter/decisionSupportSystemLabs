# Тарусов Артём Сергеевич
# НФИбд-02-20, 1032201667
# Вариант 21
#     100 100 200 200 300
# 300  1   2   3   4   8
# 200  4   5   6   2   6
# 100  1   1   3   4   5
# 200  3   3   2   2   7
# 300  5   6   7   8   10

from pulp import *

x = []
for i in range(25):
    x.append(pulp.LpVariable(f"x{i}", lowBound=0))

problem = pulp.LpProblem("0", LpMaximize)
problem += -1 * x[0] - 2 * x[1] - 3 * x[2] - 4 * x[3] - 8 * x[4] \
           - 4 * x[5] - 5 * x[6] - 6 * x[7] - 2 * x[8] - 6 * x[9] \
           - 1 * x[10] - 1 * x[11] - 3 * x[12] - 4 * x[13] - 5 * x[14] \
           - 3 * x[15] - 3 * x[16] - 2 * x[17] - 2 * x[18] - 7 * x[19] \
           - 5 * x[20] - 6 * x[21] - 7 * x[22] - 8 * x[23] - 10 * x[24], "Функция цели"
problem += x[0] + x[1] + x[2] + x[3] + x[4] <= 300  # поставщик
problem += x[5] + x[6] + x[7] + x[8] + x[9] <= 200  # поставщик
problem += x[10] + x[11] + x[12] + x[13] + x[14] <= 100  # поставщик
problem += x[15] + x[16] + x[17] + x[18] + x[19] <= 200  # поставщик
problem += x[20] + x[21] + x[22] + x[23] + x[24] <= 300  # поставщик

problem += x[0] + x[5] + x[10] + x[15] + x[20] == 100  # потребитель
problem += x[1] + x[6] + x[11] + x[16] + x[21] == 100  # потребитель
problem += x[2] + x[7] + x[12] + x[17] + x[22] == 200  # потребитель
problem += x[3] + x[8] + x[13] + x[18] + x[23] == 200  # потребитель
problem += x[4] + x[9] + x[14] + x[19] + x[24] == 300  # потребитель

problem.solve()
print("Result: ")
for variable in problem.variables():
    print(variable.name, " = ", variable.varValue)
print("Стоимость доставки: ")
print(abs(value(problem.objective)))
