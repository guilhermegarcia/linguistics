Linguistics
===========

The python script for segmental extraction does what it says: given a lexicon comprised of words and their respective syllabification patterns, it extracts segmental information and creates a new csv file where you can cheack qualitative and quantitative info on the lexicon.

Example:
```
word, syllabification, part of speech

cabeça, ka-'be-sa, noun
casa, 'ka-za, noun
átomo, 'a-to-mo, noun
caro, 'ka-ro, adj
```

Information in the output (columns):

```
word
pronunciation
nSyls
stressSylNum
stressLoc
nOnsetConsAntepen
nCodaConsAntepen
onsetConsAntepen
codaConsAntepen
VAntepen
nOnsetConsPen
nCodaConsPen
onsetConsPen
codaConsPen
VPen
nOnsetConsFinal
nCodaConsFinal
onsetConsFinal
codaConsFinal
VFinal
nOnsetConsStressed
nCodaConsStressed
onsetConsStressed
codaConsStressed
VStressed
nOnsetConsAlt
nCodaConsAlt
onsetConsAlt
codaConsAlt
VAlt
POS
```

### Helper:

```Cons```: consonant

```V```: vowel

```Alt```: alternative (if final stress, Alt = penult; if penult, final; if antepenult, penult)—this is language-specific.

```n``` or ```Num```: number of segments (quantitative info)

```Syls```: syllables

```Pen```: penult syllable/position

```Antepen```: antepenult syllable/position

```Final```: final syllable/position
