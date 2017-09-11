from __future__ import division
import editdistance
import pickle
from string import ascii_lowercase
import random
from collections import defaultdict
import csv

#Ratios for interpolation 
FIVE=3
FOUR=1
THREE=1
TWO=3

def train():
    count = 0
    f = open("train.txt")
    model5 = defaultdict(lambda : defaultdict(lambda : defaultdict (lambda : defaultdict(lambda : defaultdict(int)))))
    model4 = defaultdict(lambda : defaultdict (lambda : defaultdict(lambda : defaultdict(int))))
    model = defaultdict(lambda : defaultdict(lambda : defaultdict(int)))
    model1 = defaultdict(lambda : defaultdict(lambda : defaultdict(int)))
    model2 = defaultdict(lambda : defaultdict(int))
    for line in f:
        count+=1
        word = line.strip()
        model1[len(word)][word[0]][word[1]]+=1
        model2[len(word)][word[0]]+=1
        for i in range(1,len(word)-3) :
            try :
                model[word[i-1]][word[i]][word[i+1]]+=1
                model1[len(word)][word[i]][word[i+1]]+=1
                model2[len(word)][word[i]]+=1
                model4[word[i-1]][word[i]][word[i+1]][word[i+2]]+=1
                model5[word[i-1]][word[i]][word[i+1]][word[i+2]][word[i+3]]+=1
            except :
                continue
        i=len(word)-3
        model2[len(word)][word[i]]+=1
        model2[len(word)][word[i+1]]+=1
        model2[len(word)][word[i+2]]+=1
        model1[len(word)][word[i]][word[i+1]]+=1
        model1[len(word)][word[i+1]][word[i+2]]+=1
        model[word[i-1]][word[i]][word[i+1]]+=1
        model[word[i]][word[i+1]][word[i+2]]+=1
        model4[word[i-1]][word[i]][word[i+1]][word[i+2]]+=1

    return model, model1, model2, model4, model5

model, model1, model2, model4, model5 = train()

# return some letter not in guesses
def getRandomLetter(guesses):
    letters = []
    highPriorityLetters = ['a','e','o','i','u','y']
    for c in ascii_lowercase:
        letters.append(c)
    random.shuffle(letters)
    letters = highPriorityLetters + letters
    for l in letters:
        if l not in guesses:
            return l

def unigram(maskedWord, guesses, probabilities) :
    #probabilities = [0]*26
    maxProb = 0
    predictedCharacter = ''
    for i,c in enumerate(ascii_lowercase) :
        if model2[len(maskedWord)][c] > maxProb and c not in guesses:
            maxProb = model2[len(maskedWord)][c]
            predictedCharacter = c
    if predictedCharacter !='' : 
        return predictedCharacter
    else : 
        return getRandomLetter(guesses)

def fivegram(maskedWord, guesses) :
    probabilities = [0.0]*26
    maxProb = 0
    predictedCharacter = ''
    for i in range(len(maskedWord)-4) :
        if maskedWord[i] == '_' and maskedWord[i+1]!= '_' and maskedWord[i+2]!= '_' and maskedWord[i+3]!='_' and maskedWord[i+4]!='_':
            letter1 = maskedWord[i+1]
            letter2 = maskedWord[i+2]
            letter3 = maskedWord[i+3]
            letter4 = maskedWord[i+4]
            count = 0
            for c in ascii_lowercase:
                if model5[c][letter1][letter2][letter3][letter4] > 0 and c not in guesses:
                    currCount = model5[c][letter1][letter2][letter3][letter4]
                    count+=model5[c][letter1][letter2][letter3][letter4]

            for i,c in enumerate(ascii_lowercase):
                if model5[c][letter1][letter2][letter3][letter4] > 0 and c not in guesses:
                    currCount = model5[c][letter1][letter2][letter3][letter4]
                    if count > 0 : probabilities[i]+=((currCount)/(count))
                    if probabilities[i] > maxProb :
                        maxProb = probabilities[i]
                        predictedCharacter = c

        elif maskedWord[i] != '_' and maskedWord[i+1]== '_' and maskedWord[i+2]!= '_' and maskedWord[i+3]!='_' and maskedWord[i+4]!='_':
            letter1 = maskedWord[i]
            letter2 = maskedWord[i+2]
            letter3 = maskedWord[i+3]
            letter4 = maskedWord[i+4]
            count = 0
            for c in ascii_lowercase:
                if model5[letter1][c][letter2][letter3][letter4] > 0 and c not in guesses:
                    currCount = model5[letter1][c][letter2][letter3][letter4]
                    count+=model5[letter1][c][letter2][letter3][letter4]

            for i,c in enumerate(ascii_lowercase):
                if model5[letter1][c][letter2][letter3][letter4] > 0 and c not in guesses:
                    currCount = model5[letter1][c][letter2][letter3][letter4]
                    if count > 0 : probabilities[i]+=((currCount)/(count))
                    if probabilities[i] > maxProb :
                        maxProb = probabilities[i]
                        predictedCharacter = c

        elif maskedWord[i] != '_' and maskedWord[i+1]!= '_' and maskedWord[i+2]== '_' and maskedWord[i+3]!='_' and maskedWord[i+4]!='_':
            letter1 = maskedWord[i]
            letter2 = maskedWord[i+1]
            letter3 = maskedWord[i+3]
            letter4 = maskedWord[i+4]
            count = 0
            for c in ascii_lowercase:
                if model5[letter1][letter2][c][letter3][letter4] > 0 and c not in guesses:
                    currCount = model5[letter1][letter2][c][letter3][letter4]
                    count+=model5[letter1][letter2][c][letter3][letter4]

            for i,c in enumerate(ascii_lowercase):
                if model5[letter1][letter2][c][letter3][letter4] > 0 and c not in guesses:
                    currCount = model5[letter1][letter2][c][letter3][letter4]
                    if count > 0 : probabilities[i]+=((currCount)/(count))
                    if probabilities[i] > maxProb :
                        maxProb = probabilities[i]
                        predictedCharacter = c

        elif maskedWord[i] != '_' and maskedWord[i+1]!= '_' and maskedWord[i+2]!= '_' and maskedWord[i+3]=='_' and maskedWord[i+4]!='_':
            letter1 = maskedWord[i]
            letter2 = maskedWord[i+1]
            letter3 = maskedWord[i+2]
            letter4 = maskedWord[i+4]
            count = 0
            for c in ascii_lowercase:
                if model5[letter1][letter2][letter3][c][letter4] > 0 and c not in guesses:
                    currCount = model5[letter1][letter2][letter3][c][letter4]
                    count+=model5[letter1][letter2][letter3][c][letter4]

            for i,c in enumerate(ascii_lowercase):
                if model5[letter1][letter2][letter3][c][letter4] > 0 and c not in guesses:
                    currCount = model5[letter1][letter2][letter3][c][letter4]
                    if count > 0 : probabilities[i]+=((currCount)/(count))
                    if probabilities[i] > maxProb :
                        maxProb = probabilities[i]
                        predictedCharacter = c

        elif maskedWord[i] != '_' and maskedWord[i+1]!= '_' and maskedWord[i+2]!= '_' and maskedWord[i+3]!='_' and maskedWord[i+4]=='_':
            letter1 = maskedWord[i]
            letter2 = maskedWord[i+1]
            letter3 = maskedWord[i+2]
            letter4 = maskedWord[i+3]
            count = 0
            for c in ascii_lowercase:
                if model5[letter1][letter2][letter3][letter4][c] > 0 and c not in guesses:
                    currCount = model5[letter1][letter2][letter3][letter4][c]
                    count+=model5[letter1][letter2][letter3][letter4][c]

            for i,c in enumerate(ascii_lowercase):
                if model5[letter1][letter2][letter3][letter4][c] > 0 and c not in guesses:
                    currCount = model5[letter1][letter2][letter3][letter4][c]
                    if count > 0 : probabilities[i]+=((currCount)/(count))
                    if probabilities[i] > maxProb :
                        maxProb = probabilities[i]
                        predictedCharacter = c

    for i,item in enumerate(probabilities) :
        probabilities[i] = item*FIVE
    return fourgram(maskedWord, guesses, probabilities)

def fourgram(maskedWord, guesses, probabilities1) :
    probabilities = [0.0]*26
    maxProb = 0
    predictedCharacter = ''
    for i in range(len(maskedWord)-3) :
        if maskedWord[i] == '_' and maskedWord[i+1]!= '_' and maskedWord[i+2]!= '_' and maskedWord[i+3]!='_':
            letter1 = maskedWord[i+1]
            letter2 = maskedWord[i+2]
            letter3 = maskedWord[i+3]
            count = 0
            for c in ascii_lowercase:
                if model4[c][letter1][letter2][letter3] > 0 and c not in guesses:
                    currCount = model4[c][letter1][letter2][letter3]
                    count+=model4[c][letter1][letter2][letter3]

            for i,c in enumerate(ascii_lowercase):
                if model4[c][letter1][letter2][letter3] > 0 and c not in guesses:
                    currCount = model4[c][letter1][letter2][letter3]
                    if count > 0 : probabilities[i]+=((currCount)/(count))
                    if probabilities[i] > maxProb :
                        maxProb = probabilities[i]
                        predictedCharacter = c

        elif maskedWord[i] != '_' and maskedWord[i+1]== '_' and maskedWord[i+2]!= '_' and maskedWord[i+3]!='_':
            letter1 = maskedWord[i]
            letter2 = maskedWord[i+2]
            letter3 = maskedWord[i+3]
            count = 0
            for c in ascii_lowercase:
                if model4[letter1][c][letter2][letter3] > 0 and c not in guesses:
                    currCount = model4[letter1][c][letter2][letter3]
                    count+=model4[letter1][c][letter2][letter3]

            for i,c in enumerate(ascii_lowercase):
                if model4[letter1][c][letter2][letter3] > 0 and c not in guesses:
                    currCount = model4[letter1][c][letter2][letter3]
                    if count > 0 : probabilities[i]+=((currCount)/(count))
                    if probabilities[i] > maxProb :
                        maxProb = probabilities[i]
                        predictedCharacter = c

        elif maskedWord[i] != '_' and maskedWord[i+1]!= '_' and maskedWord[i+2]== '_' and maskedWord[i+3]!='_':
            letter1 = maskedWord[i]
            letter2 = maskedWord[i+1]
            letter3 = maskedWord[i+3]
            count = 0
            for c in ascii_lowercase:
                if model4[letter1][letter2][c][letter3] > 0 and c not in guesses:
                    currCount = model4[letter1][letter2][c][letter3]
                    count+=model4[letter1][letter2][c][letter3]

            for i,c in enumerate(ascii_lowercase):
                if model4[letter1][letter2][c][letter3] > 0 and c not in guesses:
                    currCount = model4[letter1][letter2][c][letter3]
                    if count > 0 : probabilities[i]+=((currCount)/(count))
                    if probabilities[i] > maxProb :
                        maxProb = probabilities[i]
                        predictedCharacter = c

        elif maskedWord[i] != '_' and maskedWord[i+1]!= '_' and maskedWord[i+2]!= '_' and maskedWord[i+3]=='_':
            letter1 = maskedWord[i]
            letter2 = maskedWord[i+1]
            letter3 = maskedWord[i+3]
            count = 0
            for c in ascii_lowercase:
                if model4[letter1][letter2][c][letter3] > 0 and c not in guesses:
                    currCount = model4[letter1][letter2][c][letter3]
                    count+=model4[letter1][letter2][c][letter3]

            for i,c in enumerate(ascii_lowercase):
                if model4[letter1][letter2][c][letter3] > 0 and c not in guesses:
                    currCount = model4[letter1][letter2][c][letter3]
                    if count > 0 : probabilities[i]+=((currCount)/(count))
                    if probabilities[i] > maxProb :
                        maxProb = probabilities[i]
                        predictedCharacter = c

    for i,item in enumerate(probabilities) :
        probabilities[i] = item*FOUR + probabilities1[i]
    return trigram(maskedWord, guesses, probabilities)

def trigram(maskedWord, guesses, probabilities1) :
    probabilities = [0.0]*26
    maxProb = 0
    predictedCharacter = ''
    for i in range(len(maskedWord)-2) :
        if maskedWord[i] == '_' and maskedWord[i+1]!= '_' and maskedWord[i+2]!= '_':
            letter1 = maskedWord[i+1]
            letter2 = maskedWord[i+2]
            count = 0
            for c in ascii_lowercase:
                if model[c][letter1][letter2] > 0 and c not in guesses:
                    currCount = model[c][letter1][letter2]
                    count+=model[c][letter1][letter2]

            for i,c in enumerate(ascii_lowercase):
                if model[c][letter1][letter2] > 0 and c not in guesses:
                    currCount = model[c][letter1][letter2]
                    if count > 0 : probabilities[i]+=((currCount)/(count))
                    if probabilities[i] > maxProb :
                        maxProb = probabilities[i]
                        predictedCharacter = c

        elif maskedWord[i] != '_' and maskedWord[i+1]== '_' and maskedWord[i+2]!= '_':
            letter1 = maskedWord[i]
            letter2 = maskedWord[i+2]
            count = 0
            for c in ascii_lowercase:
                if model[letter1][c][letter2] > 0 and c not in guesses:
                    currCount = model[letter1][c][letter2]
                    count+=model[letter1][c][letter2]

            for i,c in enumerate(ascii_lowercase):
                if model[letter1][c][letter2] > 0 and c not in guesses:
                    currCount = model[letter1][c][letter2]
                    if count > 0 : probabilities[i]+=((currCount)/(count))
                    if probabilities[i] > maxProb :
                        maxProb = probabilities[i]
                        predictedCharacter = c

        elif maskedWord[i] != '_' and maskedWord[i+1]!= '_' and maskedWord[i+2]== '_':
            letter1 = maskedWord[i]
            letter2 = maskedWord[i+1]
            count = 0
            for c in ascii_lowercase:
                if model[letter1][letter2][c] > 0 and c not in guesses:
                    currCount = model[letter1][letter2][c]
                    count+=model[letter1][letter2][c]

            for i,c in enumerate(ascii_lowercase):
                if model[letter1][letter2][c] > 0 and c not in guesses:
                    currCount = model[letter1][letter2][c]
                    if count > 0 : probabilities[i]+=((currCount)/(count))
                    if probabilities[i] > maxProb :
                        maxProb = probabilities[i]
                        predictedCharacter = c

    for i,item in enumerate(probabilities) :
        probabilities[i] = item*THREE + probabilities1[i]
    return bigram(maskedWord, guesses, probabilities)

def bigram(maskedWord, guesses, probabilities1) :
    probabilities = [0.0]*26
    indexList = []
    indexList1 = []
    maskCount = 0
    for i in range(len(maskedWord)-1) :
        if maskedWord[i] != '_' and maskedWord[i+1] == '_' :
            indexList.append(i)

    for i in range(1,len(maskedWord)) :
        if maskedWord[i] != '_' and maskedWord[i-1] == '_' :
            indexList1.append(i)

    maxProb = 0
    predictedCharacter = ''
    for item in indexList :
        currentLetter = maskedWord[item]
        count = 0
        for c in ascii_lowercase:
            if model1[len(maskedWord)][currentLetter][c] > 0 and c not in guesses:
                currCount = model1[len(maskedWord)][currentLetter][c]
                count+=model1[len(maskedWord)][currentLetter][c]

        for i,c in enumerate(ascii_lowercase):
            if model1[len(maskedWord)][currentLetter][c] > 0 and c not in guesses:
                currCount = model1[len(maskedWord)][currentLetter][c]
                probabilities[i]+=( (currCount/count) )
                if probabilities[i] > maxProb :
                    maxProb = probabilities[i]
                    predictedCharacter = c

    for item in indexList1 :
        currentLetter = maskedWord[item]
        count = 0
        for c in ascii_lowercase:
            if model1[len(maskedWord)][c][currentLetter] > 0 and c not in guesses:
                currCount = model1[len(maskedWord)][c][currentLetter]
                count+=model1[len(maskedWord)][c][currentLetter]

        for i,c in enumerate(ascii_lowercase):
            if model1[len(maskedWord)][c][currentLetter] > 0 and c not in guesses:
                currCount = model1[len(maskedWord)][c][currentLetter]
                probabilities[i]+=( (currCount/count) )
                if probabilities[i] > maxProb :
                    maxProb = probabilities[i]
                    predictedCharacter = c

    for i,item in enumerate(probabilities) :
        probabilities[i] = item*TWO + probabilities1[i]
        if probabilities[i] > maxProb : 
            maxProb = probabilities[i]
            predictedCharacter = ascii_lowercase[i]

    if maxProb > 0 : 
        return predictedCharacter
    else : 
        return unigram(maskedWord, guesses, probabilities)

def hangman(solution):
    guesses = []
    wrongGuess = 0
    maskedWord = ['_']*len(solution)
    while wrongGuess < 8 and '_' in maskedWord:
        predictedCharacter = fivegram(maskedWord, guesses)
        if predictedCharacter not in guesses:
            guesses.append(predictedCharacter)
        if predictedCharacter in solution:
            for i in range(0, len(solution)):
                if solution[i] == predictedCharacter:
                    maskedWord[i] = predictedCharacter
        else:
            wrongGuess += 1

    return maskedWord, guesses

def loss(solution, prediction):
    # find the levenshtein distance between the two words
    return editdistance.eval(solution, prediction)


count = 0
distance = 0.0
with open("test.txt","r") as infile :
    with open('output.tsv', 'wb') as tsvfile:
        spamwriter = csv.writer(tsvfile, delimiter='\t')
        spamwriter.writerow(["Id","Output","PredictedCharacters"])
        for line in infile:
            line = line.strip().split(',')[1]
            count += 1
            if count==1 : continue
            print count
            predictedWord = ""
            maskedWord, guesses = hangman(line)
            for item in maskedWord :
                predictedWord+=item
            if predictedWord != line : print predictedWord,line,guesses
            distance += loss(line, predictedWord)
            spamwriter.writerow([count-1,predictedWord,guesses])
print distance/(count-1)