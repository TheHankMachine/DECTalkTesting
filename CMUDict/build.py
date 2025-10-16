import re # regex

debug = False

PLOSIVES =      ["P", "B", "T", "D", "K", "G"]
NASALS =        ["M", "N", "NX"]
FRICATIVES =    ["F", "V", "TH", "DH", "S", "Z", "SH", "ZH", "HX"]
AFFRICATIVES =  ["CH", "JH"]
LIQUIDS =       ["L", "R"]
GLIDES =        ["W", "Y"]

SYLLABIC_PHONEMES = [
    "IY", "IH", "EY", "EH", "AE", "AA", "AY", "AW", "AH", "AO", "OW", "OY",
    "UH", "UW", "RR", "YU", "AX", "IX", "IR", "ER", "AR", "OR", "UR"
]

def get_all_combinations(a, b):
    out = []
    for x in a:
        for y in b:
            out.append(f"{x} {y}")
    return out

SYLLABIC_STOPS = [
    *PLOSIVES,
    *NASALS,
    *FRICATIVES,
    *AFFRICATIVES,
    *LIQUIDS,
    # *GLIDES
]

EXCEPTION_PAIRS = [
    "T S", "S T", "S K",
    "S P", "S N", "S M",
    "S F", "SH N", "SH M", "K S",
    *get_all_combinations(FRICATIVES, LIQUIDS),
    *get_all_combinations(PLOSIVES, LIQUIDS),
    *get_all_combinations(["TH", "DH"], LIQUIDS)
]

# map phonemes from the CMU set to the DECTalk set
PHOENEME_MODIFICATIONS = {
    " Y UW ": " YU ",
    " Y ": " YX ",
    " HH ": " HX ",
    " NG ": " NX ",
    " D TH ": " DZ TH ",

    " AX R ": "RR",

    " IY R ": " IR ",
    " IH R ": " IR ",

    " EY R ": " ER ",
    " EH R ": " ER ",
    " AE R ": " ER ",

    " AA R ": " AR ",
    " AH R ": " AR ",

    " OW R ": " OR ",
    " AO R ": " OR ",

    " UH R ": " UR ",
    " UW R ": " UR ",

    " R ": " RX ",

    # " EH R " : " ER ",
    # " AH L ": " EL "
}

# hash map for cmu for faster lookup times (used to check for compound words)
CMU_DICT = {}
CMU_DICT_INV = {}
for entry in open("cmudict-0.7b").read().split("\n"):
    [word, pronunciation] = entry.split("  ")

    pronunciation = " " + pronunciation + " " # padding for easier replacement
    pronunciation.replace(" AH0 ", " AX ") # specifically this uses a different phoneme based on stress (I may be wrong about this)

    pronunciation = re.sub(r"[0-9]", "", pronunciation)  # remove stress markers

    mod_priority = [*PHOENEME_MODIFICATIONS.keys()]
    mod_priority.sort(key=len, reverse=True)

    for mod in mod_priority: # do longer phonemes swaps first
        pronunciation = pronunciation.replace(mod, PHOENEME_MODIFICATIONS[mod])

    pronunciation = pronunciation.strip()

    CMU_DICT[word] = pronunciation

    # collision handling for homophones
    if pronunciation in CMU_DICT_INV:
        CMU_DICT_INV[pronunciation].append(word)
    else:
        CMU_DICT_INV[pronunciation] = [word]


def get_pron(word):
    if word in CMU_DICT:
        return CMU_DICT[word]
    return None

def get_word(pronunciation):
    if pronunciation in CMU_DICT_INV:
        return [re.sub(r"\([0-9]\)", "", word) for word in CMU_DICT_INV[pronunciation]]
    return None

def check_compound(left_pronunciation, right_pronunciation, word):
    left_word_options = get_word(left_pronunciation)
    right_word_options = get_word(right_pronunciation)

    if left_word_options is None: return False
    if right_word_options is None: return False

    for left_word in left_word_options:
        if word[:len(left_word) ] != left_word:
            continue

        for right_word in right_word_options:
            if left_word + right_word == word:
                return True

    return False

def split_syllables(word, pron):
    global debug

    phonemes = pron.split(" ")
    has_syllabic_phoneme = False

    for i in range(len(phonemes) - 1, -1, -1):
        if debug: print(word, phonemes, i, has_syllabic_phoneme, phonemes[i])

        if not has_syllabic_phoneme:
            if phonemes[i] in SYLLABIC_PHONEMES:
                has_syllabic_phoneme = True

            continue

        left = " ".join(phonemes[:i+1])
        right = " ".join(phonemes[i+1:]).replace(" | ",  " ")

        if debug: print(left, " - ", right)

        if check_compound(left, right, re.sub(r"\([0-9]\)", "", word.replace("-", ""))):
            phonemes.insert(i + 1, "|")
            has_syllabic_phoneme = left.split(" ")[-1] in SYLLABIC_PHONEMES

            if debug: print(left, " - ", right, "  FOUND COMPOUND", has_syllabic_phoneme)


        elif phonemes[i] in SYLLABIC_PHONEMES:
            phonemes.insert(i + 1, "|")
            has_syllabic_phoneme = True

        elif phonemes[i] in SYLLABIC_STOPS and i >= 1:
            if " ".join(phonemes[i - 1:i + 1]) not in EXCEPTION_PAIRS: # :/

                phonemes.insert(i, "|")
                has_syllabic_phoneme = False

    return phonemes


if __name__ == "__main__":

    # debug = True
    # split_syllables("SHELTERING", CMU_DICT["SHELTERING"])
    #
    # exit()

    out = []

    keys = [*CMU_DICT.keys()]
    keys.sort()

    for word in keys:
        pronunciation = CMU_DICT[word]

        phonemes = split_syllables(word, pronunciation)

        pronunciation = " ".join(phonemes)

        out.append(f"{word}  {pronunciation}")

    open("cmudict-mod", "w").write("\n".join(out))