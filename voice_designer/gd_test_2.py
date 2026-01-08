import matplotlib.pyplot as plt
import numpy as np
import random

def objective_function(p):
    plt.plot(*p, color="tab:red")

    # x, y = p[0:2]
    # d = 80
    #
    # a = get_paul().copy()
    # a["SM"] = max(a["SM"] + int(x * d), 0)
    # a["RI"] = max(a["RI"] + int(y * d), 0)

    # print(voice_to_string(a))

    val = np.dot(p, p)

    print(val, p)

    # val = -Descender.eval_fitness(
    #     a
    # )

    # val = p[0] ** 2 + p[1] ** 2 + random.uniform(-20, 20)
    # val = abs(x) ** (2 * abs(np.sin(y) + np.cos(y))) + y ** 2

    return val

def objective_sample(p):
    n = 1
    r = 0
    for _ in range(n):
        r += objective_function(p) / n

    return r

def get_rand_perturbation(l):
    min = 0.5
    max = 1.0

    delta = np.array([random.uniform(min, max) for _ in range(l)])
    for i in range(l):
        delta[i] *= 1 if random.random() > 5 else -1

    return delta


def estimate_grad_one_sided(p_1):
    plt.scatter(*p_1[0:2])

    delta = get_rand_perturbation(len(p_1))

    p_2 = p_1 + delta

    f_1 = objective_sample(p_1)
    f_2 = objective_sample(p_2)

    plt.plot([p_1[0], p_2[0]], [p_1[1], p_2[1]],  color="tab:blue")

    f = (f_2 - f_1) #/ 2.0

    grad_est = np.array([f / d for d in delta])

    grad_est *= 0.025

    # print(grad_est)
    # exit()



    plt.plot([p_1[0], p_1[0] - grad_est[0]], [p_1[1], p_1[1] - grad_est[1]],  color="tab:orange")

    return grad_est


plt.plot()

# Descender.set_target("./target.wav")
p = np.array([random.uniform(4, 5) for _ in range(5)])

g_past = np.array([0] * 5)
for i in range(13):
    g = estimate_grad_one_sided(p)

    print(g)

    p -= g + g_past / 3

    g_past = g


# theta = np.linspace( 0 , 2 * np.pi , 150 )
#
# for level in range(0, 50, 1):
#
#     a = level / 50 * np.cos( theta )
#     b = level / 50 * np.sin( theta )
#
#     plt.plot( a, b, color="black", marker=",")

plt.show()

