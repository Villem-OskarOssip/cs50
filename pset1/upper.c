#include <stdio.h>
#include <cs50.h>

int main(){
    string s = get_string("Before: ");
    printf("After: ");

    for (int i=0, n = strlen(s); i<n;i++){
        if (islower(n)){
            printf("%s",toupper(s));
        }
    }

}