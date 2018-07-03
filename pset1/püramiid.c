#include <cs50.h>
#include <stdio.h>

int main()
{
    int h,e;
    printf( "Enter a value :");
    scanf("%d", &h);
    e = h-1;

    for (int i=0; i<=h;i++){
        for (int j=0; j<=e;j++){
            printf(" ");
        }for (int k=0; k<=h-e;k++){
            printf("#");
        }
        printf(" ");
        for (int l=0; l<=h-e;l++){
            printf("#");
        }
        printf("\n");
    }
}
