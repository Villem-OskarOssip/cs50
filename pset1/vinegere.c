#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int lLetter(string s, int lk, int i){
    printf("%c", 'a' + (s[i] - 'a' + lk) % 26);
    return 1;
}

int uLetter(string s, int lk, int i){
    printf("%c", 'A' + (s[i] - 'A' + lk) % 26);
    return 1;
}

int main(int argc, string argv[])
{

    if (argc != 2) {
        printf("Usage: ./vinegere k\n");
        return 1;
    }
    string key;
    int l;

    key = argv[1];
    l = strlen(key);

    if (!isalpha(key)){
        return 1;
    }


    string s;
    s = get_string("plaintext: ");
    printf("ciphertext: ");

    for (int i = 0, j = 0, n = strlen(s); i < n; i++){

        int lk = tolower(key[j % l]) - 'a';

        if (isupper(s[i])){
            uLetter(s, lk, i);
            j++;
        }

        else if (islower(s[i])){
            lLetter(s, lk, i);
            j++;
        }

        else{
            printf("%c", s[i]);
        }
    }

}
