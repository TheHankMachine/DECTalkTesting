from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np
import os

import DECTalk.DECTalk

CACHE_PATH = os.path.join(os.path.dirname(__file__), "cache")

ENCODER = VoiceEncoder()


def encode(path: str) -> np.array:
    # TODO: cache this since the operation is probably pretty expensive
    # name = os.path.basename(path)
    # cache_path = os.path.join(CACHE_PATH, name)
    #
    # if os.path.exists(cache_path):
    fpath = Path(path)

    wav = preprocess_wav(fpath)

    embed = ENCODER.embed_utterance(wav)

    return embed






#
# DECTalk.DECTalk.say_to_path("[:np]" + PHONEMIC_PANGRAMS[0], "./test1.wav")
# DECTalk.DECTalk.say_to_path("[:np]" + PHONEMIC_PANGRAMS[1], "./test2.wav")
# DECTalk.DECTalk.say_to_path("[:nb]" + PHONEMIC_PANGRAMS[2], "./test3.wav")
#
# embedding_1 = encode("./test1.wav")
# embedding_2 = encode("./test2.wav")
# embedding_3 = encode("./test3.wav")
#
# print(embedding_1)
# print(embedding_2)
# print(embedding_3)
#
#
# print("1, 2", np.dot(embedding_1, embedding_2))
# print("2, 3", np.dot(embedding_2, embedding_3))


# print(
#     encode,
# )



# np.set_printoptions(precision=3, suppress=True)
# print(embed)
