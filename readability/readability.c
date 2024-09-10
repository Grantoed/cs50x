#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int calculate_coleman_liau_index(int letters, int words, int sentences);

int main(void)
{
    string text = get_string("Text: ");

    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);
    int index = calculate_coleman_liau_index(letters, words, sentences);
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    int numberOfLetters = 0;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isalpha(text[i]) != 0)
        {
            numberOfLetters++;
        }
    }
    return numberOfLetters;
}

int count_words(string text)
{
    int numberOfWords = 0;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (text[i] == ' ')
        {
            numberOfWords++;
        }
    }
    numberOfWords++;
    return numberOfWords;
}

int count_sentences(string text)
{
    int numberOfSentences = 0;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            numberOfSentences++;
        }
    }
    return numberOfSentences;
}

int calculate_coleman_liau_index(int letters, int words, int sentences)
{
    float averageNumberOfLetters = (float) letters / words * 100;
    float averageNumberOfSentences = (float) sentences / words * 100;
    float index = 0.0588 * averageNumberOfLetters - 0.296 * averageNumberOfSentences - 15.8;
    int result = round(index);
    return result;
}
