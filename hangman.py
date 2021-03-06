import re
import sys

wordList = []
with open('word_list.txt') as filein:
    wordList = set(filein.read().split())

alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
         's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def main():

    numQuestions = 0
    numWords = 0
    lengths = []
    word = []
    lieDetected = False

    puncChars = [] # stores an array of tuples of (character position in the final word/phrase,
                   # punctuation mark)

    yesChars = [] # stores each letter which has been confirmed to be in the word/phrase

    noQuestions = [] # stores each letter which has been said is not in the word/phrase but is not
                     # confirmed to be or not to be in the word/phrase

    noChars = [] # stores each letter which has been confirmed to not be in the word/phrase

    print("Hello! Welcome to Hangman, a game in which we attempt to not hang an entire person while hanging part of a person is ok.")
    print("Please enter the number of words in your selected word/phrase followed by the number of letters in each word (including punctuation that is part of the word), all separated by a space")
    print("(e.g. 3 3 7 5 could signify the phrase \"low hanging fruit\"): ")

    temp = list(map(int, sys.stdin.readline()[:-1].split(" ")))
    numWords = temp[0]
    lengths = temp[1:]

    for i in range(numWords):
        for j in range(lengths[i]):
            word.append("")

    print("Are there any punctuation marks in your words (e.g. apostrophes but not including punctuation such as commas between words)? Please enter y/n: ")
    temp2 = sys.stdin.readline()[:-1]
    if (temp2[0].lower() == 'y'):
        print("Please enter the punctuation character followed by each character position (1-indexed, when excluding spaces and punctuation between words) of that punctuation character, all separated by a space")
        print("(e.g. \"' 3 10\" could signify \"it's, doesn't\"): ")
        temp3 = list(sys.stdin.readline()[:-1].split(" "))
        char = ""
        for x in temp3:
            if isInt(x):
                word[int(x)-1] = char
            else:
                char = x

    print("Are there any punctuation marks in between your words (e.g. commas or an exclamation point at the end)? (y/n): ")
    temp4 = sys.stdin.readline()[:-1]
    if (temp4[0].lower() == 'y'):
        print("Please enter the punctuation character followed by each character position (1-indexed, when including spaces and punctuation between words) of that punctuation character, all separated by a space")
        print("(e.g. \", 6 11\" could signify \"hello, bob,\"): ")
        temp5 = list(sys.stdin.readline()[:-1].split(" "))
        char = ""
        for x in temp5:
            if isInt(x):
                puncChars.append((int(x)-1, char))
            else:
                char = x
    puncChars.sort()

    done = False

    while not done:
        (numQuestions, word, lieDetected, noQuestions, noChars, yesChars) = askNextQuestion(numQuestions, numWords, lengths, word, lieDetected, noQuestions, noChars, yesChars, puncChars)
        done = word.count("")==0

    ans = ""
    charCount = 0
    currPuncPos = 0
    for i in range(numWords):
        for j in range(lengths[i]):
            ans += word[sum(lengths[:i])+j]
            charCount += 1
        if (currPuncPos < len(puncChars) and charCount == puncChars[currPuncPos][0]):
            ans += puncChars[currPuncPos][1]
            charCount += 1
            currPuncPos += 1
        assert currPuncPos >= len(puncChars) or charCount < puncChars[currPuncPos][0]
        ans += " "
        charCount += 1

    print("Your word/phrase is \"" + ans[:-1] + "\"! We guessed your word/phrase in " + str(numQuestions) + " questions.")


def askNextQuestion(numQuestions, numWords, lengths, word, lieDetected, noQuestions, noChars, yesChars, puncChars):
    probabilities = countLetters("", numWords, lengths, word, noChars, yesChars)
    # print("here1")

    #****** check if there's only one word possible then guess that if so
    #27th entry is # of valid words
    onePossibles = 0
    for arr in probabilities:
        if arr[26]!=1: #check number of words
            break
        onePossibles += 1
    if onePossibles == numWords:
        # check if there's only one word possible then guess that if so
        for j in range(numWords):
            if (probabilities[j][26] != 1):
                break
            if (j == numWords - 1):
                excludeString = ""
                for yesCharacter in yesChars:
                    excludeString += yesCharacter
                for noCharacter in noChars:
                    excludeString += noCharacter

                for i in range(numWords):
                    regex = ""
                    for x in range(lengths[i]):
                        if word[sum(lengths[:i])+x] == "":
                            if excludeString == "":
                                regex += "."
                            else:
                                regex += "[^"+excludeString+"]"
                        else:
                            regex += word[sum(lengths[:i])+x]

                    for teststr in wordList:
                        if re.fullmatch(regex, teststr):
                            for k in range(lengths[i]):
                                word[sum(lengths[:i]) + k] = teststr[k]
        return (numQuestions, word, lieDetected, noQuestions, noChars, yesChars)

    # print("here2 word: ")
    # print(word)
    # print("here2")


    # convert each entry in probabilities into a probability
    for i in range(numWords):
        for j in range(26):
            if probabilities[i][26] == 0:
                print("Error: word " + str(i+1) + " not in local dictionary.")
                sys.exit()
            probabilities[i][j][0] = float(probabilities[i][j][0]) / probabilities[i][26]

    counter = [[0 for _ in range(26)] for _ in range(numWords)]

    if lieDetected==False:
        for char in noQuestions:
            tempNoQuestions = noQuestions.copy()
            tempNoQuestions.remove(char)
            # print("noQuestions: ")
            # print(noQuestions)
            # print("tempNoQuestions: ")
            # print(tempNoQuestions)
            additionalCount = countLetters(char, numWords, lengths, word, noChars+tempNoQuestions, yesChars)
            for i in range(numWords):
                for j in range(26):
                    counter[i][j] += additionalCount[i][j][0]*probabilities[i][j][0]
    # print("here8")
    # print(noChars)
    # print(noQuestions)
    assumingTrueCount = countLetters("", numWords, lengths, word, noChars + noQuestions, yesChars)
    #now, assuming all the no's were legit
    for i in range(numWords):
        multiplier = 1 - sum([probabilities[i][alpha.index(noQuestionChar)][0] for noQuestionChar in noQuestions])
        for j in range(26):
            counter[i][j] += assumingTrueCount[i][j][0] * multiplier
    # print("here9")

    #sum it up
    summedCounts = [0]*26
    for j in range(26):
        for i in range(numWords):
            summedCounts[j] += counter[i][j]
    # print("here10")

    #rank highest indices
    alphabet = alpha[:]
    sorted_alphabet = [x for _, x in sorted(zip(summedCounts, alphabet))]

    sorted_counts = [y for y, x in sorted(zip(summedCounts, alphabet))]
    # print(sorted_alphabet)
    # print(sorted_counts)

    #ask most probable letter
    for char in sorted_alphabet[::-1]:
        if char not in yesChars and char not in noChars:
            #this is the best one to guess
            print("Question "+str(numQuestions+1)+": Is there a "+char+"? If yes, please send each position separated by spaces (no brackets or commas).")
            numQuestions += 1
            temp = list(sys.stdin.readline().split(" "))
            if (temp[0].lower() == 'y'):
                #read in the positions
                yesChars.append(char)

                numPuncChars = len(puncChars)
                totalPhraseLength = len(word) + numWords - 1 + numPuncChars
                additionalCharactersAdded = 0  # refers to the number of spaces and puncChars that we've gone past

                puncPos = [pos for (pos, punctuation) in puncChars]

                spaceIndices = [0]*(numWords-1)
                spacePositionCounter = 0
                for i in range(len(lengths)-1):
                    spaceIndices[i] = lengths[i] + spacePositionCounter
                    spacePositionCounter = spaceIndices[i] + 1

                # print("spaceIndices: ")
                # print(spaceIndices)


                for position in temp[1:]:
                    position = int(position) - 1

                    numInFront = 0
                    for pos in puncPos:
                        if position > pos:
                            # print("adding punc in front")
                            numInFront += 1

                    for pos in spaceIndices:
                        if position > pos:
                            numInFront += 1

                    # print("numInFront: " + str(numInFront))
                    #spaces using lengths
                    #puncChars has the positions
                    word[position-numInFront] = char
                    # print("position-numInFront: " + str(position-numInFront))
                if char in noQuestions:
                    lieDetected = True
                    noQuestions.remove(char)
            else:
                if lieDetected:
                    noChars.append(char)
                elif char in noQuestions:
                    noQuestions.remove(char)
                    noChars.append(char)
                else:
                    noQuestions.append(char)
            break


    return (numQuestions, word, lieDetected, noQuestions, noChars, yesChars)

    #*****return everything
    #****update main method


    #take counter and sum acorss the words and then choose the highest one that isnt in yes chars and no chars
    #then put in question logic
    #and do lie detection logic
    #take into account question position



    #make sure to check that its not in yesChars
    # iterate through noQuestions and run countLetters passing in the letter from that question
    # update counter accordingly

    # ask the next question about the letter with the maximum counter value (with question Number)
    # check if the letter is in noQuestions to detect a lie (and update lieDetected if needed)
    # update noQuestions if no
    # update word and yesChars with the appropriate positions/chars if the answer is yes





def countLetters(c, numWords, lengths, word, noChars, yesChars):
    ret = [[[0, 0] for _ in range(26)] for _ in range(numWords)]
    excludeString = ""
    for yesCharacter in yesChars:
        excludeString += yesCharacter
    for noCharacter in noChars:
        excludeString += noCharacter

    for i in range(numWords):
        ret[i].append(0)
        regex = ""
        for x in range(lengths[i]):
            if word[sum(lengths[:i])+x] == "":
                if excludeString == "":
                    regex += "."
                else:
                    regex += "[^"+excludeString+"]"
            else:
                regex += word[sum(lengths[:i])+x]

        # print("word: ")
        # print(word)
        # print("yesChars: ")
        # print(yesChars)
        # print("noChars: ")
        # print(noChars)
        # print("char: " + c)
        print("regex: " + regex)

        for teststr in wordList:
            if re.fullmatch(regex, teststr) and c in teststr:
                ret[i][-1] += 1
                for j in range(26):
                    if alpha[j] in teststr:
                        ret[i][ord(alpha[j])-ord(alpha[0])][0] += teststr.count(alpha[j])
                        ret[i][ord(alpha[j])-ord(alpha[0])][1] += 1

    return ret

def isInt(number):
    try:
        int(number)
    except ValueError:
        return False
    else:
        return True


main()

