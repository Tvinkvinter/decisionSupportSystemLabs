# Тарусов Артём Сергеевич
# НФИбд-02-20, 1032201667
# Вариант 21
#     100 100 200 200 300
# 300  1   2   3   4   8
# 200  4   5   6   2   6
# 100  1   1   3   4   5
# 200  3   3   2   2   7
# 300  5   6   7   8   10
#
# Добавим фиктивного потребителя
#     100 100 200 200 300 200
# 300  1   2   3   4   8   0
# 200  4   5   6   2   6   0
# 100  1   1   3   4   5   0
# 200  3   3   2   2   7   0
# 300  5   6   7   8   10  0

from pulp import *

x = []
for i in range(30):
    x.append(pulp.LpVariable(f"x{i}", lowBound=0))

problem = pulp.LpProblem("0", LpMaximize)
problem += -1 * x[0] - 2 * x[1] - 3 * x[2] - 4 * x[3] - 8 * x[4] - 0 * x[5] \
           - 4 * x[6] - 5 * x[7] - 6 * x[8] - 2 * x[9] - 6 * x[10] - 0 * x[11] \
           - 1 * x[12] - 1 * x[13] - 3 * x[14] - 4 * x[15] - 5 * x[16] - 0 * x[17] \
           - 3 * x[18] - 3 * x[19] - 2 * x[20] - 2 * x[21] - 7 * x[22] - 0 * x[23] \
           - 5 * x[24] - 6 * x[25] - 7 * x[26] - 8 * x[27] - 10 * x[28] - 0 * x[29], "Функция цели"
problem += x[0] + x[1] + x[2] + x[3] + x[4] + x[5] <= 300  # поставщик
problem += x[6] + x[7] + x[8] + x[9] + x[10] + x[11] <= 200  # поставщик
problem += x[12] + x[13] + x[14] + x[15] + x[16] + x[17] <= 100  # поставщик
problem += x[18] + x[19] + x[20] + x[21] + x[22] + x[23] <= 200  # поставщик
problem += x[24] + x[25] + x[26] + x[27] + x[28] + x[29] <= 300  # поставщик

problem += x[0] + x[6] + x[12] + x[18] + x[24] == 100  # потребитель
problem += x[1] + x[7] + x[13] + x[19] + x[25] == 100  # потребитель
problem += x[2] + x[8] + x[14] + x[20] + x[26] == 200  # потребитель
problem += x[3] + x[9] + x[15] + x[21] + x[27] == 200  # потребитель
problem += x[4] + x[10] + x[16] + x[22] + x[28] == 300  # потребитель
problem += x[5] + x[11] + x[17] + x[23] + x[29] == 200  # потребитель

problem.solve()
print("Result: ")
for variable in problem.variables():
    print(variable.name, " = ", variable.varValue)
print("Стоимость доставки: ")
print(abs(value(problem.objective)))
