import re
from bs4 import BeautifulSoup
import requests
prefixes = ['ante', 'auto', 'circum ',
            'co', 'com', 'con', 'en', 'exo', 'extra',
            'hetero', 'homo', 'hyper', 'inter','intro', 'mega ',
            'micro', 'mid', 'mis', 'mono', 'over', 'post',
            'pre','pro','per', 're', 'semi', 'sub', 'trans', 
            'a', 'ab', 'an', 'anti', 'contra', 'counter',
            'de', 'dis', 'ex', 'il', 'im', 'in', 'ir', 'non', 'un']

class Derivations:
    def __init__(self):
        self.is_set = False
        self.derivationally_related_words = []
    def set(self,origin):
        self.is_set = True
        self.origin = origin
        soup = _get_soup_object("https://www.etymonline.com/word/"+origin)
        if soup == False:
            self.info_fetched = False
        else:
            self.info_fetched = True
            self.derivationally_related_words.append(origin)
            self.origin_roots = create_roots(soup)
    def is_derivationally_related(self,derived):
        if not self.info_fetched:return False
        soup = _get_soup_object("https://www.etymonline.com/word/"+derived)
        if soup == False:
            return False
        try:
            related_words = soup.find("div",class_= "word--C9UPa").findAll("a")
            related_words = [word.text for word in related_words if word.text != None]
        except:
            related_words = []
        for related in related_words:
            if related in self.derivationally_related_words:
                self.derivationally_related_words.append(derived)
                return True
        deriv_roots = create_roots(soup)
        for r in self.origin_roots:
            if r in deriv_roots:
                self.derivationally_related_words.append(derived)
                return True
        return False
    def add_derivation(self,derivation):
        self.derivationally_related_words.append(derivation)
def create_roots(soup):
    global prefixes
    regex = re.compile('[^a-z]')    
    sections = soup.findAll('div',class_="word--C9UPa")
    roots = []
    prefix = ''
    suffix = ''
    skip = False
    for sec in sections:
        if len(sec["class"])>1:continue
        spans = sec.findAll("span")
        is_suffix = False
        for span in spans:
            txt = span.text
            if is_suffix:
                suffix = txt
                txt = prefix+suffix
                is_suffix = False
            if txt == '':continue
            if len(txt.split())>1:continue
            if txt[-1]=='-' or txt in prefixes:
                prefix = txt
                is_suffix = True
                continue
            txt = regex.sub('',txt.strip())
            roots.append(txt)
    return roots

def _get_soup_object(url, parser="html.parser"):
    try:
        req = requests.get(url)
        if req.status_code != 200:
            return False
        return BeautifulSoup(req.text, parser)
    except:
        return False