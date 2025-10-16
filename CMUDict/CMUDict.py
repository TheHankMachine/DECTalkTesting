import os


DICT_PATH = os.path.join(os.path.dirname(__file__), "cmudict-mod")


CMUDict = {}
for entry in open(DICT_PATH).read().split("\n"):
    [word, pronunciation] = entry.split("  ")
    CMUDict[word] = pronunciation

