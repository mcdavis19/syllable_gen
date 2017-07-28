# -*- coding: utf-8 -*-
import random
import string
from Nucleus import *
from PhonemicInventory import IPA_Chart
from ipapy import UNICODE_TO_IPA, ipachar
from ipapy.ipastring import IPAString
from test import double_const
from ipapy.ipachar import IPAConsonant, IPAChar
from builtins import str

def get_input():
    letter = ""
    while (letter != "v" and letter != "c" and letter != "l"):
        letter = input("Would you like a vowel (v), consonant(c) or any letter (l)? ")
    print("get_input")
    return letter

def syllable():
    o = onset() 
    r = rhyme()
    assert isinstance(o, IPAString)
    assert isinstance(r, IPAString)
    return o + r

"""
Creates a randomly generated syllable onset that is plausible according
to English phonology. 

@return: IPAString representing the syllable onset
"""
def onset():
    #English syllable onsets can be up to three segments long.
    length = random.randint(0,3)
    if length == 0:                     #No onset
        onset = IPAString(unicode_string=u"")
    elif length == 1:                   #Any consonant is possible
        onset = single_onset()     
    elif length == 2:                   #Two consonants
        onset = double_cons_onset()
    else:                               #Three consonants
        onset = triple_cons_onset()
    return onset

"""
Returns a randomly generated syllable onset of three consonants
according to English syllable constraints. 

The first segment must be /s/. The second must be a voiceless plosive
and the third must be an approximant that is not homorganic with the
voiceless stop. That is, it must not share the same place of articulation.

@return: Unicode String
"""
def triple_cons_onset():
    c1 = u"s"
    c2 = random.choice([u"p", u"t", u"k"])
    #/pw/ and /bw/ are not possible except in borrowed words
    if c2 == u"p":
        c3 = random.choice([u"r", u"l", u"j"])
    #clusters like /tj/ and /dj/ are not found in American English
    #and thus excluded here.
    elif c2 == u"t":    
        c3 = random.choice([u"r", u"w"])
    else:
        c3 = random.choice([u"r", u"l", u"w", u"j"])
#         @TODO implement homorganic check method
#         while not chart.areHomorganic(c2, c3):
#             #if homorganic, reassign c3
#             c3 = random.choice([u"r", u"l", u"w", u"j"])
    onset = c1+c2+c3
    return IPAString(unicode_string=onset) 

"""
Generates a random consonant cluster of two segments that conforms to 
English syllable constraints.

@return IPAString
"""
def double_cons_onset():
    onsets = [u"p", u"t", u"k", u"b", u"d", u"g", u"f", u"θ", u"v", u"s"]
    onset1 = u"s" #random.choice(onsets)
    onset1 = UNICODE_TO_IPA[onset1]
    place = onset1.place
    
    #Assign second segment that is not homorganic except for s
    if onset1.manner == "sibilant-fricative":         #s
        onset2 = random.choice([u"r", u"l", u"w", u"j", u"p", u"t", u"k", u"m", u"n"])
        #change /s/ to /ʃ/ if followed by /r/
        if onset2 == u"r":
            onset1 = UNICODE_TO_IPA[u"ʃ"]
    elif place == "alveolar" or place == "dental":        #coronal
        onset2 = random.choice([u"r", u"w"])
    elif place == "bilabial" or place == "labio-dental":#labial
        onset2 = random.choice([u"r", u"l", u"j"])
    else:                                               #dorsal
        onset2 = random.choice([u"r", u"l", u"w", u"j"])
    
    #Convert to IPAString and return
    onset = onset1.unicode_repr + onset2
    return IPAString(unicode_string=onset)   
        
"""
Returns a syllable onset of a single consonant that conforms to English
syllable constraints. In this case, the consonant cannot be "ʒ" or "ŋ".

@return IPAString  
"""
def single_onset():
    chart = IPA_Chart()
    #syllables cannot begin with ezh or eng
    while True:
        onset = chart.random_cons()
        if onset != u"ʒ" and onset != u"ŋ":
            break
    #convert to IPA String from IPAConsonant
    return IPAString(unicode_string=onset.unicode_repr)

"""
Generates the syllable nucleus and coda i.e. the vowel and
final consonant(s) depending on the syllabic weight of the nucleus.

For example, if the vowel is long, that effects what consonants can
make up the coda, whether or not they can be clustered and if how 
how complex that cluster can be.
@return IPAString
"""
def rhyme():
    nucleus = Nucleus()
    #Get IPA string from Unicode
    rhyme = getattr(nucleus, "ipa")
    rhyme = IPAString(unicode_string=str(nucleus), ignore = True)
    #If syllable is closed, we need to get a coda.
    if not nucleus.closed:
        c = coda()
#         print(type(c), type(rhyme))
        rhyme.extend(c)
    return rhyme

"""
Generates random consonants to close the syllable while 
conforming to English syllable constraints.

@return: IPAString with syllable coda
""" 
def coda():
    
#     length = random.randint(1,3)
#     
#     #Coda will have one consonant
#     if (length == 1):
        chart = IPA_Chart()
        c1 = u""
        #syllables cannot end with certain phonemes
        while True:
            c1 = chart.random_cons()
            if (c1.unicode_repr != u"h" and 
                c1.unicode_repr != u"w" and 
                c1.unicode_repr != u"j" and
                c1.unicode_repr != u"ʒ" and 
                c1.unicode_repr != u"ð"):
                break
        
        if (random.getrandbits(1)): #random yes or no
            #return the coda we have as IPAString 
            return IPAString(ipa_chars=[c1])   
        #or continue to build coda
        else: 
            c1unicode = c1.unicode_repr
            c2 = u""  
            #add more consonants and determine what can be added
               
            #if c1 is a liquid
            if (c1unicode == u"l" or c1unicode == u"r"):
                #can be followed by an obstruent with a few exceptions
                #/lg/ is treated as an accidental gap in English
                while True:
                    c2 = chart.random_cons()
                    c2unicode = c2.unicode_repr
                    # -rl is a valid coda
                    if (c1unicode == u"r" and c2unicode == u"l"):
                        break
                    #non-velar nasals /m/ and /n/ are fine after a liquid
                    elif (c2.manner == u"nasal" and c2.place != u"velar"):
                        break
                    #not edh or ezh
                    if (c2unicode != u"ʒ" or c2unicode != u"ð"):
                        break
                    #Any other obstruent is fine.
                    elif (is_obstruent(c2)):
                        break
                    
            #c1 is a nasal
            elif ("nasal" == c1.manner):
                #do-while loop until we get a homorganic obstruent
                while True:
                    c2 = chart.random_cons()
#                     c2 = UNICODE_TO_IPA[c2]
                    if (is_obstruent(c2) and are_homorganic(c1, c2)):
                        break
            elif ("fricative" in c1.manner):    #"in" because possible "sonorant-fricative" manner
                #if c1 is /f/, then c2 can be /θ/ or /t/
                if (c1.unicode_repr == u"f"):
                    
                    c2 = UNICODE_TO_IPA[u"θ"]
#                 #if c1 is /s/, then it must be a voiceless stop
#                 else:   
                 
#             elif ("plosive" == c1.manner):
            return IPAString(ipa_chars=[c1])
    
#     #If word-final, an alveolar obstruent can be added
#     #if (word_final):
#     coda = appendix(coda)
    
    #convert to IPA String from IPAConsonant
    
"""
Tests whether two sounds have the same place of articulation or not.
In this case, it uses broad features like "coronal" and "dorsal" 
rather than the more specific "interdental"
@param param: String or IPAConsonant
@return if segments are homorganic or not.
"""
def are_homorganic(c1, c2):
    #Convert to IPAConsonant if string
    if isinstance(c1, str):
        c1 = UNICODE_TO_IPA[c1]
    elif not isinstance(c1, IPAConsonant):
        raise TypeError("One or more parameters is not a string or an IPAConsonant")    
        
    if isinstance(c2, str):
        c2 = UNICODE_TO_IPA[c2]
    elif not isinstance(c2, IPAConsonant): 
        raise TypeError("One or more parameters is not a string or an IPAConsonant")
      
    #Check built in ipapy feature
    if c1.place == c2.place:
        return True
    
    #Check broader categories
    if (get_broad_place_feature(c1.place) == get_broad_place_feature(c2.place)):
        return True
    
    return False    
    
"""
Finds a broader feature that describes the place of articulation.
Postalveolar consonants are considered to be coronal.
Labiolinguals are considered to be labial. 
"""
def get_broad_place_feature(feature):
    if (feature == "dental" or "alveolar" in feature):
        return "coronal"
    elif ("labi" in feature):
        return "labial"
    elif ("palatal" in feature or feature == "velar" or feature == "uvular"):
        return "dorsal"
    elif (feature == "pharyngeal" or feature == "glottal"):
        return feature    
    
"""
Determines if an consonant is an obstruent or not.
@param cons: IPAConsonant
@return: boolean     
"""
def is_obstruent(cons):
    #check type
    if not isinstance(cons, IPAConsonant):
            raise TypeError("One of the parameters is not an IPAConsonant.")

    manner = cons.manner            #The obstruent class consists of
    if (manner == "plosive"):        #plosives
        return True
    elif ("affricate" in manner):   #affricates
        return true                 #ipapy says "sibilant-affricate", hence the "in"
    elif ("fricative" in manner):   #fricatives
        return True
    else:
        return False
    
"""
Adds an alveolar obstruent to the end of the syllable coda
given as a Unicode string.

In English, words can end with very heavy consonant clusters as in "sixths", 
"strengths" and "twelfths". This adds that final alveolar segment. It chooses
between /t/ and /d/ according to voicing. It chooses between a plosive, fricative
or a null at random.

@param: IPAstring representing a syllable coda
@return IPAString representing a potentially heavier coda
""" 
def appendix(coda):
    r = random.randint(0,2)
    
    #add nothing
    if (r == 0):
        return coda
    #fricative 
    elif (r == 1):
        #but not after with /s/, /z/, /ʃ/, /ʒ/, /tʃ/ or /dʒ/
        if (u"sibilant" in coda[-1].manner):
            return coda.append(UNICODE_TO_IPA[u"s"])
    #plosive but not after another /t/ or /d/
    elif (r == 2):
        #get voicing for last segement of existing coda
        v = coda[-1].voicing
        if (v == u"voiced"):    #voiced
            return coda.append(UNICODE_TO_IPA[u"d"])
        else:                   #voiceless
            return coda.append(UNICODE_TO_IPA[u"t"])
        
        
def main():
#     consonants()
    
#     my_l = (UNICODE_TO_IPA[u"l"])
#     my_d = (UNICODE_TO_IPA[u"d"])
#     my_th = (UNICODE_TO_IPA[u"θ"])
#     print(my_d, my_d.place, my_l, my_l.place, my_th, my_th.place)
#     
#     my_b = (UNICODE_TO_IPA[u"b"])
#     my_w = (UNICODE_TO_IPA[u"w"])
#     print(my_b, my_b.place, my_w, my_w.place)

#     chart = IPA_Chart()
#     print(chart)
    
    for i in range(20):
        ipa = syllable()
        print(i, ipa, type(ipa))
    
#     options = {"v": vowel, "c": consonant, "l": letter}
#     
#     name = ""
#     input = ""
#     for i in range(2):
#         name = "" 
#         for j in range(3):
#             key = get_input()
#             name += options[key]()
#             
#         name = name.title()
#         print(name)
#         
main()