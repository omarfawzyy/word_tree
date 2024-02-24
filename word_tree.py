from utils import *
from derivations import Derivations
import spacy


def create_word_tree(raw):
    raw = singularize(raw)
    nlp = spacy.load("en_core_web_sm") 
    derivations = Derivations()
    word_tree = {}
    # stripping raw(input) from any suffix if possible
    first_order_suffixes = { 
        "NN_JJ_F" : ['ful'], 
        "NN_JJ_L" : ['less'],
        "NN_JJ_OUS" : ['ous'],
        "NN_JJ_D" : ['ed'],
        "NN_JJ_Y":["y"],
        "NN_JJ_AL":["ial","ical","al"],
        "NN_JJ_IC": ["tic","ic"],
        "NN_JJ_SH": ["ish"],
        "VBP_NN_O":["ation","ption","ition","tion","ion"],
        "VBP_NN_R":["er","or","ar"],
        "VBP_NN_M":["ment"],
        "VBP_NN_AL":["al"],
        "VBP_NN_CE":["ance","ence"],
        "VBP_NN_T":["ent","ant"],
        "VBP_JJ":["ative","itive","ptive","tive","ive"],
        "VBP_JJ_BLE":["able","ible"]
    }
    
    second_order_suffixes = {
        "JJ":{
            "RB":["ly"],
            "NN_N":["ness"],
            "NN_TY":["ity","ty"]
        }
    }
    for pos,types in second_order_suffixes.items():
        for label,suffixes in types.items():
            correct_suffix = [raw.endswith(suff) for suff in suffixes]
            if any(correct_suffix):
                suffix = suffixes[correct_suffix.index(True)]
                stem = raw[:-len(suffix)]
                potentials = get_potential_originals(stem,label)
                for potential in potentials:
                    inflecs = getInflections(potential)
                    if pos in inflecs:
                        raw = inflecs[pos]
    
    for label,suffixes in first_order_suffixes.items():
        prior_pos = label.split("_")[0]
        current_pos = label.split("_")[1]
        possible_suffixes = [suffix for suffix in suffixes if raw.endswith(suffix)]
        if possible_suffixes != []:
            if current_pos not in getInflections(raw):
                break
        valid_word_found = False
        for suffix in possible_suffixes:
            if label == "NN_JJ_D":
                pos_dict = getInflections(raw)
                if (((pos_dict == {} or "JJ" in pos_dict) and "VB" not in pos_dict) 
                    and nlp(raw)[0].pos_ == "VERB"):
                    raw = nlp(raw)[0].lemma_
                    valid_word_found = True
                    break  
            stem = raw[:-len(suffix)]
            potentials = get_potential_originals(stem,label)
            valid_word_idx = [prior_pos in getInflections(potential) for potential in potentials]
            if any(valid_word_idx):
                raw = potentials[valid_word_idx.index(True)]
                valid_word_found = True
                break
        if not valid_word_found and possible_suffixes != []:
            speller = SpellChecker()
            suff_lengths = [len(suff) for suff in possible_suffixes]
            longest_suffix_idx = suff_lengths.index(max(suff_lengths))
            suffix = possible_suffixes[longest_suffix_idx]
            stem = raw[:-len(suffix)]
            correction = speller.correction(stem)
            if correction not in [stem,raw,''] and correction != None:
                derivations.set(correction)
                print("checking if "+correction+" is root")
                if derivations.is_derivationally_related(raw):
                    inflecs = getInflections(raw)
                    addDerivation(word_tree,label,inflecs,derivations)
                    raw = correction
                    break
                else:
                    derivations.unset()
        if derivations.is_set: break
    # creating word tree from base word(raw)
    pos_dict = getInflections(raw)
    if "VB" not in pos_dict and nlp(raw)[0].pos_ == "VERB":
        raw = nlp(raw)[0].lemma_
        pos_dict = getInflections(raw)
    word_tree.update(pos_dict)
    for pos,word in word_tree.copy().items():
        chngdwrd = word
        if pos == 'NN':
            nn_jjs = {
                      "NN_JJ_F" : ['ful'], 
                      "NN_JJ_L" : ['less'],
                      "NN_JJ_OUS" : ['ous'],
                      "NN_JJ_D" : ['ed'],
                      "NN_JJ_Y":["ey","y"],
                      "NN_JJ_AL":["ial","ical","al"],
                      "NN_JJ_IC": ["tic","ic"],
                      "NN_JJ_SH": ["ish"]
                      }
            
            for label,suffixes in nn_jjs.items(): 
                transformed = transform_word(word,label)
                pos = "JJ"
                added = insertSuffixedWord(word_tree,pos,label,suffixes,word,transformed,derivations)    
            if "VBD" in word_tree and "NN_JJ_D" in word_tree:
                if word_tree["VBD"] == word_tree["NN_JJ_D"]:
                    word_tree.pop("NN_JJ_D")
                    
                            
        elif pos == 'VBP':
            vbp_nns = {
                "VBP_NN_O":["ation","ption","ition","tion","ion"],
                "VBP_NN_R":["er","or","ar"],
                "VBP_NN_M":["ment"],
                "VBP_NN_AL":["al"],
                "VBP_NN_CE":["ance","ence"],
                "VBP_NN_T":["ent","ant"]
            }
            for label,suffixes in vbp_nns.items():
                pos = "NN"
                transformed = transform_word(word,label)
                insertSuffixedWord(word_tree,pos,label,suffixes,word,transformed,derivations)
            if "VBP_NN_O" in word_tree:
                inserted_word = word_tree["VBP_NN_O"]
                label = "VBP_JJ"
                added_suffix = inserted_word[:-3] + "ive"
                inflecs = getInflections(added_suffix)
                derivations.add_derivation(added_suffix)#back
                addDerivation(word_tree,label,inflecs,derivations)
            vbp_jjs = {
                "VBP_JJ":["ive"],
                "VBP_JJ_BLE":["able","ible"]
            }
            for label,suffixes in vbp_jjs.items():
                pos = "JJ"
                transformed = transform_word(word,label)
                insertSuffixedWord(word_tree,pos,label,suffixes,word,transformed,derivations) 

        elif pos in ["VBD","VBN"]:
            inflecs = getInflections(word)
            if "NN" in inflecs:
                addNoun(inflecs,"VBN_NN_ORI",word_tree) 
    for k,v in word_tree.copy().items():
        vchngd = v
        parts = k.split("_")
        # adding noun suffix(ity or ness) to adjectives
        if 'JJ' in parts and "ORI" not in parts:
            label = k +"_NN_TY"
            vchngd = transform_word(v,label)
            tys = ["ity","ty"]
            pos = "NN"
            added = insertSuffixedWord(word_tree,pos,label,tys,v,vchngd,derivations)
            if not added:
                label = k+"_NN_N"
                vchngd = transform_word(v,label)
                added_suffix = vchngd + "ness"
                inflecs = getInflections(added_suffix)
                addDerivation(word_tree,label,inflecs,derivations)
        if k in ['VBD','VBN']:
                label = "VBN_NN"
                added_suffix = transform_word(v,label) +"ness"
                inflecs = getInflections(added_suffix)
                addDerivation(word_tree,label,inflecs,derivations)
        # adding adverb suffix(ly)
        if k in ['VBD','VBG','VBN'] or ('JJ' in parts and 'ORI' not in parts):
            if raw[-2:]=="ic" and "NN_JJ_AL" in word_tree:
                if parts[-1] =="AL": continue
            if 'JJ' in parts:
                idx = parts.index("JJ")
                parts[idx] = "RB"
                label = "_".join(parts)
            else:
                if k in ["VBN","VBD"]:
                    label = "VBN_RB"
                elif k == "VBG":
                    label = k + "_RB" 
            added_suffix = transform_word(v,label)+"ly"
            inflecs = getInflections(added_suffix)
            addDerivation(word_tree,label,inflecs,derivations)
    return word_tree
def insertSuffixedWord(word_tree,pos,label, suffixes,root,chngdwrd,derivations):
    '''
    this function checks if suffix combination exists and adds it 
    to the word_tree dictionary. 
    '''
    if label in word_tree:
        return True
    candidates = []
    #checking each suffix combination for a given label
    for suff in suffixes:
        added_suffix = corr_spell(chngdwrd+suff,suffixes) 
        inflecs = getInflections(added_suffix)
        #change label according to pos of added_suffix
        if label == "VBP_NN_T":
            if pos == "NN" and "NN" not in inflecs and "JJ" in inflecs:
                pos = "JJ"
                parts = label.split("_")
                parts[parts.index("NN")] = "JJ"
                label = "_".join(parts)
        # clearing up suffix confusions    
        if pos not in inflecs and inflecs !={}:
            continue
        if label == "VBP_NN_T":
            if added_suffix[-4:] == "ment" and chngdwrd[-1] != "m":
                continue
        # update stem if last word in stem doubled
        if label.split("_")[-1] in ["AL","BLE","CE","R","T"]:
            doubled = chngdwrd+chngdwrd[-1]
            if added_suffix.startswith(doubled):
                chngdwrd = doubled
        # adding combination to candidates list unless stem is identified as a different word
        if added_suffix.startswith(chngdwrd):
            potential_suffix = added_suffix[len(chngdwrd):]
            correct_index = [potential_suffix == suff for suff in suffixes]
        else:
            correct_index = [added_suffix.endswith(suff) for suff in suffixes]
        if any(correct_index):
            suffix = suffixes[correct_index.index(True)]
            if added_suffix == chngdwrd+suffix:
                candidates.append({"stem":chngdwrd,"suffix":suffix})
                break
            else:
                stem = added_suffix[:-len(suffix)]
                potentials = get_potential_originals(stem,label)
                if not any(getInflections(potential)!={} for potential in potentials):
                    candidates.append({"stem":stem,"suffix":suffix})

    if len(candidates)>1:
        #picking candidate closest to the given word
        scores = [shared_letters(cand["stem"],chngdwrd) for cand in candidates]
        idxs = [idx for idx in range(len(scores)) if scores[idx] == max(scores)]
        word_lengths = [len(candidates[idx]["stem"]) for idx in idxs]
        shortest = candidates[idxs[word_lengths.index(min(word_lengths))]]
        suffix = shortest["suffix"]
        removed_suffix = shortest["stem"]
    elif len(candidates)==1:
        suffix = candidates[0]["suffix"]
        removed_suffix = candidates[0]["stem"]
    else:
        return False
    #check if word exists
    added_suffix = removed_suffix+suffix 
    inflecs = getInflections(added_suffix)
    if inflecs == {}:
        inflecs = {pos:added_suffix}
    elif pos not in inflecs:
        return False
    
    # lookup root of word online
    if removed_suffix not in [chngdwrd,root]:
        #check if word is derived from different root retrievable by inversing spelling changes
        potential_originals = get_potential_originals(removed_suffix, label)
        found = any(getInflections(pot) != {} for pot in potential_originals)
        if not found:
            # add if word is derivationally related based on etymology(uses results from etymonline.com)
            print(f'checking if "{added_suffix}" is derivationally related')
            if not derivations.is_set:
                derivations.set(root)
            if derivations.is_derivationally_related(added_suffix):
                derivations.add_derivation(added_suffix)
                addDerivation(word_tree,label,inflecs,derivations)
                return True
            else:
                return False
    else:
        derivations.add_derivation(added_suffix)
        addDerivation(word_tree,label,inflecs,derivations)
        return True
    return False
def addDerivation(word_tree,label,inflecs,derivations):
    if label == "VBP_NN_T":
        if "JJ" in inflecs:
            label = "VBP_JJ_T"
            word_tree.update({label:inflecs["JJ"]})
        if "NN" in inflecs:
            label = "VBP_NN_T"
            addNoun(inflecs,label,word_tree)
    elif "JJ" in inflecs:
        derivation = inflecs["JJ"]
        word_tree.update({label:derivation})
        derivations.add_derivation(derivation)
        if "NN" in inflecs:
            label = label + "_NN_ORI"
            addNoun(inflecs,label,word_tree)
    elif "NN" in inflecs:
        addNoun(inflecs,label,word_tree)
        derivations.add_derivation(inflecs["NN"])
    elif "RB" in inflecs:
        derivations.add_derivation(inflecs["RB"])
        word_tree.update({label:inflecs["RB"]})
def addNoun(inflecs,label,added):
    parts = label.split("_")
    if "NN" in inflecs:
        added.update({label: inflecs["NN"]})
    if "NNS" in inflecs:
        if parts[-1] == "NN":
            plur_label = '_'.join(parts[0:-1]) + "_NNS"
            added.update({plur_label:inflecs['NNS']})
        elif len(parts) > 1: 
            if parts[-2] == "NN":
                plur_label = '_'.join(parts[0:-2]) + "_NNS_" + parts[-1]
                added.update({plur_label: inflecs['NNS']})


