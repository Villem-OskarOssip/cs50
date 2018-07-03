#include <stdio.h>
#include <stdbool.h>
#include <cs50.h>

int main()
{
int n;
    do{
        n = get_int("Enter value: ");
    }while(n<0);
}