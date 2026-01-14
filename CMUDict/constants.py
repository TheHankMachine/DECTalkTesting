def get_all_combinations(a: list[str], b: list[str]) -> list[str]:
    out = []
    for x in a:
        for y in b:
            out.append(f"{x} {y}")
    return out


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