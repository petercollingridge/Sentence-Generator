import os
import random

# Fix subject pronouns I->me, he->him 
# Add final punctuation
# Possesives
# Add buzai - not ... anymore
# Add yizhi - always
# Add optional options e.g. negation, also
# Catch errors if categories not defined
# Associate verbs with relevant nouns

vowels = ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
to_be = {'I': 'am', 'you': 'are', 'you (polite)': 'are'}
do = {'I': 'do', 'you': 'do'}
pronoun_subj_obj = {'I': 'me', 'he': 'him', 'she': 'her'}
possesive = {'I': 'mine', 'he': 'his', 'she': 'hers', 'you': 'yours'}

class Pattern(object):
    def __init__(self, english, chinese, options):
        self.english = english.rstrip().split(' ')
        self.chinese = chinese.rstrip().split(' ')
        
        self.options = []
        for option in options.split('\t'):
            all_options = []
            for sub_option in option.split('/'):
                all_options.extend(categories[sub_option])
            self.options.append(all_options)

    def generateSentence(self):
        choices = [random.choice(word) for word in self.options]
        chinese = [word.startswith('#') and word_dict[choices[int(word[1:])]] or word_dict[word] for word in self.chinese]
        english = [word.startswith('#') and word_dict[choices[int(word[1:])]].meaning or word for word in self.english]
        
        # Correct an/a
        for i, word in enumerate(english[:-1]):
            if word == 'a' and english[i+1].startswith(vowels):
                english[i] = 'an'
            elif '%' in word:
                pronoun = word_dict[choices[int(word.split('%')[1])]].meaning
                verb = to_be.get(pronoun, 'is')
                english[i] = verb
            
        english[0] = english[0].capitalize()

        return (english, chinese)

class Word(object):
    def __init__(self, hanzi, pinyin, tags=None):
        self.hanzi  = hanzi
        self.pinyin = pinyin
        
        if tags:
            self.tags = tags
        else:
            self.tags = []

class Hanzi(object):
    def __init__(self, pinyin, meaning, tags=None):
        self.pinyin = pinyin
        self.meaning = meaning
        self.tags = []

    def addTags(self, tags):
        self.tags.extend(tags)
        
def getWordsFromList(filename):
    """ Read tab-delimited file in format hanzi/pinyin/meaning/tags
        and create dictionary of words with hanzi as keys. """
    
    try:
        fin = open(filename)
    except IOError:
        print "Could not open word list %s" % filename
        return
    
    word_dict = {}
    
    for line in fin:
        word = line.strip('\n').split('\t')
        new_word = Hanzi(word[1], word[2])
        word_dict[word[0]] = new_word
        
        if len(word) > 3:
            new_word.addTags(word[3:])

    return word_dict

def getPatternsFromFile(filename):
    try:
        fin = open(filename)
    except IOError:
        print "Could not open word list %s" % filename
        return
    
    patterns = []
    
    for line in fin:
        temp = line.rstrip().split('|')
        patterns.append(Pattern(english=temp[0], chinese=temp[1], options=temp[2]))

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

word_dict = getWordsFromList(os.path.join('data', 'word_list.txt'))
categories = splitWordsIntoCategories(word_dict)

if __name__ == '__main__':
    patterns = getPatternsFromFile(os.path.join('data', 'patterns.txt'))
    random_pattern = random.choice(patterns)
    random_pattern.generateSentence()

