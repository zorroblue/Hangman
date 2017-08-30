import editdistance
import operator
import cPickle as pickle
from string import ascii_lowercase
import string
import random
from nltk.util import ngrams
from random import randint

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
       
    f = open("letter_freq_model.pkl","wb")
    print count
    pickle.dump(model, f, -1) 
    return model

def train_ngrams():
    f = open("train.txt")
    reverse_model = {}
    reverse_model[2] = {}
    reverse_model[3] = {}
    reverse_model[4] = {}
    reverse_model[5] = {}
    model = {}
    model[2] = {}
    model[3] = {}
    model[4] = {}
    model[5] = {}
    for line in f:
        line = line.strip()
        bigrams = ngrams(line, 2)
        trigrams = ngrams(line, 3)
        quadgrams = ngrams(line, 4)
        pentagrams = ngrams(line, 5)
        for bigram in bigrams:
            a,b = bigram
            if a not in model[2]:
                model[2][a] = {}
            if b not in model[2][a]:
                model[2][a][b] = 0
            model[2][a][b] += 1
            b,a = bigram
            if a not in reverse_model[2]:
                reverse_model[2][a] = {}
            if b not in reverse_model[2][a]:
                reverse_model[2][a][b] = 0
            reverse_model[2][a][b] += 1

        for trigram in trigrams:
            a,b,c = trigram
            a = (a,b)
            b = c
            if a not in model[3]:
                model[3][a] = {}
            if b not in model[3][a]:
                model[3][a][b] = 0
            model[3][a][b] += 1
            x,b,c = trigram
            a = (b,c)
            b = x
            if a not in reverse_model[3]:
                reverse_model[3][a] = {}
            if b not in reverse_model[3][a]:
                reverse_model[3][a][b] = 0
            reverse_model[3][a][b] += 1

        for quadgram in quadgrams:
            a,b,c,d = quadgram
            a = (a,b,c)
            b = d
            if a not in model[4]:
                model[4][a] = {}
            if b not in model[4][a]:
                model[4][a][b] = 0
            model[4][a][b] += 1
            x,b,c,d = quadgram
            a = (b,c,d)
            b = x
            if a not in reverse_model[4]:
                reverse_model[4][a] = {}
            if b not in reverse_model[4][a]:
                reverse_model[4][a][b] = 0
            reverse_model[4][a][b] += 1

        for pentagram in pentagrams:
            a,b,c,d,e = pentagram
            a = (a,b,c,d)
            b = d
            if a not in model[5]:
                model[5][a] = {}
            if b not in model[5][a]:
                model[5][a][b] = 0
            model[5][a][b] += 1
            x,b,c,d,e = pentagram
            a = (b,c,d,e)
            b = x
            if a not in reverse_model[5]:
                reverse_model[5][a] = {}
            if b not in reverse_model[5][a]:
                reverse_model[5][a][b] = 0
            reverse_model[5][a][b] += 1
    f = open("ngram_model.pkl","wb")
    pickle.dump((model,reverse_model), f, -1)
    print "N-Grams training complete"

#train_letterfrequency()
#train_ngrams()
ngram_model, ngram_reverse_model = pickle.load(open('ngram_model.pkl'))
letter_freq_model = pickle.load(open('letter_freq_model.pkl'))


def use_letter_freq(size, guesses):
    for k,v in sorted(letter_freq_model[size].items(), key=operator.itemgetter(1), reverse=True):
        if k not in guesses:
            #print "Using letter"
            return k
            break
    return random.choice(string.letters)

def model(maskedWord, guesses):
    # N-Grams without length
    size = len(maskedWord)
    #print maskedWord
    if maskedWord == '_'*len(maskedWord):
        # cold start
        for k, v in sorted(letter_freq_model[size].items(), key=operator.itemgetter(1), reverse=True):
            if k not in guesses:
                return k
        return random.choice(string.letters)
    else:
        #print maskedWord
        j = len(maskedWord)-1
        choice = randint(0,1)
        # if choice == 1:
        #     w = reversed(range(0, len(maskedWord)))
        # else:
        #     w = range(0, len(maskedWord))
        for i in reversed(range(0, len(maskedWord))):
            if i == 0 and maskedWord[i] == '_':
                count = 1
                maxi = 0
                prev = []
                while count<min(5,len(maskedWord)) and maskedWord[count] != '_':
                    prev.append(maskedWord[count])
                    count+=1 
                count-=1
                if count == 0:
                    return use_letter_freq(size, guesses)
                count = min(count,4)
                prev = tuple(prev[:count])
                count+=1
                if prev[:(count-1)] not in ngram_reverse_model[count]:
                    while count>=2:
                        if prev[:(count-1)] in ngram_reverse_model[count]:
                            for k,v in sorted(ngram_reverse_model[count][prev[:(count-1)]].items(), key=operator.itemgetter(1), reverse=True):
                                #print "Option : ", k, count
                                if k not in guesses:
                                    #print "Returning ", k
                                    return k
                        count -= 1
                    return use_letter_freq(size, guesses)
                for k,v in sorted(ngram_reverse_model[count][prev].items(), key=operator.itemgetter(1), reverse=True):
                    if k not in guesses:
                        #print "Returning1 ", k
                        return k
            if maskedWord[i] == '_':
                count = 0
                j = i-1
                prev = []
                while j>=0 and maskedWord[j] != '_' and count<=3:
                    j -= 1
                    count += 1
                    prev.append(maskedWord[j])
                if len(prev) != 0:
                    prev.reverse()
                    prev = tuple(prev)
                else:
                    prev = ()
                if count == 0 or prev not in ngram_model[count+1]:
                    return use_letter_freq(size, guesses)
                count += 1
                for k,v in sorted(ngram_model[count][prev].items(), key=operator.itemgetter(1), reverse=True):
                    if k not in guesses:
                        #print 'Returning1'
                        return k
        return use_letter_freq(size, guesses)    



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
        #print maskedWord, wrongGuess

    return maskedWord, guesses

def loss(solution, prediction):
    # find the levenshtein distance between the two words
    count = 0
    for i in range(0, len(solution)):
        if solution[i] != prediction[i]:
            count+=1
    return count

f = open("test.txt")
count = 0.0
distance = 0.0
for line in f:
    line = line.strip().split(',')[1]
    count += 1
    if count == 1:
        continue
    predictedWord, guesses = hangman(line)
    print predictedWord, line
    l = loss(line, predictedWord)
    distance += l
print distance/count