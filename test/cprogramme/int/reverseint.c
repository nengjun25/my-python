#include<stdio.h>
#include<stdlib.h>
#include<string.h>

const int MAX_INT = (1L << 31) - 1;

const int MIN_INT = -1 << 31;

int main(){
    int a = 1233210;
    
    reverse(a);
    back_int(a);    
}

void reverse(int i)
{
    int j = 0;
    while(i > 0){
        int m = i % 10;
        j = j*10 + m;
        i = i / 10;
    }
    printf("j is %d \n",j);

}


void back_int(int i)
{

    if (i < 0 || i % 10 == 0){
        printf("false \n");
        return;
    }

    int j = 0; 
    while(i > 0){
        int m = i % 10;
        i = i /10;
        j = j*10+m;
        
        if (i == j || i/10 == j){
            printf("true \n");
            return;
        }
    }
    
    printf("false \n");
}
