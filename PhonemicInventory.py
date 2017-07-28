# -*- coding: utf-8 -*-
from ipapy import UNICODE_TO_IPA
import random

class IPA_Chart:
        
    consonants = {}    
        
    def __init__(self):
        
        self.consonants = {
            #labials
            "labial": [u"p", u"b", u"f", u"v", u"m", u"w"],
            #coronals
            "coronal": [u"t", u"d", 
                u"tʃ", u"dʒ", u"θ", u"ð", u"s", u"z", u"ʃ", u"ʒ",
                u"n", u"r", u"l"],
            #dorsal (palatals and velars)
            "dorsal": [u"k", u"g", u"ŋ", u"j"],
            #glottal
            "glottal": [u"h"],
        }
            
#             #labials
#             "labial": { 
#                 "stop": 
#                     {"voiceless": u"p", 
#                     "voiced": u"b"},
#                 "fricative":
#                     {"voiceless":u"f", 
#                     "voiced": u"v"},
#                 "nasal": u"m",
#                 "glide": u"w"
#             },
#             #alveolars
#             "coronal": { 
#                 "stop": 
#                     {"voiceless":u"t", 
#                      "voiced": u"d"},
#                 "affricate":
#                     {"voiceless":u"tʃ", 
#                     "voiced": u"dʒ"},
#                 "fricative":
#                     {"interdental":
#                         {"voiceless": u"θ", 
#                         "voiced": u"ð"},
#                     "alveolar": 
#                         {"voiceless":u"s", 
#                         "voiced": u"z"},
#                     "post-alveolar":
#                         {"voiceless": u"ʃ", 
#                         "voiced": u"ʒ"}
#                     },
#                 "nasal": u"n",
#                 "liquid": 
#                     {"rhotic": u"r",
#                     "lateral": u"l"}
#                 },
#             #dorsal (palatals and velars)
#             "dorsal": { 
#                 "stop": 
#                     {"voiceless":u"k", 
#                      "voiced": u"g"},
#                 "nasal": u"ŋ",
#                 "glide": u"j"
#                 },
#             #glottal
#             "glottal": u"h",
#         }
        self.dictToIPA(self.consonants)
        
    """
    Converts entire list to IPA objects.
    """    
    def dictToIPA(self, d):
        for key, value in d.items():
            for index in range(len(value)):
                value[index] = UNICODE_TO_IPA[value[index]]
#         #for pair in preexisting dictionary
#         for key, value in d.items():
#             #if value is a dictionary, perform recursion
#             if isinstance(value, dict):
#                 self.dictToIPA(value)
#             #otherwise, convert the values to IPA objects.
#             else: 
#                 d[key] = UNICODE_TO_IPA[value]
    
    """
    Tests whether two sounds have the same place of articulation or not.
    In this case, it uses broad features like "coronal" and "dorsal" 
    rather than the more specific "interdental"
    @return if segments are homorganic or not.
    """
    def areHomorganic(self, c1, c2):
        #Check type
        if not isinstance(c1, str) or isinstance(c2, str):
            raise TypeError("One of the parameters is not a Unicode String.")
        
        c1 = UNICODE_TO_IPA[c1]
        c2 = UNICODE_TO_IPA[c2]
        
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
    def get_broad_place_feature(self, feature):
        if (feature == "dental" or "alveolar" in feature):
            return "coronal"
        elif ("labi" in feature):
            return "labial"
        elif ("palatal" in feature or feature == "velar" or feature == "uvular"):
            return "dorsal"
        elif (feature == "pharyngeal" or feature == "glottal"):
            return feature
        
    """
    Returns a random consonant
    @return: IPAString
    """
    def random_cons(self):
        result = random.choice(list(self.consonants.values()))
        return random.choice(result)
    """
    Returns a string version of the object.
    """    
    def __str__(self):    
        return self.printList(self.consonants)
        
    def printList(self, d):
        result = ""
        for key in d:
            value = d[key]
            #if value is a dictionary, recursion
            if isinstance(value, dict):
                result += self.printList(value)
                result += "/n"
            #otherwise, convert the values to IPA objects.
            else: 
                result += "\t"
                result += value.unicode_repr
        return result
    