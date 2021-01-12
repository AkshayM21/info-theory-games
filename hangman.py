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
            if x.isnumeric():
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
            if x.isnumeric():
                puncChars.append((int(x)-1, char))
            else:
                char = x
    puncChars.sort()

    done = False

    while not done:
        askNextQuestion(numQuestions, numWords, lengths, word, lieDetected)
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


def askNextQuestion(numQuestions, numWords, lengths, word, lieDetected):
    probabilities = countLetters("", numWords, lengths, word)

    # check if there's only one word possible then guess that if so
    if word.count("")==1:
        numZeros = 0
        nonZeroCount = 0
        for count in probabilities[word.index("")]:
            if count==0:
                numZeros += 1
            else:
                nonZeroCount += count
        if numZeros==25: #magic number but basically checking if there's only 1 letter possible)
            print("Is the remaining letter "+str(alpha[probabilities[word.index("")].index(nonZeroCount)])+"?")
            temp = input()
            numQuestions += 1
            if (lower(temp[0]) == 'n'):
                #ruh roh
                print("Error.")
            else:
                return None

        return None

    # convert each entry in probabilities into a probability

    # counter = [[0 for _ in range(26)] for _ in range(numWords)]

    # iterate through noQuestions and run countLetters passing in the letter from that question
    # update counter accordingly

    # ask the next question about the letter with the maximum counter value
    # check if the letter is in noQuestions to detect a lie (and update lieDetected if needed)
    # update noQuestions if no
    # update word and yesChars with the appropriate positions/chars if the answer is yes



# counts the number of times each letter appears in a valid word given the global variable word and
# the input c, which dictates that the valid words should also contain c
# c will be "" when there are no additional constraints
# countLetters returns a numWords x 27 2D array which the first 26 entries are arrays of (number of
# times that letter appears in a valid word, the number of words in which the letter appears) and of
# which the last entry is the number of valid words
def countLetters(c, numWords, lengths, word):
    ret = [[[0, 0] for _ in range(26)] for _ in range(numWords)]
    for i in range(numWords):
        ret[i].append(0)
        regex = ""
        for x in range(lengths[i]):
            if word[sum(lengths[:i])+x] == "":
                regex += "."
            else:
                regex += word[sum(lengths[:i])+x]

        for teststr in wordList:
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
def checkLetter(c, i, numWords, lengths, word):
    regex = ""
    for x in range(lengths[i]):
        if word[sum(lengths[:i])+x] == "":
            regex += "."
        else:
            regex += word[sum(lengths[:i])+x]

    prev = -1
    for teststr in wordList:
        if len(teststr) == len(regex) and re.match(regex, teststr):
            assert teststr.find(c) > -1
            if prev == -1:
                prev = teststr.find(c)
            if teststr.find(c) != prev or teststr.rfind(c) != prev:
                return False

    return True


main()

