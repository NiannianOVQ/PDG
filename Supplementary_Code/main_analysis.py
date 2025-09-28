from numba import jit
import numpy as np

# 收益矩阵使用参数
alpha = 0.2
beta = 0.5
b = 1.6

r = 1  # C-C
s = 0  # C-D
t = b  # D-C
P = 0  # D-D
c_e = 1 + 2 * alpha  # C-E
e_c = 1 + alpha  # E-C
d_e = beta * b  # D-E
e_d = -beta * beta * b  # E-D
e = 1.05  # E-E
m = 6  # Number of historical actions in the reputation mechanism
delta = 0.8  # Reputation Decay Factor
Time = 10000  # Step length
k = 0.1  # Noise parameter


@jit(nopython=True)
def calculate_array():
    # Initial strategy matrix: 0 represents defector, 1 represents cooperator, 2 represents enforcer
    array = np.random.randint(0, 3, size=(100, 100))
    reputation = np.random.randint(0, 3, size=(100, 100, m))  # Randomly initialize the reputation matrix
    # Map the initial strategy to reputation values: 0 - Defect, 0.5 - Cooperate, 1 - Enforce
    reputation = reputation / 2.0

    # Map the values of the initial policy matrix array to the last element of the reputation history.
    for i in range(100):
        for j in range(100):
            reputation[i, j, -1] = array[i, j] / 2.0
    return array, reputation

@jit(nopython=True)
def calculate_reputation(r_now, history, delta, m):
    if m == 1:
        return r_now

    weights = np.linspace(delta, 1, m - 1)  # 使用线性衰减的权重
    r_last = np.sum(history[:-1] * weights) / np.sum(weights)  # 历史声誉加权平均

    # Enhance the incentive effect for continuous cooperation or law enforcement actions
    if m >= 3:
        n = 0
        for i in range(-2, -m - 1, -1):
            if history[i] == 1 or history[i] == 2:
                n += 1
            else:
                break
        if n >= 2:
            r_last += 0.1 * n

    re = 0.5 * r_now + 0.5 * r_last

    return re


@jit(nopython=True)
def ind_payoff(array, reputation, i, j, b, m, delta):
    neighbor = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    total = 0
    for x, y in neighbor:
        nx, ny = (i + x) % 100, (j + y) % 100

        if array[i, j] == 2 and array[nx, ny] == 2:  # If both parties are law enforcement officers
            # Mutual assessment by both parties
            history_i = reputation[i, j]
            history_nx = reputation[nx, ny]

            r_now_i = array[i, j] / 2.0
            r_now_nx = array[nx, ny] / 2.0

            re_i = calculate_reputation(r_now_i, history_i, delta, m)
            re_nx = calculate_reputation(r_now_nx, history_nx, delta, m)

            if re_i <= 0.25:
                action_i = 0
            elif re_i < 0.8:
                action_i = 1
            else:
                action_i = 2

            if re_nx <= 0.25:
                action_nx = 0
            elif re_nx < 0.8:
                action_nx = 1
            else:
                action_nx = 2

            if action_i == 0 and action_nx == 0:
                total += P
            elif action_i == 1 and action_nx == 1:
                total += r
            elif action_i == 2 and action_nx == 2:
                total += e
            elif action_i == 0 and action_nx == 1:
                total += t
            elif action_i == 1 and action_nx == 0:
                total += s
            elif action_i == 0 and action_nx == 2:
                total += d_e
            elif action_i == 1 and action_nx == 2:
                total += c_e
            elif action_i == 2 and action_nx == 0:
                total += e_d
            elif action_i == 2 and action_nx == 1:
                total += e_c

        elif array[i, j] == 2 and array[nx, ny] != 2:
            # Assessing the Neighbor
            history = reputation[nx, ny]
            r_now = array[nx, ny] / 2.0
            re = calculate_reputation(r_now, history, delta, m)
            if re <= 0.25:
                neighbor_action = 0
            elif re < 0.8:
                neighbor_action = 1
            else:
                neighbor_action = 2

            if neighbor_action == 0:
                total += e_d
            if neighbor_action == 1:
                total += e_c
            if neighbor_action == 2:
                total += e

        elif array[i, j] != 2 and array[nx, ny] == 2:
            # The agent was assessed
            history = reputation[i, j]
            r_now = array[i, j] / 2.0
            re = calculate_reputation(r_now, history, delta, m)
            if re <= 0.25:
                agent_action = 0
            elif re < 0.8:
                agent_action = 1
            else:
                agent_action = 2

            if agent_action == 0:
                total += d_e
            if agent_action == 1:
                total += c_e
            if agent_action == 2:
                total += e

        elif array[i, j] != 2 and array[nx, ny] != 2:
            if array[i, j] == 0:
                if array[nx, ny] == 1:
                    total += b
            if array[i, j] == 1:
                if array[nx, ny] == 1:
                    total += r
    pay = total
    return pay


@jit(nopython=True)
def update_strategy(array, reputation, b, m, delta):
    for _ in range(10000):
        x, y = np.random.randint(0, 100), np.random.randint(0, 100)
        neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        dx, dy = neighbors[np.random.randint(0, 4)]
        nx, ny = (x + dx) % 100, (y + dy) % 100

        # Update Strategy
        payoff_i = ind_payoff(array, reputation, x, y, b, m, delta)
        payoff_j = ind_payoff(array, reputation, nx, ny, b, m, delta)
        prob = 1 / (1 + np.exp((payoff_i - payoff_j) / k))
        if np.random.rand() < prob:
            array[x, y] = array[nx, ny]

        # Update Reputation
        history = reputation[x, y]
        r_now = array[x, y] / 2.0
        reputation[x, y] = np.roll(history, -1)
        reputation[x, y][-1] = r_now

    return array, reputation


fc_end, fd_end, fe_end = np.zeros(Time), np.zeros(Time), np.zeros(Time)
for _ in range(10):
    fc, fd, fe = [], [], []
    array, reputation = calculate_array()
    for _ in range(Time):
        count_0, count_1, count_2 = np.sum(array == 0), np.sum(array == 1), np.sum(array == 2)
        count_all = 10000
        fraction_D, fraction_C, fraction_E = count_0 / count_all, count_1 / count_all, count_2 / count_all

        fd.append(fraction_D), fc.append(fraction_C), fe.append(fraction_E)
        array, reputation = update_strategy(array, reputation, b, m, delta)

    fd_end += fd
    fc_end += fc
    fe_end += fe

# Calculate the average of ten runs
f0 = fd_end / 10
f1 = fc_end / 10
f2 = fe_end / 10

f0, f1, f2 = np.array(f0), np.array(f1), np.array(f2)

print("Cooperation rate is", f1)
print("Defection rate is", f0)
print("Enforcement rate is", f2)
