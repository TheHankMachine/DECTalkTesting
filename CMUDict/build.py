from constants import *
import re
import os

type Dict = dict[str, str]


IN_DICT_PATH = os.path.join(os.path.dirname(__file__), "cmudict-0.7b")
OUT_DICT_PATH = os.path.join(os.path.dirname(__file__), "cmudict-mod")


def load_dict(path: str) -> Dict:
    dict = {}

    for entry in open(path).read().split("\n"):
        [word, pronunciation] = entry.split("  ")

        dict[word] = pronunciation

    return dict


def save_dict(dict: Dict, path: str):
    open(path, "w").write("\n".join([f"{word}  {pron}" for word, pron in dict.items()]))


def invert_dict(dict: Dict) -> Dict:
    inv = {}

    for [word, pron] in dict.items():
        if pron not in inv:
            inv[pron] = [word]
        else:
            inv[pron] += [word]

    return inv


def convert_entries_to_arphabet(dict: Dict) -> None:
    # do longer phoneme modifications first
    mod_priority = [*PHOENEME_MODIFICATIONS.keys()]
    mod_priority.sort(key=len, reverse=True)

    for word in dict:
        pronunciation = f" {dict[word]} "

        # this specifically uses a different phoneme based on stress (I may be wrong about this)
        pronunciation.replace(" AH0 ", " AX ")

        # remove stress markers
        pronunciation = re.sub(r"[0-9]", "", pronunciation)

        for mod in mod_priority:
            pronunciation = pronunciation.replace(mod, PHOENEME_MODIFICATIONS[mod])

        dict[word] = pronunciation.strip()


def split_entries_into_syllables(dict: Dict):
    inv: Dict = invert_dict(dict)

    for word, pron in dict.items():
        syllables = split_syllables(word, pron, inv)

        dict[word] = " ".join(syllables)


def check_compound(left_pron: str, right_pron: str, word: str, inv: Dict) -> bool:
    left_word_options = inv[left_pron] if left_pron in inv else None        #get_word(left_pron)
    right_word_options = inv[right_pron] if right_pron in inv else None     #get_word(right_pron)

    if not left_word_options: return False
    if not right_word_options: return False

    for left_word in left_word_options:
        if word[:len(left_word)] != left_word:
            continue

        for right_word in right_word_options:
            if left_word + right_word == word:
                return True

    return False


def split_syllables(word: str, pron: str, inv: Dict) -> list[str]:
    # I don't remember how this works
    phonemes = pron.split(" ")
    has_syllabic_phoneme = False

    for i in range(len(phonemes) - 1, -1, -1):

        if not has_syllabic_phoneme:
            if phonemes[i] in SYLLABIC_PHONEMES:
                has_syllabic_phoneme = True

            continue

        left = " ".join(phonemes[:i+1])
        right = " ".join(phonemes[i+1:]).replace(" | ",  " ")

        if check_compound(left, right, re.sub(r"\([0-9]\)", "", word.replace("-", "")), inv):
            phonemes.insert(i + 1, "|")
            has_syllabic_phoneme = left.split(" ")[-1] in SYLLABIC_PHONEMES

        elif phonemes[i] in SYLLABIC_PHONEMES:
            phonemes.insert(i + 1, "|")
            has_syllabic_phoneme = True

        elif phonemes[i] in SYLLABIC_STOPS and i >= 1:
            if " ".join(phonemes[i - 1:i + 1]) not in EXCEPTION_PAIRS: # :/

                phonemes.insert(i, "|")
                has_syllabic_phoneme = False

    return phonemes


if __name__ == "__main__":

    dict: Dict = load_dict(IN_DICT_PATH)
    convert_entries_to_arphabet(dict)
    split_entries_into_syllables(dict)

    save_dict(dict, OUT_DICT_PATH)

