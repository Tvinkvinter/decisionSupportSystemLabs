# Тарусов Артём Сергеевич
# НФИбд-02-20, 1032201667
import numpy as np

matrix = np.array([[8, 11, 9, 3, 5],
                   [3, 8, 3, 0, 6],
                   [9, 11, 4, 12, 6],
                   [11, 6, 11, 11, 1],
                   [8, 4, 0, 7, 7]])

q = [0.0, 0.0, 0.18, 0.01, 0.8]
p = [0.55, 0.0, 0.18, 0.0, 0.26]
answer = {}

lower_price = max([min(x) for x in matrix])
upper_price = min([max(x) for x in np.rot90(matrix)])
if lower_price == upper_price:
    print("седловая точка есть", f"ответ v={lower_price}")
else:
    buff = 0
    for i, pin in zip(matrix, p):
        buff += pin * sum([x * y for x, y in zip(i, q)])
    answer["H(P,Q)"] = buff
    for k, i in enumerate(np.rot90(matrix), 1):
        answer[f"H(P,B{k})"] = sum([x * y for x, y in zip(i, p)])
for i in [(x, y) for x, y in answer.items()]:
    print(f"Выигрыш игрока А в ситуации {i[0]} = {i[1]}")
