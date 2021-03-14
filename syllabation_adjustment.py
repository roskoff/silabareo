#!/usr/bin/python3
import sys
import re
from utils.hyphenate import Hyphenator

## Implementación basada en 6.3 Reglas de ajuste silábico
## (http://elies.rediris.es/elies4/Fon3.htm)
class SyllableAdjustment:

    def adjust(self, syllabed_word):
        # Regla 1 : { _ s - } = { _ es - }
        result = syllabed_word
        result = re.sub('^s-', 'es-', result)

        # Antes de la Regla 2, juntamos "l-l"
        result = re.sub('^l-l', 'll', result)

        # Regla 2 : { _ C - } = { _ Ø - }
        result = re.sub('^[^aáeéiíoóuús]-', '', result)

        # Antes de la Regla 3, debemos juntar "-t-l", de lo
        # contrario, "a-t-le-ta" quedaría "a-le-ta"
        result = re.sub('-t-l', '-tl', result)

        # Antes de la Regla 3, debemos juntar "-l-l"
        result = re.sub('-l-l', '-ll', result)

        # Antes de la Regla 3, debemos juntar "k-y" (whis-k-y), "b-y" (rug-b-y), etc.
        result = re.sub('(-[^aáeéiíoóuúsf])-y$', '\\1y', result)

        # Regla 3: { - C - } = { - Ø - }
        result = re.sub('-[^aáeéiíoóuúsf]-', '-', result)

        # Regla 4: { - C _ } = { - Ø _ }
        result = re.sub('-[^aáeéiíoóuúsfy]$', '', result)

        # Regla 5: { p - p } = { Ø - p }
        result = re.sub('([aáeéiíoóuú])p-p([^-])', '\\1-p\\2', result)

        # Regla 6: { t - t } = { Ø - t }
        result = re.sub('([aáeéiíoóuú])t-t([^-])', '\\1-t\\2', result)

        # Regla 7: { k - k } = { Ø - k }
        result = re.sub('([aáeéiíoóuú])k-k([^-])', '\\1-k\\2', result)
        # Estas reglas derivadas son necesarias ya que no hacemos
        # la transcripción grafema-fonema
        # Regla 7': { c - c } = { Ø - c } (ej. staccato)
        # result = re.sub('([aáeéiíoóuú])c-c([^-])', '\\1-c\\2', result)
        # (Descartamos 7', debido a que no conviene la elición para palabras
        # en español, ej. "elecciones" -> "e-le-cio-nes", "acción" -> "a-ción"

        # Regla 7'': { c - q } = { Ø - q } (ej. becqueriano)
        result = re.sub('([aáeéiíoóuú])c-q([^-])', '\\1-q\\2', result)
        
        # Regla 7''': { c - k } = { Ø - k } (ej. jockey, stocks)
        result = re.sub('([aáeéiíoóuú])c-k([^-s])', '\\1-k\\2', result)

        # Regla 8: { s - s } = { Ø - s }
        result = re.sub('s-s', '-s', result)

        # Regla 8': { z - z } = { Ø - z } (ej. pizza)
        result = re.sub('z-z', '-z', result)

        # Regla 9: { f - f } = { Ø - f }
        result = re.sub('f-f', '-f', result)

        # Regla 10: { - C s } = { - Ø s }
        result = re.sub('-[bdknlr]s', '-s', result)

        # Regla 11: { L } = { l }
        # La omitimos, aparentemente la Regla 4 ya se encarga

        # Resilabación

        # Regla 12: { - f } = { f }
        result = re.sub('-f$', 'f', result)
        result = re.sub('-f-', 'f-', result)

        # Regla 13: { - s } = { s }
        result = re.sub('-s$', 's', result)
        result = re.sub('-s-', 's-', result)

        # Regla 14: { - y _ } = { y _ }
        # La traducción directa sería `result = re.sub('-y$', 'y', result)`,
        # pero por practicidad para poder traducir más adelante un acorde,
        # transformaremos la `y` final como vocal `i`.
        result = re.sub('-y$', 'i', result)
        result = re.sub('y$', 'i', result)

        # Las reglas 15, 16 y 17 no hacen falta implementar debido a que son
        # simplemente para limpieza de los guiones. Por practicidad, ya se
        # fueron elimiminando a medida que se aplicaban las reglas anteriores
        return result

if __name__ == "__main__":
    with open('build/patterns_for_hyphen.txt', mode='r', encoding='UTF-8') as patternfile:
        patterns = (patternfile.read().replace('UTF-8\nLEFTHYPHENMIN 1\nRIGHTHYPHENMIN 1\n', '').replace('\n', ' '))

    hyphenator = Hyphenator(patterns, "")
    syllable_adjustment = SyllableAdjustment()

    if len(sys.argv) > 1:
        for word in sys.argv[1:]:
            hyphenated_word = hyphenator.hyphenate_word_as_string(word)
            print (syllable_adjustment.adjust(hyphenated_word))
    else:
        print ("Modo de empleo: $ python3 syllabation_adjustment.py palabra")

    del patterns