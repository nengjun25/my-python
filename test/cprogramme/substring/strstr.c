#include<stdio.h>
#include<stdlib.h>
#include<string.h>

void main(){
    char *s = "rergewrwrbtq";
    char *p = "wr";

    strstr1(s,p);
}

int strstr1(char *s,char *p){
    int ls = strlen(s);
    int lp = strlen(p);
    int index = 0;

    for (int i =0 ;i<ls;i++){
        if(s[i] == p[0]){
            index = i;
            for(int k = 1;k<lp;k++){
                if(s[i+k] != p[k]){
                    index = 0;
                    break;
                }
            }
            if(index != 0){
                break;
            }
        }
    }

    printf("index is %d \n",index);
    return index;

}
