#include <stdio.h>
#include <stdbool.h>
#include <cs50.h>
#include <stdlib.h>
#include <time.h>

int main()
{
    srand(time(NULL));

    for(int i = 0; i < 10; i++ ){
        printf( "Random number #%d: %d\n", i, rand() );
    }
}

