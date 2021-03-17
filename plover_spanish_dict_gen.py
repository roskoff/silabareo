#!/usr/bin/python3

import sys
import time
from utils.hyphenate import Hyphenator
from syllabation_adjustment import SyllableAdjustment
import json

VOWELS = {
    "a": "A",
    "e": "E",
    "i": "EU",
    "o": "O",
    "u": "U",
    "á": "A*",
    "é": "*E",
    "í": "*EU",
    "ó": "O*",
    "ú": "*U"
}

DIPTHONGS = {
    "ui": "*EU",
    "uí": "*EU",
    "iu": "*U",
    "iú": "*U",
    "ai": "AEU",
    "ái": "A*EU",
    "au": "AU",
    "áu": "A*U",
    "ei": "*E",
    "éi": "*E",
    "eu": "*E",
    "éu": "*E",
    "oi": "OEU",
    "ói": "O*EU",
    "ia": "A*",
    "iá": "A*",
    "ie": "*E",
    "ié": "*E",
    "io": "O*",
    "ió": "O*",
    "ua": "A*",
    "uá": "A*",
    "ue": "*E",
    "ué": "*E",
    "uo": "OU",
    "uó": "O*U"
}

CONSONANTS_LHS = {
    "b": "PW",
    "c": "K",
    "d": "TK",
    "f": "TP",
    "g": "TKPW",
    "h": "H",
    "j": "SKWR",
    "k": "K",
    "l": "HR",
    "m": "PH",
    "n": "TPH",
    "ñ": "TPWH",
    "p": "P",
    "q": "K",
    "r": "R",
    "s": "S",
    "t": "T",
    "v": "SR",
    "w": "W",
    "x": "KP",
    "y": "KWR",
    "z": "STKPW"
}

CONSONANTS_LHS_FOR_L = {
    "b": "PW",
    "c": "K",
    "f": "TP",
    "g": "TKPW",
    "k": "K",
    "p": "P",
    "t": "T"
}

CONSONANTS_LHS_FOR_R = {
    "b": "PW",
    "c": "K",
    "d": "TK",
    "f": "TP",
    "g": "TKPW",
    "k": "K",
    "p": "P",
    "t": "T"
}

CONSONANTS_RHS = {
    "b": "B",
    "c": "BG",
    "d": "D",
    "f": "F",
    "g": "G",
    "j": "PBLG",
    "k": "BG",
    "l": "L",
    "m": "PL",
    "n": "PB",
    "p": "P",
    "r": "R",
    "s": "S",
    "t": "T",
    "v": "F",
    "x": "BGS",
    "y": "KWR",
    "z": "Z"
}

ALPHABET = {
    "A": "a",
    "PW": "b",
    "KR": "c",
    "KH": "ch",
    "TK": "d",
    "TP": "f",
    "TKPW": "g",
    "H": "h",
    "SKWR": "j",
    "K": "k",
    "HR": "l",
    "PH": "m",
    "TPH": "n",
    "TPWH": "ñ",
    "P": "p",
    "KW": "q",
    "R": "r",
    "S": "s",
    "T": "t",
    "U": "u",
    "SR": "v",
    "W": "w",
    "KP": "x",
    "KWR": "y",
    "STKPW": "z",
}

def to_plover_stroke(sylls, w):
    debug_stroke = False
    if not sylls:
        return syll_stroke(w)
    else:
        result = ''
        for s in sylls.split('-'):
            # Este es sólo un mensaje de depuración, el caso es muy difícil que
            # se de, pero si ocurre, queremos saber el por qué.
            if (len(s) == 0): print(">>> Curent result: {}, Word: {}".format(result, w))
            result += syll_stroke(s) + ("(" + s + ")" if debug_stroke else '') + "/"

        return result[:-1] # Strip last "/"

# Esta función recibe una sílaba y la asume correcta ("s" tiene sentido como sílaba). Lo
# que pasa dentro es una traducción ad hoc basada en las reglas definidas
# para el plugin plover_system_spanish_eo_variant.
#
# Es probable que no se pueda traducir, en tal caso, se marca como falla "~s~" y se
# continúa con el proceso.
def syll_stroke(s):
    assert len(s) > 0

    try:
        # Vowel alone is a syllable
        if len(s) == 1:
            return VOWELS[s]
    except KeyError:
        pass

    # Dipthong alone could be a syllable
    try:
        if len(s) == 2:
            return DIPTHONGS[s]
    except KeyError:
        pass

    try:
        if len(s) == 2:
            try:
                # consonant_rhs + vowel
                # Excepciones: ce, ci, cé, cí, ge, gi, gé, gí
                if s == "ce":
                    return "SE"
                elif s == "ci":
                    return "SEU"
                elif s == "cé":
                    return "S*E"
                elif s == "cí":
                    return "S*EU"
                elif s == "ge":
                    return "SKWRE"
                elif s == "gi":
                    return "SKWREU"
                elif s == "gé":
                    return "SKWR*E"
                elif s == "gí":
                    return "SKWR*EU"
                else:
                    return CONSONANTS_LHS[s[0]] + VOWELS[s[1]]
            except KeyError:
                # vowel + consonant_lhs
                return VOWELS[s[0]] + CONSONANTS_RHS[s[1]]
    except KeyError:
        pass

    if len(s) == 3:
        try:
            # consonant_rhs + vowel + consonant_lhs
            # Excepciones: ceC, ciC, céC, cíC, geC, giC, géC, gíC (siendo que C
            # pertenece a CONSONANTS_RHS)
            if s[0:2] == "ce":
                return "SE" + CONSONANTS_RHS[s[2]]
            elif s[0:2] == "ci":
                return "SEU" + CONSONANTS_RHS[s[2]]
            elif s[0:2] == "cé":
                return "S*E" + CONSONANTS_RHS[s[2]]
            elif s[0:2] == "cí":
                return "S*EU" + CONSONANTS_RHS[s[2]]
            elif s[0:2] == "ge":
                return "SKWRE" + CONSONANTS_RHS[s[2]]
            elif s[0:2] == "gi":
                return "SKWREU" + CONSONANTS_RHS[s[2]]
            elif s[0:2] == "gé":
                return "SKWR*E" + CONSONANTS_RHS[s[2]]
            elif s[0:2] == "gí":
                return "SKWR*EU" + CONSONANTS_RHS[s[2]]
            else:
                return CONSONANTS_LHS[s[0]] + VOWELS[s[1]] + CONSONANTS_RHS[s[2]]
        except KeyError:
            pass

        # gue, gui, gué, guí
        if s == "gue": return "TKPWE"
        if s == "gui": return "TKPWEU"
        if s == "gué": return "TKPW*E"
        if s == "guí": return "TKPW*EU"

        # que, qui, qué, quí
        if s == "que": return "KE"
        if s == "qui": return "KEU"
        if s == "qué": return "K*E"
        if s == "quí": return "K*EU"

        try:
            # "rr" + vowel
            if s[0:2] == "rr":
                return "WR" + VOWELS[s[2]]
        except KeyError:
            pass

        try:
            # consonant_lhs + dipthong
            # Excepciones: ceV2, céV2, ciV2, geV2, géV2, giV2 (siendo V2 la
            # segunda vocal de uno de los diptongos definidos. Notar que no
            # hay diptongo con "í" como primera vocal)
            if s[0:2] in ["ce", "cé", "ci"]:
                return "S" + DIPTHONGS[s[1:]]
            elif s[0:2] in ["ge", "gé", "gi"]:
                return "SKWR" + DIPTHONGS[s[1:]]
            else:
                return CONSONANTS_LHS[s[0]] + DIPTHONGS[s[1:]]
        except KeyError:
            pass

        try:
            # dipthong + consonant_rhs
            return DIPTHONGS[s[0:2]] + CONSONANTS_RHS[s[2]]
        except KeyError:
            pass

        try:
            # consonant_lhs_for_l + "l" + vowel
            if s[1] == 'l':
                return CONSONANTS_LHS_FOR_L[s[0]] + "HR" + VOWELS[s[2]]
        except KeyError:
            pass

        try:
            # consonant_lhs_for_r + "r" + vowel
            if s[1] == 'r':
                return CONSONANTS_LHS_FOR_R[s[0]] + "R" + VOWELS[s[2]]
        except KeyError:
            pass

        try:
            # "ll" + vowel
            if s[0:2] == "ll":
                return "KWR" + VOWELS[s[2]]
        except KeyError:
            pass

        try:
            if s[0:2] == "ch":
                # "ch" + vowel
                return "KH" + VOWELS[s[2]]
        except KeyError:
            pass

    if len(s) == 4:
        try:
            if s[0:3] == "gue":
                return "TKPWE" + CONSONANTS_RHS[s[3]]

            if s[0:3] == "gui":
                return "TKPWEU" + CONSONANTS_RHS[s[3]]

            if s[0:3] == "gué":
                return "TKPW*E" + CONSONANTS_RHS[s[3]]

            if s[0:3] == "guí":
                return "TKPW*EU" + CONSONANTS_RHS[s[3]]

            if s[0:3] == "que":
                return "KE" + CONSONANTS_RHS[s[3]]

            if s[0:3] == "qui":
                return "KEU" + CONSONANTS_RHS[s[3]]

            if s[0:3] == "qué":
                return "K*E" + CONSONANTS_RHS[s[3]]

            if s[0:3] == "quí":
                return "K*EU" + CONSONANTS_RHS[s[3]]

            if s[0:3] in ["gue", "gui", "gué"]:
                return "TKPW" + DIPTHONGS[s[2:]]

            if s[0:3] in ["que", "qui", "qué"]:
                print("Coloquio" + s)
                return "K" + DIPTHONGS[s[2:]]

        except KeyError:
            pass

        try:
            if s[0:3] in ["gue", "gui", "gué"]:
                return "TKPW" + DIPTHONGS[s[2:]]

            if s[0:3] in ["que", "qui", "qué"]:
                return "K" + DIPTHONGS[s[2:]]

        except KeyError:
            pass

        try:
            if s[0:2] == "rr":
                return "WR" + DIPTHONGS[s[2:]]
        except KeyError:
            pass

        try:
            if s[0:2] == "rr":
                return "WR" + VOWELS[s[2]] + CONSONANTS_RHS[s[3]]
        except KeyError:
            pass

        try:
            # consonant_lhs_for_l + "l" + dipthong
            if s[1] == 'l':
                return CONSONANTS_LHS_FOR_L[s[0]] + "HR" + DIPTHONGS[s[2:]]
        except KeyError:
            pass

        try:
            # consonant_rhs_for_r + "r" + dipthong
            if s[1] == 'r':
                return CONSONANTS_LHS_FOR_R[s[0]] + "R" + DIPTHONGS[s[2:]]
        except KeyError:
            pass

        try:
            # consonant_lhs_for_l + "l" + vowel + consonant_lhs
            if s[1] == 'l':
                return CONSONANTS_LHS_FOR_L[s[0]] + "HR" + VOWELS[s[2]] + CONSONANTS_RHS[s[3]]
        except KeyError:
            pass

        try:
            # consonant_rhs_for_r + "r" + vowel + consonant_lhs
            if s[1] == 'r':
                return CONSONANTS_LHS_FOR_R[s[0]] + "R" + VOWELS[s[2]] + CONSONANTS_RHS[s[3]]
        except KeyError:
            pass

        try:
            # "ll" + dipthong
            if s[0:2] == "ll":
                return "KWR" + DIPTHONGS[s[2:]]
        except KeyError:
            pass

        try:
            # "ll" + vowel + consonant_rhs
            if s[0:2] == "ll":
                return "KWR" + VOWELS[s[2]] + CONSONANTS_RHS[s[3]]
        except KeyError:
            pass

        try:
            if s[0:2] == "ch":
                # "ch" + dipthong
                return "KH" + DIPTHONGS[s[2:]]
        except KeyError:
            pass

        try:
            if s[0:2] == "ch":
                # "ch" + vowel + consonant_rhs
                return "KH" + VOWELS[s[2]] + CONSONANTS_RHS[s[3]]
        except KeyError:
            pass

        try:
            if s[2:] == 'rs':
                # consonant_lhs + vowel + 'rs'
                return CONSONANTS_LHS[s[0]] + VOWELS[s[1]] + 'RS'
        except KeyError:
            pass

        try:
            if s[2:] == 'ns':
                # consonant_lhs + vowel + 'ns'
                return CONSONANTS_LHS[s[0]] + VOWELS[s[1]] + 'PBS'
        except KeyError:
            pass

        try:
            if s[0:2] in ["ce", "cé", "ci"]:
                return "S" + DIPTHONGS[s[1:3]] + CONSONANTS_RHS[s[3]]
            elif s[0:2] in ["ge", "gé", "gi"]:
                return "SKWR" + DIPTHONGS[s[1:3]] + CONSONANTS_RHS[s[3]]
            else:
                return CONSONANTS_LHS[s[0]] + DIPTHONGS[s[1:3]] + CONSONANTS_RHS[s[3]]
        except KeyError:
            pass

    if len(s) == 5:

        try:
            if s[0:2] == "rr":
                return "WR" + DIPTHONGS[s[2:4]] + CONSONANTS_RHS[s[4]]
        except KeyError:
            pass

        try:
            # consonant_rhs_for_l + "l" + vowel + "rs"
            if s[1] == 'l' and s[3:] == "rs":
                return CONSONANTS_LHS_FOR_L[s[0]] + "HR" + VOWELS[s[2]] + "RS"
        except KeyError:
            pass

        try:
            # consonant_lhs_for_l + "l" + vowel + "ns"
            if s[1] == 'l' and s[3:] == "ns":
                return CONSONANTS_LHS_FOR_L[s[0]] + "HR" + VOWELS[s[2]] + "PBS"
        except KeyError:
            pass

        try:
            # consonant_lhs_for_r + "r" + vowel + "rs"
            if s[1] == 'r' and s[3:] == "rs":
                return CONSONANTS_LHS_FOR_R[s[0]] + "R" + VOWELS[s[2]] + "RS"
        except KeyError:
            pass

        try:
            # consonant_lhs_for_r + "r" + vowel + "ns"
            if s[1] == 'r' and s[3:] == "ns":
                return CONSONANTS_LHS_FOR_R[s[0]] + "R" + VOWELS[s[2]] + "PBS"
        except KeyError:
            pass

    return "~" + s + "~"

def count_syllabation_errors(compiled_dict):
    #return dict.keys
    return len([x for x in [*compiled_dict] if "~" in x])

def count_collisions(dict):
    return len([x for x in [*compiled_dict] if "##" in x])

def dump_failed_syllabation(compiled_dict):
    fails = {}
    for k in compiled_dict:
        if ("~" in k):
            fails[k] = compiled_dict[k]

    filename = "fails" + time.strftime("%Y%m%d-%H%M%S") + ".json"
    with open(filename, 'w', encoding='utf8') as fp:
        json.dump(fails, fp, ensure_ascii=False,indent=0, separators=(',', ':'))
        print("Failed json file created: {}".format(filename))

def dump_key_collisions(compiled_dict):
    collisions = {}
    for k in compiled_dict:
        if ("##" in k):
            collisions[k] = compiled_dict[k]

    filename = "collisions" + time.strftime("%Y%m%d-%H%M%S") + ".json"
    with open(filename, 'w', encoding='utf8') as fp:
        json.dump(collisions, fp, ensure_ascii=False,indent=0, separators=(',', ':'))
        print("Collisions json file created: {}".format(filename))

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print ("Modo de empleo: $ python3 plover_spanish_dict_gen.py spanish_corpus.txt new_dict.json")
        exit(0)

    corpus_file_name = sys.argv[1]
    output_dictionary = sys.argv[2]
    #wordlist = ["madrugada", "mamá", "ataja", "coopera", "clama", "cráter" ]
    wordlist = []
    with open(corpus_file_name) as f:
        wordlist = f.read().splitlines()

    with open('build/patterns_for_hyphen.txt', mode='r', encoding='UTF-8') as patternfile:
        patterns = (patternfile.read().replace('UTF-8\nLEFTHYPHENMIN 1\nRIGHTHYPHENMIN 1\n', '').replace('\n', ' '))

    hyphenator = Hyphenator(patterns, "")
    syllable_adjustment = SyllableAdjustment()

    total_words = len(wordlist)
    compiled_dict = {}
    for i in range(0, total_words):
        hyphenated_word = hyphenator.hyphenate_word_as_string(wordlist[i])
        sylls = syllable_adjustment.adjust(hyphenated_word)
        stroke = to_plover_stroke(sylls, wordlist[i])

        # El acorde final se agrega en el diccionario python, pero debido
        # a las reglas del plugin plover_system_spanish_eo_variant, es probable
        # que surjan colisiones entre palabras.
        if (compiled_dict.get(stroke) == None):
            compiled_dict[stroke] = wordlist[i]
        else:
            compiled_dict[stroke + "##" + str(i)] = wordlist[i]

        print ("{:.2f}%".format(i / float(total_words) * 100), end='\r')

    failed_syllabation = count_syllabation_errors(compiled_dict)
    key_collisions = count_collisions(compiled_dict)
    print("Corpus size: {:,}".format(total_words))
    print("Generated entries: {:,}".format(len(compiled_dict)))
    print("Failures on syllabation: {:,}".format(failed_syllabation))
    print("Key collisions: {:,}".format(key_collisions))

    # Tanto las fallas como las colisiones se guardan también en
    # archivos separados para su posterior análisis y búsqueda de
    # su solución.
    if failed_syllabation > 0:
        dump_failed_syllabation(compiled_dict)

    if key_collisions > 0:
        dump_key_collisions(compiled_dict)

    with open(output_dictionary, 'w', encoding='utf8') as fp:
        json.dump(compiled_dict, fp, ensure_ascii=False,indent=0, separators=(',', ':'))
