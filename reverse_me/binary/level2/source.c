#include <stdio.h>
#include <string.h>

void no(void) {
    printf("Nope.\n");
}

void ok(void) {
    printf("Good job.\n");
}

int main(void) {
    char input[24];
    char pass[9];
    int a, b, c, var3;

    printf("Please enter key: ");
    if (scanf("%s", input) != 1)
        no();

    if (input[1] != '0' || input[0] != '0')
        no();

    memset(pass, 0, 9);
    pass[0] = 'd';

    a = 0, b = 2, c = 1;
    while (1) {
        if (c >= 8)
            break;

        char chara = input[a];
        char charb = input[a + 1];
        char charc = input[a + 2];
        var3 = ((chara - '0') * 100) + ((charb - '0') * 10) + (charc - '0');

        pass[c] = (char)var3;
        a = a + 3;
        c = c + 1;
    }

    pass[c] = '\0';
    var3 = strcmp(pass, "delabere");

    if (var3 == 0)
        ok();
    else
        no();

    return 0;
}
