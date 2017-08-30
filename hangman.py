import editdistance
import operator
import cPickle as pickle
from string import ascii_lowercase
import random
from nltk.util import ngrams

def train_letterfrequency():
    count = 0
    f = open("train.txt")
    model = {}
    for line in f:
        count+=1
        word = line.strip().split()[0]
        if len(word) not in model:
            model[len(word)] = {}
        for c in word:
            if c not in model[len(word)]:
                model[len(word)][c] = 1
            else:
                model[len(word)][c] += 1
       
    f = open("model.pkl","wb")
    print count
    pickle.dump(model, f, -1) 
    return model

def train_ngrams():
    count = 0
    f = open("train.txt")
    bigram_model = {}
    for line in f:
        count+=1
        word = line.strip().split()[0]
        if len(word) not in bigram_model:
            bigram_model[len(word)] = {}
        chars = [c for c in word]
        bigrams = ngrams(chars,2)
        for bigram in bigrams:
            if bigram[0] not in bigram_model[len(word)]:
                bigram_model[len(word)][bigram[0]] = {}
            if bigram[1] not in bigram_model[len(word)][bigram[0]]:
                bigram_model[len(word)][bigram[0]][bigram[1]] = 0
            bigram_model[len(word)][bigram[0]][bigram[1]] += 1
    f = open("bigram_model.pkl","wb")
    print count
    pickle.dump(bigram_model, f, -1) 
    return bigram_model


train_letterfrequency()
train_ngrams()
letter_freq_model = pickle.load(open("model.pkl"))
trained_model = pickle.load(open('bigram_model.pkl'))

 # return some letter not in guesses
def getRandomLetter(guesses):
    letters = []
    for c in ascii_lowercase:
        letters.append(c)
    random.shuffle(letters)
    for l in letters:
        if l not in guesses:
            return l

def use_letter_freq(size, guesses):
    for k,v in sorted(letter_freq_model[size].items(), key=operator.itemgetter(1), reverse=True):
        if k not in guesses:
            return k
            break
    return getRandomLetter(guesses)

def model(maskedWord, guesses):
    # create model here
    size = len(maskedWord)
    if size not in trained_model:
        return getRandomLetter(guesses)

    # for dry start (all _)
    if len(maskedWord) == maskedWord.count('_'):
        # guess the most common letter in words of that length
        return use_letter_freq(size, guesses)
    
    # for further guesses, use a bigram model
    for i in range(0, len(maskedWord)):
        if maskedWord[i] == '_':
            if i == 0 or maskedWord[i-1] == '_':
                continue
            for k,v in sorted(trained_model[size][maskedWord[i-1]].items(), key=operator.itemgetter(1), reverse=True):
                if k not in guesses:
                    return k
                    break
            break
    
    if maskedWord[i] == '_':
        return use_letter_freq(size, guesses)
    
    return getRandomLetter(guesses)

def hangman(solution):
    guesses = {}
    wrongGuess = 0
    maskedWord = "_"*len(solution)
    while wrongGuess < 8 and '_' in maskedWord:
        predictedCharacter = model(maskedWord, guesses)
        if predictedCharacter in guesses:
            continue
        guesses[predictedCharacter] = 1
        if predictedCharacter in solution:
            chars = list(maskedWord)
            for i in range(0, len(solution)):
                if solution[i] == predictedCharacter:
                    chars[i] = predictedCharacter
            maskedWord = ''.join(chars)
        else:
            wrongGuess += 1

    return maskedWord, guesses

def loss(solution, prediction):
    # find the levenshtein distance between the two words
    return editdistance.eval(solution, prediction)

f = open("test.txt")
count = 0.0
distance = 0.0
for line in f:
    line = line.strip().split(',')[1]
    count += 1
    if count == 1:
        continue
    predictedWord, guesses = hangman(line)
    distance += loss(line, predictedWord)
print distance/count