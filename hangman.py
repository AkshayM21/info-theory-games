from english_words import english_words_lower_set
import re
import sys

wordList = english_words_lower_set
wordList.add("it's")
wordList.add("he's")
wordList.add("she's")

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

    print("Your word is " + ans + "! We guessed your word in " + str(numQuestions) + " questions.")


def askNextQuestion(numQuestions, numWords, lengths, word, lieDetected, noQuestions, noChars, yesChars, puncChars):
    probabilities = countLetters("", numWords, lengths, word, noChars)
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
                for i in range(numWords):
                    regex = ""
                    for x in range(lengths[i]):
                        if word[sum(lengths[:i]) + x] == "":
                            regex += "."
                        else:
                            regex += word[sum(lengths[:i]) + x]

                    for teststr in wordList:
                        skipping = False
                        for testchr in noChars:
                            if testchr in teststr:
                                skipping = True
                        if skipping:
                            continue
                        if len(teststr) == len(regex) and re.match(regex, teststr):
                            for k in range(lengths[i]):
                                word[sum(lengths[:i]) + k] = teststr[k]
        return (numQuestions, word, lieDetected, noQuestions, noChars, yesChars)

    # print("here2 word: ")
    # print(word)
    # print("here2")


    # convert each entry in probabilities into a probability

    # guaranteed = []
    for i in range(numWords):
        for j in range(26):
            probabilities[i][j][0] = float(probabilities[i][j][0]) / probabilities[i][26]
            # if i == 0 and probabilities[i][j][1] == probabilities[i][26]:
            #     guaranteed.append(alpha[j])
            # if alpha[j] in guaranteed and probabilities[i][j][1] != probabilities[i][26]:
            #     guaranteed.remove(alpha[j])
    # print("here3")
    # print(word)

    # check 100% probability thing

    # for char in guaranteed:
    #     if char in yesChars:
    #         guaranteed.remove(char)
    # print("here4")
    # print(word)

    # guaranteed now has the list of letters that are guaranteed to be in the word/phrase

    # for char in guaranteed:
    #     for i in range(numWords):
    #         ret = checkLetter(char, i, numWords, lengths, word, noChars)
    #         if ret == False:
    #             guaranteed.remove(char)
    # print("here5")
    # print(word)

    # guaranteed has every letter we don't want to ask about now

    # print(guaranteed)
    # for char in guaranteed:
    #     for i in range(numWords):
    #         regex = ""
    #         for x in range(lengths[i]):
    #             if word[sum(lengths[:i]) + x] == "":
    #                 regex += "."
    #             else:
    #                 regex += word[sum(lengths[:i]) + x]
    #
    #         for teststr in wordList:
    #             if len(teststr) == len(regex) and re.match(regex, teststr):
    #                 if teststr.find(char) == -1:
    #                     break
    #                 else:
    #                     word[sum(lengths[:i]) + teststr.index(char)] = char
    # print("here6")
    # print(word)

    # for char in guaranteed:
    #     yesChars.append(char)
    # print("here7")
    # print(word)

    # guaranteed now has the list of letters that are guaranteed to be in the word/phrase


    counter = [[0 for _ in range(26)] for _ in range(numWords)]

    if lieDetected==False:
        for char in noQuestions:
            additionalCount = countLetters(char, numWords, lengths, word, noChars)
            for i in range(numWords):
                for j in range(26):
                    counter[i][j] += additionalCount[i][j][0]*probabilities[i][j][0]
    # print("here8")
    #
    # print(noChars)
    # print(noQuestions)
    assumingTrueCount = countLetters("", numWords, lengths, word, noChars + noQuestions)
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
                    spacePositionCounter += spaceIndices[i] + 1


                for position in temp[1:]:
                    position = int(position) - 1

                    numInFront = 0
                    for pos in puncPos:
                        if position > pos:
                            numInFront += 1

                    for pos in spaceIndices:
                        if position > pos:
                            numInFront += 1

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





def countLetters(c, numWords, lengths, word, noChars):
    ret = [[[0, 0] for _ in range(26)] for _ in range(numWords)]
    for i in range(numWords):
        ret[i].append(0)
        regex = ""
        for x in range(lengths[i]):
            if word[sum(lengths[:i])+x] == "":
                regex += "."
            else:
                regex += word[sum(lengths[:i])+x]
        # print("word: ")
        # print(word)
        # print(noChars)
        # print("regex: " + regex)

        for teststr in wordList:
            skipping = False
            for testchr in noChars:
                if testchr in teststr:
                    skipping = True
            if skipping:
                continue
            if len(teststr) == len(regex) and re.match(regex, teststr) and c in teststr:
                ret[i][-1] += 1
                for j in range(26):
                    if alpha[j] in teststr:
                        ret[i][ord(alpha[j])-ord(alpha[0])][0] += teststr.count(alpha[j])
                        ret[i][ord(alpha[j])-ord(alpha[0])][1] += 1

    return ret

# check if letter given 100% prob is in same position in each possible valid word
# c is the input letter
# i is the index of the word within which c has a 100% chance of being, corresponding to the
# appropriate index within the lengths array
# returns true if the letter is in the same unique position in each valid word, false otherwise
# def checkLetter(c, i, numWords, lengths, word, noChars):
#     regex = ""
#     for x in range(lengths[i]):
#         if word[sum(lengths[:i])+x] == "":
#             regex += "."
#         else:
#             regex += word[sum(lengths[:i])+x]
#
#     prev = -1
#     found = False
#     checked = False
#     for teststr in wordList:
#         skipping = False
#         for testchr in noChars:
#             if testchr in teststr:
#                 skipping = True
#         if skipping:
#             continue
#
#         if len(teststr) == len(regex) and re.match(regex, teststr):
#             if teststr.find(c) != -1:
#                 found = True
#             if teststr.find(c) == -1:
#                 if found:
#                     return False
#                 else:
#                     checked = True
#             elif prev == -1:
#                 if checked:
#                     return False
#                 prev = teststr.find(c)
#             elif teststr.find(c) != prev or teststr.rfind(c) != prev:
#                 return False
#             checked = True
#
#     return True


def isInt(number):
    try:
        int(number)
    except ValueError:
        return False
    else:
        return True


main()

