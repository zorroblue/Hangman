import editdistance

def model(maskedWord, guesses):
    # create model here
    return predictedCharacter

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
            for i in range(0, len(solution)):
                if solution[i] == predictedCharacter:
                    maskedWord[i] = predictedCharacter
        else:
            wrongGuess += 1

    return maskedWord, guesses

def loss(solution, prediction):
    # find the levenshtein distance between the two words
    return editdistance(solution, prediction)



