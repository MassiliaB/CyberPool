#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

void no(void) {
    printf("Nope.\n");
}

void ok(void) {
    printf("Good job.\n");
}

int main(void)
{
    // Variables
    long userInput;
    int scanResult;
    size_t processedKeyLength;
    bool isProcessedKeyShorterThan8;
    char currentDigit;
    char nextDigit;
    char digitAfterNext;
    int zeroValue;
    char inputKey[31];
    char processedKey[9];
    long currentIndex;
    int comparisonResult;

    // Initialization
    zeroValue = 0;
    printf("Please enter key: ");
    scanResult = scanf("%s", inputKey);
    printf("hello\n");

    // Input validation
    if (scanResult != 1)
        no();
    if (inputKey[0] != '4')
        no();
    if (inputKey[1] != '2')
        no();
    printf("hello2\n");

    fflush(stdin);
    memset(processedKey, 0, 9);
    processedKey[0] = '*';
    zeroValue = 0;
    currentIndex = 2;

    // Processing input key
    while (true)
    {
        processedKeyLength = strlen(processedKey);
        userInput = currentIndex;
        isProcessedKeyShorterThan8 = false;

        if (processedKeyLength < 8)
        {
            processedKeyLength = strlen(inputKey);
            isProcessedKeyShorterThan8 = userInput < processedKeyLength;
        }

        if (!isProcessedKeyShorterThan8)
            break;

        // Extracting digits from input key
        currentDigit = inputKey[currentIndex];
        nextDigit = inputKey[currentIndex + 1];
        digitAfterNext = inputKey[currentIndex + 2];

        // Check for backslash and adjust processing
        if (currentDigit == '\\' && nextDigit == '4' && digitAfterNext == '2') {
            currentIndex += 2;  // Skip the backslash and '4'
            currentDigit = '4'; // Set currentDigit to '4'
        }

        scanResult = currentDigit - '0';
        processedKey[processedKeyLength] = (char)scanResult;
        processedKeyLength = processedKeyLength + 1;
        currentIndex = currentIndex + 3;
    }
    processedKey[processedKeyLength] = '\0';
    printf("key = %s\n", processedKey);
    comparisonResult = strcmp(processedKey, "********");

    // Output based on comparison result
    if (comparisonResult == -2)
        no();
    else if (comparisonResult == -1)
        no();
    else if (comparisonResult == 0)
        ok();
    else if (comparisonResult == 1)
        no();
    else if (comparisonResult == 2)
        no();
    else if (comparisonResult == 3)
        no();
    else if (comparisonResult == 4)
        no();
    else if (comparisonResult == 5)
        no();
    else if (comparisonResult == 0x73)
        no();
    else
        no();

    return 0;
}
