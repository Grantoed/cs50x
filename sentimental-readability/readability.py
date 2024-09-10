from cs50 import get_string
from re import split


def main():
    text = get_string("Text: ")

    letters = countLetters(text)
    words = len(text.split(' '))
    sentences = len(split(r'(?<=[.?!])\s+', text))
    index = calculateColemanLiauIndex(letters, words, sentences)
    if (index < 1):
        print("Before Grade 1")
    elif (index >= 16):
        print("Grade 16+")
    else:
        print(f"Grade {index}")


def countLetters(text):

    numberOfLetters = 0

    for letter in text:
        if letter.isalpha():
            numberOfLetters += 1

    return numberOfLetters


def calculateColemanLiauIndex(letters, words, sentences):
    averageNumberOfLetters = letters / words * 100
    averageNumberOfSentences = sentences / words * 100
    index = 0.0588 * averageNumberOfLetters - 0.296 * averageNumberOfSentences - 15.8
    result = round(index)
    return result


main()
