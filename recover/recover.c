#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

const int BLOCK_SIZE = 512;

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open the input file
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    BYTE buffer[BLOCK_SIZE];
    int fileCounter = 0;
    FILE *outputFile = NULL;
    char filename[8];

    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (outputFile != NULL)
            {
                fclose(outputFile);
            }

            sprintf(filename, "%03i.jpg", fileCounter);

            outputFile = fopen(filename, "w");
            if (outputFile == NULL)
            {
                printf("Could not create output JPEG file.\n");
                fclose(card);
                return 1;
            }

            fileCounter++;
        }

        if (outputFile != NULL)
        {
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, outputFile);
        }
    }

    if (outputFile != NULL)
    {
        fclose(outputFile);
    }

    fclose(card);

    return 0;
}
