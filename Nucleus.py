# -*- coding: utf-8 -*-
import random

class Nucleus:

    def __init__(self):
        
        #list of possible English syllable nuclei
        self.vowels = [
            #0 short vowels
            [u"æ", u"ɒ", u"ɛ", u"ə", u"ɪ", u"ʌ", u"ʊ"],
            #1 long vowels
            [u"ɑ:", u"i:", u"u:", u"aɪ", u"aʊ", u"eɪ", u"ɔɪ", u"oʊ"],
            #2 syllabic consonants
#             [u"ɹ̩", u"l̩", u"n̩", u"m̩"]
        ]

        index = random.randint(0, (len(self.vowels) - 1))  #pick a random kind of syllable nucleus
        #get qualities for vowels.
        if(index == 0):
            self.long = False   #short vowel
            self.closed = False #closed syllable
        elif(index == 1):
            self.long = True    #long vowel
            self.closed = bool(random.getrandbits(1))   #can be open or closed.
        else: 
            self.long = False   #syllabic consonants aren't long vowels
            self.closed = True  #always at the end of syllables and words
            
        self.ipa = random.choice(self.vowels[index])     #pick a random nucleus from that category
        
    def __str__(self):
        return self.ipa   
