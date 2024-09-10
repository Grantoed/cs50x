#include "cs50.h"
#include "stdio.h"

int main(void)
{
    const int MIN_HEIGHT = 1;
    const int MAX_HEIGHT = 8;

    int height = get_int("How tall should the pyramid be? ");

    while (height < MIN_HEIGHT || height > MAX_HEIGHT)
    {
        height = get_int("How tall should the pyramid be? ");
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height - i - 1; j++)
        {
            printf(" ");
        }

        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        printf("  ");

        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        printf("\n");
    }
}
