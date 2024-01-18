# include <stdio.h>
# include <string.h>

int main(void)

{
    char *password = "__stack_check";
    char input[256];
    printf("Please enter key: ");
    scanf("%s", input);
    int ispass = strcmp(input, password);
    if (ispass == 0)
        printf("Good job.\n");
    else
        printf("Nope.\n");
    return 0;
}
