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

## Generación de diccionario Plover

En base a las herramientas mencionadas en pasos anteriores, creamos el script `plover_spanish_dict_gen.py`. Este se encargará de hacer la traducción de las sílabas de las palabras que le pasemos a su correspondiente acorde, teniendo en cuenta las reglas definidas en [plover_system_spanish_eo_variant](github.com/roskoff/plover_spanish_system_eo_variant).

Aparte de generar el diccionario final, adicionalmente genera dos posibles archivos: uno con fallas de traducción (no consiguió aplicar las reglas del plugin) y otro con colisiones detectadas (debido a las reglas del plugin, más de una palabra coincide con el mismo acorde).

Estos archivos deberán tenerse en cuenta para un análisis posterior y ayudarán a determinar si este script (o los pasos anteriores) contienen casos no considerados, o bien hay que procesar entradas manualmente por la vía de la excepción.

Una ejecución de prueba sobre un corpus de 100 mil palabras mostró un 6.6% de fallas de traducción y un 2,3% de colisiones. La intención es reducir este porcentaje al mínimo por medio de:
- Utilización de corpus con entradas más limpias
- Verificación de reglas de silabació faltanes/erróneas
- Posibles adaptaciones de reglas del plugin del sistema en español

Agrego un pequeño archivo de pruebas denominado `mini_corpus_test.txt` en el repositorio sólo para verificar su funcionamiento.

La salida principal es un diccionario `.json` con los acordes correspondientes de las palabras del corpus. Con la depuración apropiada de estas entradas, el diccionario se puede publicar como parte del diccionario principal del plugin `plover_spanish_system_eo_variant`.

## Testing
```sh
$ python3 tests/syllabation_test.py
$ python3 tests/syllabation_adjustment_test.py
```

## Referencias
- [RLA-ES, Recursos Lingüísticos Abiertos del Español](https://github.com/sbosio/rla-es).
- [Hunspell en github](https://github.com/hunspell)
- [Reglas de silabación](http://elies.rediris.es/elies4/Fon2.htm) y [Reglas de ajuste silábico](http://elies.rediris.es/elies4/Fon3.htm), del trabajo "LA TRANSCRIPCIÓN FONÉTICA AUTOMÁTICA DEL DICCIONARIO ELECTRÓNICO DE FORMAS SIMPLES FLEXIVAS DEL ESPAÑOL: ESTUDIO FONOLÓGICO EN EL LÉXICO", publicado en [Estudios de Lingüística del Español Volumen 4 (1999)](http://elies.rediris.es/elies4/), a pesar de lo añejo, lo descrito en los capítulos que usé fue extremadamente útil y el contenido considero que sigue muy vigente.

## TO-DO
- Aplicar reglas de compactación para generar acordes complementarios, según reglas/sugerencias del plugin `plover_spanish_system_eo_variant`, ejemplo: `"PO/HREU/TEU/KA":"política"`, se puede complementar con una entrada más corta, `"PO/HREU/TEUBG":"política"`
- Considerar la inclusión de reglas de presilabación para palabras excepcionales, ver [6.8. Reglas de presilabación: PRESILAB](http://elies.rediris.es/elies4/Fon8.htm).

## Agradecimientos
- En especial a Santiago Bosio (RLA-ES) por tirarme la punta de ovillo para poder encontrar un enfoque más apropiado.
- `spaniard`, `roalheva`, `defunkydrummer` y `nvdaes` de la comunidad de Plover <3