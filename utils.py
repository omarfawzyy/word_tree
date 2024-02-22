from lemminflect import getAllInflections
from spellchecker import SpellChecker
vowels = ["a","e","i","u","o","w","y"]
def similar(word,derivation): 
    global vowels
    word_consonants= []
    word_vowels = []
    for char in word:
        if char not in vowels:
            word_consonants.append(char)
        else:
            word_vowels.append(char)
    derivation_consonants= []
    derivation_vowels= []
    for char in derivation:
        if char not in vowels:
            derivation_consonants.append(char)
        else:
           derivation_vowels.append(char) 
    if ((word[0] in vowels and derivation[0] not in vowels)
    or (derivation[0] in vowels and word[0] not in vowels)):
        return False
    #checking if words share consonants (last letter exception to accomodate transformations)
    deriv_len = len(derivation_consonants)
    word_len = len(word_consonants)
    if word_len>2 and deriv_len>2:
        if word_len == deriv_len:
            derivation_consonants = derivation_consonants[:-1] 
            word_consonants = word_consonants[:-1]
        elif word_len+1==deriv_len:
            derivation_consonants = derivation_consonants[:-1]
        elif word_len==deriv_len+1:
            word_consonants = word_consonants[:-1]
    return  derivation_consonants == word_consonants
    
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
    if len(word)<2:
        return []
    nn_jjs = ["NN_JJ_OUS","NN_JJ_F","NN_JJ_L","NN_JJ_Y","NN_JJ_D","NN_JJ_AL","NN_JJ_IC","NN_JJ_SH"]
    potentials = [word]
    if label in nn_jjs+["VBP_JJ_BLE","VBP_JJ"]:
        type = label.split("_")
        if len(type) == 3:
            type = type[2]
        else:
            type = type[1]
        if word[-1].endswith("i"):
            potentials.append(word[:-1]+"y")
        if type in ["OUS","Y","AL","IC","SH","BLE","JJ","R"]:
            if word[-1] != "e":
                potentials.append(word + "e")
            if word[-1] == word[-2] and word[-1] != "e":
                potentials.append(word[:-1])
            if type in ["BLE","JJ"]:
                if word[-4:].endswith("miss"):
                    potentials.append(word[:-1]+"ss")
                if type  == "JJ":
                    if word[-1] == "s" and word[-2] != "s":
                        potentials.append(word[-1]+"de")
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
            if shared_letters_num > max and similar(stemmed_cand,stemmed_word):
                winner = cand
                max = shared_letters_num
    except:
        return winner
    return winner
def transform_word(word,label):
    try:
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
            elif label not in cons_suffs:
                if word[-1]=="e" and word[-2] != "g": 
                    chngdwrd = word[:-1]
                elif word[-2] in vowels and word[-3] not in vowels and word[-1] not in vowels:
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
        if label in ["VBP_NN_T","VBP_NN_T"]:
            if word[-4:] in ["ance","ence"]:
                chngdwrd = word[:-4]
            elif word[-1] == "e":
                chngdwrd = chngdwrd[:-1]
            if word.endswith("ate") and len(word)>6:
                chngdwrd = word[:-3]
        if label == "VBP_NN_CE":
            if word[-4:] in ["ent","ant"]:
                chngdwrd = word[:-3]
            if word[-1] == "y" and word[-2] not in vowels:
                chngdwrd = word[:-1]+"i"
            if word[-1] == "e":
                chngdwrd = word[:-1]
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
    except:
        return chngdwrd
    return chngdwrd
def spell_check(word):
    speller = SpellChecker()
    correction = speller.correction(word)
    if similar(word,correction):
        return correction
    else:
        return None