from cs50 import get_string


def main():
    cardNumber = get_string("Number: ")
    numberOfDigits = len(cardNumber)
    sumOfEveryOtherDigit = sumUpEveryOtherDigit(cardNumber, numberOfDigits)
    americanExpress = isAmericanExpress(cardNumber, numberOfDigits)
    masterCard = isMasterCard(cardNumber, numberOfDigits)
    visa = isVisa(cardNumber, numberOfDigits)
    if (sumOfEveryOtherDigit % 10 != 0):
        print("INVALID\n")
    elif (americanExpress):
        print("AMEX\n")
    elif (masterCard):
        print("MASTERCARD\n")
    elif (visa):
        print("VISA\n")
    else:
        print("INVALID\n")


def isAmericanExpress(cardNumber, numberOfDigits):
    firstTwoDigits = int(cardNumber[0] + cardNumber[1])

    if ((numberOfDigits == 15) and (firstTwoDigits == 34 or firstTwoDigits == 37)):
        return True
    else:
        return False


def isMasterCard(cardNumber, numberOfDigits):
    firstTwoDigits = int(cardNumber[0] + cardNumber[1])

    if ((numberOfDigits == 16) and (firstTwoDigits >= 51 and firstTwoDigits <= 55)):
        return True
    else:
        return False


def isVisa(cardNumber, numberOfDigits):
    firstDigit = int(cardNumber[0])

    if numberOfDigits == 13:
        if firstDigit == 4:
            return True
    elif numberOfDigits == 16:
        if firstDigit == 4:
            return True
    else:
        return False


def sumUpEveryOtherDigit(cardNumber, numberOfDigits):
    sum = 0
    isEveryOtherDigit = False

    for i in range(numberOfDigits - 1, -1, -1):
        digit = int(cardNumber[i])
        if isEveryOtherDigit:
            digit = digit * 2
            if digit > 9:
                digit = digit - 9
        sum += digit
        isEveryOtherDigit = not isEveryOtherDigit

    return sum


main()
