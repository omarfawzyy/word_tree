<img src="https://github.com/omarfawzyy/word_tree/raw/main/illustration.png" alt="word tree example" width="500">

## Generate derivatives of a base word through suffix additions

Suffixes are added to a given base word to create derivative words with varying meanings and part of speech(ex. beauty,beautiful,etc). In order to ensure that all derivatives are captured,it is preferable to provide the base word rather than a suffixed word. For example instead of supplying "romantic" to the function, supply "romance" to capture more derivatives. Base words can be a verb, noun, adjective, or even an adverb. 

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

## Labeling Scheme

The labeling and concept of the word tree is inspired by this [paper](https://aclanthology.org/W19-4415.pdf). Each label consists of component(s)(seperated by "_") that describe the pos of the component and/or the kind of suffix added to the word in case multiple suffixes lead to the same pos. Check appendix A of the above paper for more details.

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
The words are looked up on etymonline.com

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

