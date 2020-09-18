#include<stdio.h>
#include<stdlib.h>
#include<string.h>

void main()
{
    char *s = "leetcodeishiring";

    sort(s,3);

}


void sort(char *s, int h)
{
    int len = strlen(s);

    int group = 2*h -2;
    
    int left = len % group;

    int groupCount = len / group;
    
    int width = 0 ;
    printf("group count %d \n",groupCount);
    if (left == 0){
        width = (h-1)*groupCount;
    }else if (left <= h){
        width = (h-1)*groupCount+1; 
    }else {
        width = (h-1)*groupCount+left-h+1;
    }

    char m[width][h];
    
    printf("wid is %d \n",width);

    printf("m size %d \n",sizeof(m));
    
    memset(m,0,sizeof(m));

    int j = 0;
    int i = 0;
    int k = 0;
    while(i < len && j < width){
       // printf("i is %d , j is %d \n",i,j);
        int mod = j % (h-1);
        if(mod  == 0 ){
            for (int k =0 ;k < h ; k++){
                m[j][k] = s[i];
                i++;
                if(k == h -1){
                    j++;
                }
            }
        }else {
            m[j][h-mod-1] = s[i];
            j++;
            i++;
        }
    }
  

    for (int x = 0 ; x < width ; x++){
        for(int y = 0;y< h ; y ++){
            if(y == h-1){
                printf("%c \n",m[x][y]);
            }else {
                printf("%c",m[x][y]);
            }
        }     
    }

    for (int l = 0;l<h ; l++){
        for(int n = 0;n < width ; n++){
            char p = m[n][l];
            if (p != 0){
                printf("%c",p);
            }
        }
    }

}



void output(char s[2][3])
{
    for(int i = 0 ; i < 3 ; i++){
        for(int j = 0 ; j< 2 ; j ++){
            printf("%c",s[j][i]);
        }

    }


}

