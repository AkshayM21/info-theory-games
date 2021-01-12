from english_words import english_words_lower_set
import re

wordList = english_words_lower_set
wordList.add("it's")
wordList.add("he's")
wordList.add("she's")

alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
         's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

numQuestions = 0
numWords = 0
lengths = []
word = []
lieDetected = False

yesChars = [] # stores each letter which has been confirmed to be in the word/phrase
# stores each letter which has been said is not in the word/phrase but is not confirmed to be or not
# to be in the word/phrase
noQuestions = []
noChars = [] # stores each letter which has been confirmed to not be in the word/phrase

def main():
    print("Hello! Welcome to Hangman, a game in which we attempt to not hang an entire person while hanging part of a person is ok.")
    print("Please enter the number of words in your selected word/phrase followed by the number of letters in each word, all separated by a space")
    print("(e.g. 3 3 7 5 could signify the phrase \"low hanging fruit\"): ")

    temp = map(int, input().split(" "))
    numWords = temp[0]
    lengths = temp[1:]

    for i in range(numWords):
        for j in range(lengths[i]):
            word.append("")
        word.append(" ")

    done = False

    while not done:
        askNextQuestion()
        done = word.count("")==0

    ans = ""
    for i in range(len(word)):
        ans += word[i]

    print("Your word is " + ans + "! We guessed your word in " + str(numQuestions) + " questions.")


def askNextQuestion():
    probabilities = countLetters("")

    # check if there's only one word possible then guess that if so

    # convert each entry in probabilities into a probability

    counter = [[0 for _ in range(26)] for _ in range(numWords)]

    # iterate through noQuestions and run countLetters passing in the letter from that question
    # update counter accordingly

    # ask the next question about the letter with the maximum counter value
    # check if the letter is in noQuestions to detect a lie (and update lieDetected if needed)
    # update noQuestions if no
    # update word with the appropriate positions if the answer is yes



# counts the number of times each letter appears in a valid word given the global variable word and
# the input c, which dictates that the valid words should also contain c
# c will be "" when there are no additional constraints
# countLetters returns a numWords x 27 2D array which the first 26 entries are arrays of (number of
# times that letter appears in a valid word, the number of words in which the letter appears) and of
# which the last entry is the number of valid words
def countLetters(c):
    ret = [[[0, 0] for _ in range(26)] for _ in range(numWords)]
    for i in range(numWords):
        ret[i].append(0)
        regex = ""
        for x in range(lengths[i]):
            if word[sum(lengths[:i])+x] == "":
                regex += "."
            else:
                regex += word[sum(lengths[:i])+x]

        for str in wordList:
            if re.fullmatch(regex, str) and c in str:
                ret[-1] += 1
                for j in range(26):
                    if alpha[j] in str:
                        ret[i][ord(alpha[j])-ord(alpha[0])][0] += str.count(alpha[j])
                        ret[i][ord(alpha[j])-ord(alpha[0])][1] += 1

    return ret

# check if letter given 100% prob is in same position in each possible valid word
# c is the input letter
# i is the index of the word within which c has a 100% chance of being, corresponding to the
# appropriate index within the lengths array
# returns true if the letter is in the same unique position in each valid word, false otherwise
def checkLetter(c, i):
    regex = ""
    for x in range(lengths[i]):
        if word[sum(lengths[:i])+x] == "":
            regex += "."
        else:
            regex += word[sum(lengths[:i])+x]

    prev = -1
    for str in wordList:
        if re.fullmatch(regex, str):
            assert str.find(c) > -1
            if prev == -1:
                prev = str.find(c)
            if str.find(c) != prev or str.rfind(c) != prev:
                return False

    return True


