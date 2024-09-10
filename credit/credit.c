#include "cs50.h"
#include "math.h"
#include "stdio.h"

int countDigits(long cardNumber);
int sumUpEveryOtherDigit(long cardNumber);
int sumOfDigits(int number);
bool isAmericanExpress(long cardNumber, int numberOfDigits);
bool isMasterCard(long cardNumber, int numberOfDigits);
bool isVisa(long cardNumber, int numberOfDigits);

int main(void)
{
    long cardNumber = get_long("Number: ");
    int sumOfEveryOtherDigit = sumUpEveryOtherDigit(cardNumber);
    int numberOfDigits = countDigits(cardNumber);
    bool americanExpress = isAmericanExpress(cardNumber, numberOfDigits);
    bool masterCard = isMasterCard(cardNumber, numberOfDigits);
    bool visa = isVisa(cardNumber, numberOfDigits);
    if (sumOfEveryOtherDigit % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }
    else if (americanExpress)
    {
        printf("AMEX\n");
    }
    else if (masterCard)
    {
        printf("MASTERCARD\n");
    }
    else if (visa)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
        return 0;
    }
}

bool isAmericanExpress(long cardNumber, int numberOfDigits)
{
    int firstTwoDigits = cardNumber / pow(10, numberOfDigits - 2);
    if ((numberOfDigits == 15) && (firstTwoDigits == 34 || firstTwoDigits == 37))
    {
        return true;
    }
    else
    {
        return false;
    }
}

bool isVisa(long cardNumber, int numberOfDigits)
{
    if (numberOfDigits == 13)
    {
        int firstDigit = cardNumber / pow(10, 12);
        if (firstDigit == 4)
        {
            return true;
        }
    }
    else if (numberOfDigits == 16)
    {
        int firstDigit = cardNumber / pow(10, 15);
        if (firstDigit == 4)
        {
            return true;
        }
    }
    return false;
}

bool isMasterCard(long cardNumber, int numberOfDigits)
{
    int firstTwoDigits = cardNumber / pow(10, numberOfDigits - 2);
    if ((numberOfDigits == 16) && (firstTwoDigits >= 51 && firstTwoDigits <= 55))
    {
        return true;
    }
    else
    {
        return false;
    }
}

int countDigits(long cardNumber)
{
    int count = 0;

    while (cardNumber > 0)
    {
        count++;
        cardNumber = cardNumber / 10;
    }

    return count;
}

int sumUpEveryOtherDigit(long cardNumber)
{
    int sum = 0;
    bool isEveryOtherDigit = false;

    while (cardNumber > 0)
    {
        int lastDigit = cardNumber % 10;
        if (isEveryOtherDigit)
        {
            sum += sumOfDigits(lastDigit * 2);
        }
        else
        {
            sum += lastDigit;
        }
        cardNumber = cardNumber / 10;
        isEveryOtherDigit = !isEveryOtherDigit;
    }

    return sum;
}

int sumOfDigits(int number)
{
    int sum = 0;
    while (number > 0)
    {
        sum += number % 10;
        number = number / 10;
    }
    return sum;
}
