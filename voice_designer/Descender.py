from fuckshit import *
from DECTalk import DECTalk
import numpy as np
import Encoder
import math

target_embedding = None
fittest_voice = (None, -math.inf)

def set_target(path: str):
    global target_embedding
    target_embedding = Encoder.encode(path)


def eval_fitness(voice: Voice):
    global target_embedding, fittest_voice
    if target_embedding is None:
        raise "no"

    # panphone = random.choice(PHONEMIC_PANGRAMS)
    panphone = ". ".join(PHONEMIC_PANGRAMS)
    setting = voice_to_string(voice)

    DECTalk.say_to_path(f"{setting} {panphone}","./temp.wav")

    embedding = Encoder.encode("./temp.wav")
    fitness = np.dot(embedding, target_embedding)

    if fitness > fittest_voice[1]:
        fittest_voice = (voice, fitness)

    # print(fitness, voice)
    return fitness


def estimate_grad(voice: Voice) -> Voice:
    global target_embedding
    if target_embedding is None:
        raise "no"

    perturbation = get_perturbed_voice(voice)
    diff = voice_diff(voice, perturbation)

    f_1 = eval_fitness(voice)
    f_2 = eval_fitness(perturbation)

    f = (f_1 - f_2) / 2.0

    grad_est = {}
    for key in voice.keys():
        grad_est[key] = 0 if diff[key] == 0 else f / diff[key]

    return grad_est


def grad_descent(initial: Voice):
    global fittest_voice

    curr_voice = initial.copy()



    while fittest_voice[1] < 0.85:
    # for _ in range(1):

        grad_past = ZERO_VOICE.copy()
        for i in range(5):
            grad = ZERO_VOICE.copy()

            N = 8

            for j in range(N):
                grad_est = estimate_grad(curr_voice)

                # print(grad_est)

                for key in grad_est.keys():
                    grad[key] += grad_est[key] / N


            for key in grad_est.keys():
                curr_voice[key] += int((grad_est[key] + grad_past[key]) * 700)

                if curr_voice[key] < 0:
                    curr_voice[key] = 0

            grad_past = grad.copy()

        curr_voice = fittest_voice[0].copy()

    print(fittest_voice)


# if __name__ == "__main__":
#     set_target("./target.wav")
#     # # eval_fitness(
#     # #     {'AP': 162, 'AS': 33, 'B4': 278, 'B5': 2048, 'BF': -7, 'BR': 49, 'F4': 3859, 'F5': 1916, 'HR': 0, 'HS': 111,
#     # #      'LA': 33, 'LX': 86, 'NF': 0, 'PR': 98, 'QU': 0, 'RI': 20, 'SM': 0, 'SR': 36, 'SX': 0}
#     # # )
#     grad_descent(
#         # get_wendy()
#         {'AP': 128, 'AS': 21, 'B4': 254, 'B5': 2291, 'BF': 33, 'BR': 57, 'F4': 4037, 'F5': 2055, 'HR': 0, 'HS': 116, 'LA': 4, 'LX': 85, 'NF': 0, 'PR': 79, 'QU': 32, 'RI': 56, 'SM': 0, 'SR': 0, 'SX': 0}
#     #     # {
#     #     #     "AP": 112,
#     #     #     "AS": 100,
#     #     #     "B4": 280,
#     #     #     "B5": 330,
#     #     #     "BF": 18,
#     #     #     "BR": 0,
#     #     #     "F4": 3300,
#     #     #     "F5": 3650,
#     #     #     "HR": 18,
#     #     #     "HS": 150,
#     #     #     "LA": 0,
#     #     #     "LX": 0,
#     #     #     "NF": 10,
#     #     #     "PR": 100,
#     #     #     "QU": 40,
#     #     #     "RI": 100,
#     #     #     "SM": 100,
#     #     #     "SR": 25,
#     #     #     "SX": 1
#     #     # }
#     #     # {'AP': 162, 'AS': 33, 'B4': 278, 'B5': 2048, 'BF': 0, 'BR': 49, 'F4': 3859, 'F5': 1916, 'HR': 0, 'HS': 111,
#     #     #  'LA': 33, 'LX': 86, 'NF': 0, 'PR': 98, 'QU': 0, 'RI': 20, 'SM': 0, 'SR': 36, 'SX': 0}
#
#     )
#
#     # v = {'AP': 133, 'AS': 102, 'B4': 0, 'B5': 1654, 'BF': 113, 'BR': 61, 'F4': 3519, 'F5': 1917, 'HR': 140, 'HS': 160, 'LA': 0, 'LX': 50, 'NF': 18, 'PR': 30, 'QU': 21, 'RI': 90, 'SM': 62, 'SR': 177, 'SX': 0}
#     # v = {'AP': 99, 'AS': 26, 'B4': 304, 'B5': 1760, 'BF': 15, 'BR': 53, 'F4': 4041, 'F5': 2035, 'HR': 0, 'HS': 100, 'LA': 6, 'LX': 69, 'NF': 3, 'PR': 39, 'QU': 7, 'RI': 63, 'SM': 0, 'SR': 15, 'SX': 0}
#     # v = {'AP': 128, 'AS': 21, 'B4': 254, 'B5': 2291, 'BF': 33, 'BR': 57, 'F4': 4037, 'F5': 2055, 'HR': 0, 'HS': 116, 'LA': 4, 'LX': 85, 'NF': 0, 'PR': 79, 'QU': 32, 'RI': 56, 'SM': 0, 'SR': 0, 'SX': 0}
#     # DECTalk.say(voice_to_string(v) + "this is the voice that my computer thinks sounds most like paul")