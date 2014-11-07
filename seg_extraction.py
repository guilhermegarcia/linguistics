''' 
This script was developed for the lexicon analysis in Garcia (2014)
Input: a list of words *with* proper syllabification (-) and stress mark (')
Output: segmental info for each word (qualitative and quantitative)

Guilherme D. Garcia
'''

import csv
import re

''' 
This script will get a syllabified string and extract segmental information
such as: number of segments in onset position, stressed vowel etc. Crucially,
stress location is also extracted, based on your input file, where stress should
be marked with a ' (à la IPA). Whatever mark you use, just make sure you change it
below. 

First, you need a specific file format. The default here
is a comma-separated file where you have three columns per row.
word, syllabification and part of speech. Feel free to add more 
and adapt the script below, but remember the script currently requires 
*three* columns per row. Also, this script was developed for Portuguese,
so you will have to make some changes if you want to run other languages—
Romance languages such as Spanish and Italian shouldn't require a lot of
changes.

If you have monosyllables in your lexicon, please add a (redundant) stress mark.

Many thanks to Prof. Morgan Sonderegger (McGill), who was incredibly helpful.
'''


# Open a file comma-separated file
f = open("...", 'rU')

# Define output file:
outF = open("output.csv", 'wb')
csvOut = csv.writer(outF)

# list for words where stress isn't on the last 3 sylls (Portuguese stress is restricted to these positions)
badStressWords = []

# header row in the output file
csvOut.writerow(['word', 'pronunciation', 'nSyls', 'stressSylNum', 'stressLoc',
                 'nOnsetConsAntepen', 'nCodaConsAntepen', 'onsetConsAntepen', 'codaConsAntepen', 'VAntepen',
                 'nOnsetConsPen', 'nCodaConsPen', 'onsetConsPen', 'codaConsPen', 'VPen',
                 'nOnsetConsFinal', 'nCodaConsFinal', 'onsetConsFinal', 'codaConsFinal', 'VFinal',
                 'nOnsetConsStressed', 'nCodaConsStressed', 'onsetConsStressed', 'codaConsStressed', 'VStressed',
                 'nOnsetConsAlt', 'nCodaConsAlt', 'onsetConsAlt', 'codaConsAlt', 'VAlt', 'POS'])


# V and C consonant phones: define the inventories of the language
vowels = ['i~', 'e~', 'w~', 'a~', 'u~', 'j~', 'j', 'E', 'O', 'a', 'e', 'i', 'o', 'o~', 'u', 'w']

consonants = ['tS', 'p','dZ','J', 'L', 'S', 'R', 'N', 'X', 'Z', 'b',  'd', 'g', 'f', 'k', 'm', 'l', 'n', 's', 'r', 't', 'v', 'z']

## function to return information about the syllable in the list 'syls' corresponding to position 'location'.
def syllInfo(syls, location):
    ## only consider last 3 sylls
    assert location in ['antepenult', 'penult', 'final']

    
    nSyls = len(syls)

    ## return NAs for undefined syllables (antepenult if 1-2 syllable word, similar for penult)
    if((location == 'antepenult' and nSyls < 3) or (location == 'penult' and nSyls < 2 )):
        [nOnsetCons, nCodaCons, onsetCons, codaCons, V] = ['NA', 'NA', 'NA', 'NA', 'NA']
    else:
        ## pick out the right entry of syls
        if(location == 'final'):
            syl = syls[-1]
        elif(location == 'penult'):
            syl = syls[-2]
        elif(location == 'antepenult'):
            syl = syls[-3]

        # make list of phones
        syl = list(syl)

        for x in range(len(syl)-1):
            if syl[x] == '~' and syl[x-1]+syl[x] in vowels:
                syl[x-1:x+1] = [''.join(syl[x-1:x+1])]

        # if this is the stressed syll, remove the stress marker
        if(syl[0] == "'"):
            syl = syl[1:]
        
        # which phones are vowels
        vowelInds = []
        for i, ph in enumerate(syl):
            if(ph in vowels):
                vowelInds.append(i)

        # make sure syll has between 1-3 vowel phones, assuming only monoph/diph/triphthongs are allowed.
        assert len(vowelInds)>0 and len(vowelInds)<=3, vowelInds

        #  vowel phones (1-3)
        V = syl[vowelInds[0]]
        if len(vowelInds)>1:
            V += syl[vowelInds[1]]

        # number of consonants in onset and coda
        nOnsetCons = vowelInds[0]
        nCodaCons = len(syl) - vowelInds[-1] - 1

        ## material in onset and coda
        onsetCons = ''.join(syl[:vowelInds[0]]) if nOnsetCons > 0 else 'None'
        codaCons = ''.join(syl[vowelInds[-1]+1:]) if nCodaCons > 0 else 'None'

    return [nOnsetCons, nCodaCons, onsetCons, codaCons, V]

# for every line in the lexicon
for l in f:
    # separate word from pronunciation from part of speech
    entries = l.rstrip().split(',')

    # there should be just two ',', as there are three items per row
    assert len(entries)==3, "More than two , on line %s" % l

    # part of speech (pos) is the third element in each row

    word, pron = entries[0], entries[1]
    POS = entries[2]

    # these are the strings corresponding to different syllables (-)
    syls = pron.split('-')

    # number of syllables
    nSyls = len(syls) 

    # stressed syllables (those including ')
    stressedSyls = [(num, syl) for num, syl in enumerate(syls) if re.search("'", syl)]

    # make sure there's exactly 1 stressed syll. Only primary stress is dealt with here.
    assert len(stressedSyls) == 1, stressedSyls

    # which syllable (number) is stressed
    stressSylNum = stressedSyls[0][0] + 1

    ## get info for last 3 syllables (all NA if word doesn't have this syllable)
    [nOnsetConsAntepen,nCodaConsAntepen, onsetConsAntepen, codaConsAntepen, VAntepen] = syllInfo(syls, 'antepenult')
    [nOnsetConsPen,nCodaConsPen, onsetConsPen, codaConsPen, VPen] = syllInfo(syls, 'penult')
    [nOnsetConsFinal,nCodaConsFinal, onsetConsFinal, codaConsFinal, VFinal] = syllInfo(syls, 'final')

    ## for final stressed syllable, alternative = penult if it exists, set alternative syll info to NA otherwise
    if(stressSylNum == nSyls):
        stressLoc = 'final'
        [nOnsetConsStressed,nCodaConsStressed, onsetConsStressed, codaConsStressed, VStressed] =  syllInfo(syls, 'final')
        [nOnsetConsAlt,nCodaConsAlt, onsetConsAlt, codaConsAlt, VAlt] = syllInfo(syls, 'penult') if nSyls > 1 else ['NA', 'NA', 'NA', 'NA', 'NA']

    ## for penult, alternative = final
    elif(stressSylNum +1 == nSyls):
        stressLoc = 'penult'
        [nOnsetConsStressed,nCodaConsStressed, onsetConsStressed, codaConsStressed, VStressed] =  syllInfo(syls, 'penult')
        [nOnsetConsAlt,nCodaConsAlt, onsetConsAlt, codaConsAlt, VAlt] = syllInfo(syls, 'final')

    ## for antepenult, no alternative
    elif(stressSylNum + 2 == nSyls):
        stressLoc = 'antepenult'
        [nOnsetConsStressed,nCodaConsStressed, onsetConsStressed, codaConsStressed, VStressed] =  syllInfo(syls, 'antepenult')
        [nOnsetConsAlt,nCodaConsAlt, onsetConsAlt, codaConsAlt, VAlt] = syllInfo(syls, 'penult')

    else:
        print "Stress not on last 1-3 syllables: skipping word %s" % word
        badStressWords.append([word, pron])
        continue

    # write a row to CSV for this word
    csvOut.writerow([word, pron, nSyls, stressSylNum, stressLoc,
                     nOnsetConsAntepen,nCodaConsAntepen, onsetConsAntepen, codaConsAntepen, VAntepen,
                     nOnsetConsPen,nCodaConsPen, onsetConsPen, codaConsPen, VPen,
                     nOnsetConsFinal,nCodaConsFinal, onsetConsFinal, codaConsFinal, VFinal,
                     nOnsetConsStressed,nCodaConsStressed, onsetConsStressed, codaConsStressed, VStressed,
                     nOnsetConsAlt,nCodaConsAlt, onsetConsAlt, codaConsAlt, VAlt, POS])


    

# close the CSV file
outF.close()

## Finally, if there's any error due to stressless lexical words, print these words.

print
print "Words not included because stress not on one of last 3 sylls:"
for (word, pron) in badStressWords:
    print word, pron


