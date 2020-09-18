#include<stdio.h>
#include<stdlib.h>
#include<string.h>

char *my_pre(char*[],int);

void main(){
    char *s[] = {
        "abc",
        "ab",
        "abcererer"
    };
    int len = sizeof(s)/sizeof(char*);
    printf("len is %d \n",len);

    char *p = "1234";
    printf(" *p is %s \n",p);
    char *m;
    m = p;

    p = "12345";
   
    printf("p is %p",p);

    printf("size of p is %ld \n",sizeof(p));

    printf("*p is %s *m is %s",p,m);

    printf("*p2 is %c *m2 is %c",*p,*m);
    
    printf("pre is %s \n",my_pre(s,len));
                
}

char *my_pre(char *s[],int len){

    if (len == 0){
        return "";
    }

    if (len == 1){
        return s[0];
    }

    
    char *p;
    p = (char*)malloc(strlen(""));
    strcpy(p,"");

    int l = strlen(s[0]);

    for (int i = 0;i<l;i++){
        for(int j = 1;j< len;j++){
            
            int ll = strlen(s[j]);
            
            if (i == ll){
                return p;
            }
        
            if(s[0][i] != s[j][i]){
                return p;
            }

            if(j = len -1){
                char *m;
                m = p;
                p =(char *)malloc(strlen(p)+1);

                sprintf(p,"%s%c",m,s[0][i]);

                printf("strcat p is %s \n",p);
            }
        }
    }

    return p;
}


