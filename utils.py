from lemminflect import getAllInflections
from spellchecker import SpellChecker
vowels = ["a","e","u","w","y","i","o"]
def similar(word,other_word):
    vowels = ["a","e","u","w","y","i","o"]
    possible_transformations = [word]
    essential_letters = []
    keep_vowel = True
    for i in range(len(word)):
        if word[i] in vowels and keep_vowel:
            essential_letters.append(word[i])
            keep_vowel = False
        if word[i] not in vowels:
            essential_letters.append(word[i])
            keep_vowel = True
    vowels_idxs = [idx for idx in range(len(essential_letters)) if essential_letters[idx] in vowels]
    cons_idxs = [idx for idx in range(len(essential_letters)) if idx not in vowels_idxs]
    essential_letters = "".join(essential_letters)
    if essential_letters not in possible_transformations:
        possible_transformations.append(essential_letters)
    last_vowel_removed = (essential_letters[-2] in vowels 
                          and word[-2] in vowels 
                          and word[-2] != essential_letters[-2])
    if len(vowels_idxs)>1 and not last_vowel_removed:
        #monstr ous
        excluded = vowels_idxs[-1]
        possible =  essential_letters[:excluded]+essential_letters[excluded+1:]
        possible_transformations.append("".join(possible))
    if len(cons_idxs)>2 and len(essential_letters)-1 in cons_idxs:
        #absor ption #communic(a) able
        possible_transformations.append(word[:-1])
    if any(other_word.startswith(possib) for possib in possible_transformations):
        return True
    else:
        return False
    
def getInflections(raw):
    infl_dict = getAllInflections(raw)
    infl_copy = infl_dict.copy()
    for k,vals in infl_dict.items():
        if k=="NNS":
            if len(vals) == 1 and vals[0] == infl_dict["NN"][0]:
                infl_copy.pop(k)
            else:
                longest = 0
                for val in vals:
                    if len(val) > longest:
                        plural = val
                        longest = len(val)
                infl_copy.update({k:plural})
        else:
            infl_copy.update({k:vals[0]})
    return infl_copy
def get_potential_originals(word,label):
    potentials = [word]
    if len(word)<=2:
        return potentials
    parts = label.split("_")
    identifier = parts[-1]
    if word[-1].endswith("i"):
        potentials.append(word[:-1]+"y")
    if identifier in ["OUS","Y","AL","IC","SH","BLE","JJ","R"]:
        if word[-1] != "e":
            potentials.append(word + "e")
        if word[-1] == word[-2] and word[-1] != "e":
            potentials.append(word[:-1])
        if identifier in ["BLE","JJ"]:
            if word.endswith("miss"):
                potentials.append(word[:-1]+"ss")
            if identifier  == "JJ":
                if word[-1] == "s" and word[-2] != "s":
                    potentials.append(word[-1]+"de")
    if identifier == "O":
        potentials.append(word+"e")
    if identifier == "TY":
        if word.endswith("os"):
            potentials.append(word[:-1]+"us")
        if word.endswith("il"):
            potentials.append(word[:-2]+"le")
        elif word[-1] != "e":
            potentials.append(word+"e")
    if identifier in ["T","CE"]:
        if word[-1] != "e":
            potentials.append(word+"e")
        if len(word)>6:
            if word.endswith("ate") and word[-4] not in vowels:
                potentials.append(word[:-3])
    return potentials  
    
def shared_letters(first,second):
    sum = 0
    second = list(second)
    for c in first:
        if c in second:
            del second[second.index(c)]
            sum += 1
    return sum 
def corr_spell(word,suffixes):
    correct_suff = [word.endswith(suff) for suff in suffixes]
    if any(correct_suff):
        stemmed_word = word[:-len(suffixes[correct_suff.index(True)])]
    else:
        return ''
    speller = SpellChecker()
    cands = speller.candidates(word)
    max = 0
    winner = ''
    try:
        for cand in cands:
            correct_suff = [cand.endswith(suff) for suff in suffixes]
            if any(correct_suff):
                stemmed_cand = cand[:-len(suffixes[correct_suff.index(True)])]
            else: continue
            shared_letters_num = shared_letters(stemmed_cand,stemmed_word)
            if shared_letters_num > max and similar(stemmed_word,stemmed_cand):
                winner = cand
                max = shared_letters_num
    except:
        return winner
    return winner
def transform_word(word,label):
    chngdwrd = word
    if label.startswith("NN_JJ"):
        if chngdwrd[-1] == "y" and word[-2] not in vowels:
            chngdwrd = word[:-1] + "i" 
        cons_suffs = ["NN_JJ_F","NN_JJ_L"]
        if label =="NN_JJ_Y":
            if word[-1] == "y":
                chngdwrd = word + "e"
            if word[-1] == "e":
                chngdwrd = word[:-1]
        elif label =="NN_JJ_AL" :
            if word[-1] == 'y':
                chngdwrd = word[:-1]+"i"
            if word[-1] == "e":
                chngdwrd = word[:-1]
        if label not in cons_suffs:
            if word[-1]=="e" and word[-2] != "g": 
                chngdwrd = word[:-1]
            if len(word)>=3:
                if word[-2] in vowels and word[-3] not in vowels and word[-1] not in vowels:
                    if len(word) <= 4:
                        chngdwrd = word + word[-1]

    if label == "VBP_NN_R":
        if word[-1] == "e":
                chngdwrd = word[:-1]
        if word[-2] in vowels and word[-3] not in vowels and word[-1] not in vowels:
            if len(word) <= 4:
                chngdwrd = word + word[-1]
        if word[-1]=="y" and word[-2] not in vowels:
            chngdwrd = chngdwrd[:-1]+"i"
    if label in ["VBP_JJ_BLE","VBP_NN_O","VBP_JJ"]:
        if word[-3:] == "mit":
            chngdwrd = word[:-1] + "ss"
        if word[-1] == "e" and word[-2] not in ["g","c"]:
            chngdwrd = word[:-1]
        if word[-2] in vowels and word[-3] not in vowels and word[-1] not in vowels:
            if len(word) <= 4:
                chngdwrd = word + word[-1]
    if label in ["VBP_NN_O","VBP_JJ"]:
        if word[-1] == "e" and word[-2] in ["g","c"]:
            chngdwrd = chngdwrd[:-1]
        if chngdwrd[-1] == "d" and chngdwrd[-2] != "d":
            chngdwrd = chngdwrd[:-1]+"s"
            
    if label in ["VBP_NN_M","VBP_NN_AL"]:
        if word[-1] == "y" and word[-2] not in vowels:
            chngdwrd = word[:-1] + "i"
        if word[-1] == "e":
            chngdwrd = chngdwrd[:-1]
    if label in ["VBP_NN_T","VBP_NN_CE"]:
        if word[-1] == "e":
            chngdwrd = chngdwrd[:-1]
        if word.endswith("ate") and len(word)>6:
            chngdwrd = word[:-3]
    if label.split("_")[-1] == "TY":
        if word.endswith("ous"):
            chngdwrd = word[:-2]+"s"
        if word.endswith("le"):
            chngdwrd = word[:-2]+"il"
        elif word[-1] == "e":
            chngdwrd = word[:-1]
    if label in ["VBP_NN_N","VBN_NN"]:
        if word[-1] == "y" and word[-2] not in vowels:
            chngdwrd = word[:-1]+"i"
    if "RB" in label.split("_"):
        if word[-1]=='y' and word[-2] not in vowels:
            chngdwrd = word[:-1]+"i" 
        if word[-2:] == "le":
            chngdwrd = word[:-2]
        if word[-2:] == "ic":
            chngdwrd = word+"al"
    return chngdwrd
def singularize(plural):
    endings = ["ses","shes","ches","xes","zes"]
    if plural.endswith("ies"):
        singular = plural[:-3]+"y"
        inflecs = getInflections(singular)
        if "NNS" in inflecs:
            if getInflections(singular)["NNS"]==plural:
                return singular
        else:
            return plural
    elif any(plural.endswith(ending) for ending in endings):
        singular = plural[:-2]
        inflecs = getInflections(singular)
        if "NNS" in inflecs:
            if getInflections(singular)["NNS"]==plural:
                return singular
        else:
            return plural
    elif plural.endswith("s"):
        singular = plural[:-1]
        inflecs = getInflections(singular)
        if "NNS" in inflecs:
            if getInflections(singular)["NNS"]==plural:
                return plural[:-1]
        else:
            return plural
    else:
        return plural
