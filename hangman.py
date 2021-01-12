from english_words import english_words_lower_set

wordList = english_words_lower_set
wordList.add("it's")
wordList.add("he's")
wordList.add("she's")

numQuestions = 0
numWords = 0
lengths = []
word = []
lieDetected = False

# stores each letter which has been said is not in the word/phrase but is not confirmed to be or not
# to be in the word/phrase
noQuestions = []

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
    # convert each entry into a probability

    counter = [[0 for _ in range(26)] for _ in range(numWords)]

    # iterate through noQuestions and run countLetters passing in the letter from that question
    # update counter accordingly

    # ask the next question about the letter with the maximum counter value
    # check if the letter is in noQuestions to detect a lie (and update lieDetected if needed)
    # update noQuestions if no
    # update word if the answer is yes



# counts the number of times each letter appears in a valid word given the global variable word and
# the input c, which dictates that the valid words should also contain c
# c will be "" when there are no additional constraints
# countLetters returns a numWords x 27 2D array which the first 26 entries are arrays of (number of
# times that letter appears in a valid word, the number of words in which the letter appears) and of
# which the last entry is the number of valid words
def countLetters(c):
    ret = [[[0, 0] for _ in range(26)] for _ in range(numWords)]
    for x in range(numWords):
        ret[x].append(0)

    


    return ret

# check if letter given 100% prob is in same position in each word
def checkLetter(c):
    ret = true

    return ret


