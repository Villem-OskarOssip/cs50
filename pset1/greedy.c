
#include <stdio.h>
#include <stdbool.h>
#include <cs50.h>

int main()
{
    int c, count;
    count = 0;
    bool x=true, y=true, z=true, a=true;

   printf( "Enter a value :");
   scanf("%d", &c);

   while (c != 0){
       while (x){
           if (c-25>=0){
               c -= 25;
               count++;
           }else{
               x = false;
           }
       }while (y){
           if (c-10>=0){
               c-=10;
               count++;
           }else{
               y=false;
           }
       }while (z){
           if (c-5>=0){
               c-=5;
               count++;
           }else{
               z=false;
           }
       }while (a){
           if (c-1>=0){
               c-=1;
               count++;
           }else{
               a=false;
           }
       }
   }



   printf("%d\n", count);
   printf("END");

}
