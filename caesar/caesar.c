#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int encrypt_text(string text, int key);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    string argument = argv[1];

    if (argc == 1 || argc > 2)
    {
        printf("Program should have one argument! \n");
        return 1;
    }

    for (int i = 0, length = strlen(argument); i < length; i++)
    {
        if (isdigit(argument[i]) == 0)
        {
            printf("Usage: ./caesar key \n");
            return 1;
        }
    }

    int key = atoi(argument);

    string plainText = get_string("plaintext: ");

    encrypt_text(plainText, key);
}

int encrypt_text(string text, int key)
{
    printf("ciphertext: ");
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        char rotatedChar = rotate(text[i], key);
        printf("%c", rotatedChar);
    }
    printf("\n");
    return 0;
}

char rotate(char c, int n)
{
    if (isalpha(c))
    {
        char offset = isupper(c) ? 'A' : 'a';
        return (c - offset + n) % 26 + offset;
    }
    else
    {
        return c;
    }
}
