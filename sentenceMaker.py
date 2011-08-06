import os
import random

# Possesives
# Add optional options e.g. negation
# Fix I->me, he->him 
# Fix space before punctuation
# Catch errors if categories not defined
# Improve how Chinese words are defined in pattern: dict[hani] = word
# How to associate verbs with relevant nouns

vowels = ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
to_be = {'I': 'am', 'you': 'are', 'you (polite)': 'are'}
pronoun_subj_obj = {'I': 'me', 'he': 'him', 'she': 'her'}
possesive = {'I': 'mine', 'he': 'his', 'she': 'hers', 'you': 'yours'}

class Pattern(object):
    def __init__(self, english, chinese, options):
        self.english = english.split(' ')
        self.chinese = chinese.split(' ')
        self.options = [categories[option] for option in options]

    def generateSentence(self):
        choices = [random.choice(word) for word in self.options]

        english = [word.startswith('#') and choices[int(word[1:])] or word for word in self.english]
        
        # Correct an/a
        for i, word in enumerate(english[:-1]):
            if word == 'a' and english[i+1].startswith(vowels):
                english[i] = 'an'
            elif '%' in word:
                pronoun =choices[int(word.split('%')[1])]
                verb = to_be.get(pronoun, 'is')
                english[i] = verb
            
        english[0] = english[0].capitalize()
        print " ".join(english)

        pinyin = [word.startswith('#') and all_words[choices[int(word[1:])]].pinyin or all_words[word].pinyin for word in self.chinese]
        print " ".join(pinyin)
        
        # Choose correct irregular verb - could do earlier

class Word(object):
    def __init__(self, hanzi, pinyin, tags=None):
        self.hanzi  = hanzi
        self.pinyin = pinyin
        
        if tags:
            self.tags = tags
        else:
            self.tags = []

def getWordsFromList(filename):
    """ Read tab-delimited file in format hanzi/pinyin/meaning/tags and create dictionary of words. """
    
    try:
        fin = open(filename)
    except IOError:
        print "Could not open word list %s" % filename
        return
    
    all_words = {}
    
    for line in fin:
        word = line.strip('\n').split('\t')
        if len(word) > 3:
            all_words[word[2]] = Word(word[0], word[1], word[3:])
        elif len(word) > 2:
            all_words[word[2]] = Word(word[0], word[1])

    return all_words

def getPatternsFromFile(filename):
    try:
        fin = open(filename)
    except IOError:
        print "Could not open word list %s" % filename
        return
    
    patterns = []
    
    for line in fin:
        temp = line.rstrip().split('\t')
        patterns.append(Pattern(english=temp[0], chinese=temp[1], options=temp[2:]))

    return patterns

def splitWordsIntoCategories(word_dict):
    """ Read a dictionary of words and split into dictionary using word tags as keys """
    
    categories = {}
    
    for meaning, word in word_dict.iteritems():
        for tag in word.tags:
            category_list = categories.get(tag, [])
            category_list.append(meaning)
            categories[tag] = category_list
    
    return categories

all_words = getWordsFromList(os.path.join('data', 'word_list.txt'))
categories = splitWordsIntoCategories(all_words)
patterns = getPatternsFromFile(os.path.join('data', 'patterns.txt'))

random_pattern = random.choice(patterns)
random_pattern.generateSentence()

