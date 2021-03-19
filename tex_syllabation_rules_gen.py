#!/usr/bin/python3

import sys

output_rules_files = None

ALPHABET = "abcdefghijklmnñopqrstuvwxyz"
VOWELS = "aeiouü"
VOWELS_WITH_ACCENT_MARK = "áéíóú"
ALL_VOWELS = VOWELS + VOWELS_WITH_ACCENT_MARK
CONSONANTS_LHS = "bcdfghjklmnñpqrstvwxyz"
CONSONANTS_LHS_FOR_L = "bcfgkpt"
CONSONANTS_LHS_FOR_R = "bcdfgkpt"
CONSONANTS_RHS = "bcdfgjklmnnñprstvxyz"
DIPTHONGS = [
    "ui", "uí", "iu", "iú", "ai", "ái", "au", "áu", "ei",
    "éi", "eu", "éu", "oi", "ói", "ia", "iá", "ie", "ié",
    "io", "ió", "ua", "uá", "ue", "ué", "uo", "uó",
]
DOUBLE_CONSONANTS = ["rr", "ll", "ch"]

## Implementación basada en 6.2 Reglas de silabación
## (http://elies.rediris.es/elies4/Fon2.htm)

def initialize(filename: str):
    global output_rules_files
    output_rules_files = open(filename, mode="w")
    output_rules_files.write('\n')

def cleanup():
    if output_rules_files != None:
        output_rules_files.close()

def add_rule(rule: str):
    output_rules_files.write(rule + "\n")

def write_rules():
    # 6.2.4.1.1 Secuencias V C V --> V - C V (ataque simple entre vocales).
    # Regla 1: V C V = V - C V (1)
    for v1 in ALL_VOWELS:
        for c in CONSONANTS_LHS:
            for v2 in VOWELS:
                syll = c + v2
                if (syll == "qe"):
                    add_rule(v1 + "3que")
                elif (syll == "qi"):
                    add_rule(v1 + "3qui")
                elif (syll in ["qa", "qo", "qu"]):
                    pass
                else:
                    add_rule(v1 + "1" + syll)
                
        for dc in DOUBLE_CONSONANTS:
            for v2 in VOWELS:
                add_rule(v1 + "1" + dc + v2)

    # Regla 2: V C V = V - C V (2)
    for v1 in VOWELS:
        for c in CONSONANTS_LHS:
            for v2 in VOWELS_WITH_ACCENT_MARK:
                syll = c + v2
                if (syll == "qé"):
                    add_rule(v1 + "3qué")
                elif (syll == "qí"):
                    add_rule(v1 + "3quí")
                elif (syll in ["qá", "qó", "qú"]):
                    pass
                else:
                    add_rule(v1 + "1" + syll)
        
        for dc in DOUBLE_CONSONANTS:
            for v2 in VOWELS_WITH_ACCENT_MARK:
                add_rule(v1 + "1" + dc + v2)
    
    # Regla 3: { y _ } = { - y _ }
    for v1 in ALL_VOWELS:
        for c in CONSONANTS_LHS:
            if (c == "y"): continue
            add_rule(v1 + "1" + c + "y.")
        
        for dc in DOUBLE_CONSONANTS:
            add_rule(v1 + "1" + dc + "y.")

    # Reglas 4 y 5 no están exactamente como en la referencia, pero las considero
    # equivalentes.
    # Regla 4: V O L = V - O L (1) (Obstruyente Líquida)
    for v1 in ALL_VOWELS:
        for c in CONSONANTS_LHS_FOR_L:
            add_rule(v1 + "1" + c + "l")

    # Regla 5: V O L = V - O L (2) (Obstruyente Líquida)
    for v1 in ALL_VOWELS:
        for c in CONSONANTS_LHS_FOR_R:
            add_rule(v1 + "1" + c + "r")

    # Regla 6: C s V --> C - s V
    for v1 in "bcdknlrx":
        for v2 in ALL_VOWELS:
            add_rule(v1 + "1s" + v2)

    # Regla 7: {s, z, x, c, m, ñ, L} C = {s, z, x, c, m, ñ, L} - C
    for c2 in CONSONANTS_LHS:
        for c1 in "szjxcmñ":
            # ch, conflicto en Regla 7
            # cr y cl, conflicto en Regla 4
            if (c1 + c2 in ['ch', 'cr', 'cl']): continue

            add_rule(c1 + "1" + c2)
        
        # lly y chy, conflicto en Regla 3
        if (c2 == "y"): continue

        add_rule("ll1" + c2)
        add_rule("ch1" + c2)

    # Regla 8: {b, k} C = {b, k} - C
    for c1 in CONSONANTS_LHS:
        if (c1 in "rls"): continue

        add_rule("b1" + c1)
        add_rule("k1" + c1)

    # Regla 9: {p, g, f} C = {p, g, f} - C
    for c1 in CONSONANTS_LHS:
        if (c1 in "rl"): continue

        add_rule("p1" + c1)
        add_rule("g1" + c1)
        add_rule("f1" + c1)

    # Regla 10: {d} C = {d} - C
    for c1 in CONSONANTS_LHS:
        if (c1 in "rs"): continue

        add_rule("d1" + c1)

    # Regla 11: {t} C = {t} - C
    for c1 in CONSONANTS_LHS:
        if (c1 in "r"): continue

        add_rule("t1" + c1)

    # Regla 12: {m, n, l, r} C = {m, n, l, r} - C
    for c1 in CONSONANTS_LHS:
        if (c1 in "s"): continue

        add_rule("m1" + c1)
        add_rule("n1" + c1)
        add_rule("l1" + c1)

        # "rr", conflictos en Regla 1 y 2
        if (c1 == "r"): continue

        add_rule("r1" + c1)

    # Regla 13: V V = V - V (1)
    for v1 in "aeoáéíóú":
        add_rule(v1 + "1a")
        add_rule(v1 + "1e")
        add_rule(v1 + "1o")

    # Regla 14: V V = V - V (2)
    for v2 in VOWELS_WITH_ACCENT_MARK:
        add_rule("a1" + v2)
        add_rule("e1" + v2)
        add_rule("o1" + v2)

    # Regla 15: V V = V - V (3)
    add_rule("i1i")
    add_rule("i1í")

    # Regla 16: V V = V - V (4)
    add_rule("í1i")

    # Regla 17: V V = V - V (5)
    add_rule("u1u")
    add_rule("u1ú")

    # Regla 18: V V = V - V (6)
    add_rule("ú1u")

if __name__ == "__main__":
    initialize(sys.argv[1])

    write_rules()

    cleanup()
