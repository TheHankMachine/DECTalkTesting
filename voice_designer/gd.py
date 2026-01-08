import matplotlib.pyplot as plt

from typing import Callable
import numpy as np
import random

# import Encoder
from DECTalk import DECTalk
from fuckshit import *

type ObjectiveFunction = Callable[[np.typing.ArrayLike], float]



def get_rand_perturbation(l: int) -> np.typing.ArrayLike:
    min = 2
    max = 8

    delta = np.array([random.uniform(min, max) for _ in range(l)])
    for i in range(l):
        delta[i] *= 1 if random.random() > 0.5 else -1

    return delta


def estimate_gradient(p_1: np.typing.ArrayLike, objective_function: ObjectiveFunction, p_0: np.typing.ArrayLike, oversample=1) -> tuple[np.typing.ArrayLike]:
    g = est_grad_helper(p_1, objective_function, p_0)

    if oversample <= 1:
        return g

    g /= oversample
    for _ in range(oversample - 1):
        g += est_grad_helper(p_1, objective_function, p_0) / oversample

    return g


def est_grad_helper(p_1: np.typing.ArrayLike, objective_function: ObjectiveFunction, p_0: np.typing.ArrayLike) -> tuple[np.typing.ArrayLike]:
    delta = get_rand_perturbation(len(p_1))

    p_2 = p_1 + delta

    f_1 = objective_function(p_1)
    f_2 = objective_function(p_2)

    plt.scatter(*p_1[0:2], c="#" + "ee" + f"{int(max(f_1 * 220, 0)):02x}" * 2)
    plt.scatter(*p_2[0:2], c="#" + f"{int(max(f_2 * 220, 0)):02x}" * 2 + "ee")
    # print("#" + f"{int(f_1 * 220):02x}" * 3)

    # plt.scatter(vec_mag(p_0 - p_1), f_1, color="tab:blue")
    # plt.plot([vec_mag(p_0 - p_1), vec_mag(p_0 - p_2)], [f_1, f_2], color="tab:orange", alpha=0.2)

    # print(f_1, p_1)

    f = (f_2 - f_1)

    grad_est = np.array([f / d for d in delta])

    # grad_est /= vec_mag(grad_est) ** 0.5
    grad_est *= 1_200



    # plt.plot([vec_mag(p_0 - p_1), vec_mag(p_0 - p_1 - grad_est)], [f_1, f_1 - vec_mag(grad_est)], color="tab:orange", alpha=0.2)

    # grad_est = np.sqrt(grad_est)

    # plt.scatter(*p_1[0:2], color="black")
    # plt.scatter(*p_2[0:2], color="tab:blue")
    # plt.plot([vec_mag(p_0 - p_1), vec_mag(p_0 - p_2)], [f_1, f_2], color="tab:orange", alpha=0.2)
    # plt.plot([p_1[0], p_1[0] - grad_est[0]], [p_1[1], p_1[1] - grad_est[1]],  color="tab:orange")

    # print("grad est", grad_est)

    return grad_est


def vec_mag(p):
    return np.dot(p, p)


def descent(p_0: np.typing.ArrayLike, objective_function: ObjectiveFunction,
            momentum_len: int = 0, momentum_falloff = 0.33, max_iter: int = 5, gradient_oversampling = 1):
    momentum = []
    p = np.array(p_0)

    plt.plot()

    for i in range(max_iter):
        grad_est = estimate_gradient(p, objective_function, p_0, gradient_oversampling)

        momentum.insert(0, grad_est)
        if len(momentum) > momentum_len + 1:
            momentum.pop()

        for i, m in enumerate(momentum):
            p -= m * (momentum_falloff ** i)

    plt.show()

    return p





# def f(p):
#     return abs(np.sin(np.sqrt(vec_mag(p)) / 25))


# for x in range(1, 80, 10):
#     for y in range(1, 80, 10):
#         p = np.array([x // 1, y // 1])
#
#         v = f(p)
#
#         plt.scatter(*p, c="#" + f"{int(max(v * 220, 0)):02x}" * 2 + "ee")

if __name__ == "__main__":
    descent(np.array([23.0, 25.0, 10.0, 2.0]), f, max_iter = 15, gradient_oversampling = 5)
# plt.show()