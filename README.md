<img src="https://github.com/omarfawzyy/word_tree/raw/main/illustration.png" alt="word tree example" width="500">

## Generate derivatives of a base word through suffix additions

Suffixes are added to a given base word to create derivative words with varying meanings and part of speech(ex. beauty,beautiful,etc). In order to ensure that all derivatives are captured, the given word must not include any of the suffixes because the algorithm adds suffixes to the input not stem it. For example instead of supplying "beautiful" to the function, supply "beauty" to capture more derivatives. Base words can be a verb(present form), noun, adjective, or even an adverb. 
### Algorithm details:
for every suffix:
1. base word's spelling is transformed depending on the suffix to be added
2. the suffix is combined with the transformed word
3. the suffixed word is inputted to a spellchecker 
4. if the spellchecker did not alter the word, the word is added to the wordtree 
5. if spellchecked word's stem is identified as a different word the word isn't added to the word tree.
6. if spellchecked word's stem cannot be identified we check if the spellchecked word is derivationally related to base word according to (etymonline.com)
7. if word is derivationally related it is added to word tree otherwise it isn't.
## Examples

Here are some examples :

```python
>>> from word_tree.word_tree import create_word_tree
>>> create_word_tree("beauty")
>>> {'NNS': 'beauties', 'NN': 'beauty',
     'NN_JJ_F': 'beautiful', 'NN_JJ_OUS': 'beauteous',
     'NN_RB_F': 'beautifully'}
>>> create_word_tree("use")
>>> {'NNS': 'uses', 'NN': 'use', 'VBG': 'using', 'VBZ': 'uses',
     'VB': 'use', 'VBP': 'use', 'VBN': 'used', 'NN_JJ_F': 'useful',
     'NN_JJ_L': 'useless', 'NN_JJ_D': 'used', 'VBP_NN_R': 'user',
     'VBP_NNS_R': 'users', 'VBP_NN_CE': 'usance', 'VBP_JJ_BLE': 'usable',
     'NN_JJ_F_NN_N': 'usefulness', 'NN_JJ_F_NNS_N': 'usefulnesses',
     'NN_RB_F': 'usefully', 'NN_JJ_L_NN_N': 'uselessness',
     'NN_RB_L': 'uselessly', 'VBP_JJ_BLE_NN_TY': 'usability'}
>>> create_word_tree("brute")
>>> {'JJ': 'brute', 'NNS': 'brutes', 'NN': 'brute', 'NN_JJ_AL': 'brutal',
     'NN_JJ_SH': 'brutish', 'NN_JJ_AL_NN_TY': 'brutality', 'NN_RB_AL': 'brutally'}
```

## Bonus: Derivations Module

The derivations module used above for looking up if a word is derivationally related to another can be used independently as shown below.

```python
>>> from word_tree.derivations import Derivations
>>> # use set method to input base word
>>> derivations = Derivations()
>>>derivations.set("beauty")
>>> # use is_derivationally_related method to return boolean value 
>>> derivations.is_derivationally_related("beautiful")
>>> True
```


## Compatibility

Tested on Python 3

## Installation

1. Clone the repository:

```
git clone https://github.com/omarfawzyy/word_tree.git
```


## Maintainer

Hello, I'm Omar. Feel free to get in touch with me
at omaralzamk@gmail.com.

## Dependencies

- [lemminflect](https://pypi.org/project/lemminflect/0.1.0/)
- [pyspellchecker](https://pypi.org/project/pyspellchecker/)

## Acknowledgements
The concept of the word tree and the naming scheme of the labels are inspired by this [paper](https://aclanthology.org/W19-4415.pdf)

