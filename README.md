# Silabar*eo*

Utilitarios para generar palabras separadas en sílabas y construcción de diccionario para Plover.

## Generación de reglas de silabación

```sh
$ python3 tex_syllabation_rules_gen.py build/patterns.txt
$ perl utils/substrings.pl build/patterns.txt build/patterns_for_hyphen.txt UTF-8 1 1
$ python3 utils/hyphenate.py <palabra>
```

- `tex_syllabation_rules_gen.py` implementa las reglas de separación silábica encontradas aquí [6.2 Reglas de silabación](http://elies.rediris.es/elies4/Fon2.htm).
- `utils/substrings.pl` se toma originalmente del [proyecto Hunspell](https://github.com/hunspell/hyphen/blob/master/substrings.pl), este script perl se encarga de convertir los patrones generados por `tex_syllabation_rules_gen.py` (que es un formato `patgen` de TeX) al formato de Libhnj, que entiende `utils/hyphenate.py`.
- `utils/hyphenate.py` es una adaptación del original encontrado en el proyecto [RLA-ES](https://github.com/sbosio/rla-es/blob/master/separacion/hyphenate.py). La clase `Hyphenator` permite separar una palabra de acuerdo a los patrones recibidos.

## Silabación ajustada

Llegado este punto, tenemos una separación en sílabas bastante robusta, pero aún no está completa debido a una serie de casuísticas difícles de implementar en formato de patrones sin que colisionen entre sí. Recurriremos al script `syllabation_adjustment.py` para hacer estos ajustes.

```sh
$ python3 syllabation_adjustment.py <palabra>
```

El resultado debería ser una separación silábica final basada (mayormente) en la fonética de la palabra, por ejemplo: `"postdata" -> "pos-da-ta"`, la `t` es descartada, ya que en la mayoría de los casos no sumaría a la definición de la sílaba para asignarle su acorde en Plover, el cual quedaría así `"POS/TKA/TA": "postdata"`.


## Testing
```sh
$ python3 tests/syllabation_test.py
$ python3 tests/syllabation_adjustment_test.py
```

## Referencias
- [RLA-ES, Recursos Lingüísticos Abiertos del Español](https://github.com/sbosio/rla-es).
- [Hunspell en github](https://github.com/hunspell)
- [Reglas de silabación](http://elies.rediris.es/elies4/Fon2.htm) y [Reglas de ajuste silábico](http://elies.rediris.es/elies4/Fon3.htm), del trabajo "LA TRANSCRIPCIÓN FONÉTICA AUTOMÁTICA DEL DICCIONARIO ELECTRÓNICO DE FORMAS SIMPLES FLEXIVAS DEL ESPAÑOL: ESTUDIO FONOLÓGICO EN EL LÉXICO", publicado en [Estudios de Lingüística del Español Volumen 4 (1999)](http://elies.rediris.es/elies4/), a pesar de lo añejo, lo descrito en los capítulos que usé fue extremadamente útil y el contenido considero que sigue muy vigente.

## Agradecimientos
- En especial a Santiago Bosio (RLA-ES) por tirarme la punta de ovillo para poder encontrar un enfoque más apropiado.
- `spaniard`, `roalheva` y `nvdaes` de la comunidad de Plover <3