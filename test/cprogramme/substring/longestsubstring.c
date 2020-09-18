#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main()
{
    char str[] = "abcabcbb";
    char str2[] = "bbbbb";
    char str3[] = "pwwkew";
    
    get_max_sub(str);
    get_max_sub(str2);
    get_max_sub(str3);

    flexible_window(str);
    flexible_window(str2);
    flexible_window(str3);
    
}

int get_max_sub(char str[])
{
    int size = strlen(str);
    int maxlen = 0;
      for (int i = 0;i< size;i++){
          for(int j = i+1; j < size ; j++){
              int flag = 0;
              for (int k = i ; k< j; k++){
                  if (str[k] == str[j]){
                      flag = 1;
                      int len = j-i;
                      printf("start  at %d end at %d \n",i,j);
                      if (len > maxlen){
                          maxlen = len;
                      }
                      break;
                  }
              }
  
              if (flag == 1){
                  break;
              }
          }
          if (maxlen >= size -i){
              break;
          }
      }
      printf("max length is %d \n",maxlen);
      return maxlen;
}

int flexible_window(char* str)
{
    int size = strlen(str);
    char appear[128];
    memset(appear,0,128);
    int maxlen = 0;
    int i = 0;
    int j = 0;

    while(i <= size -1 && j <= size -1){
        int len = strlen(appear);
        int duplicate = 0;
        int flag = 0;
        
        for(int k = 0;k<len;k++){
            if(str[j] == appear[k]){
                printf(" duplicate %d \n",str[j]);
                duplicate = k;
                i = i+k+1;
                flag = 1;
                break;
            }
        }

        if(flag == 1){
            printf("delete appear dup is %d len is %d \n",duplicate,len);
            for (int m = 0;m < len ; m++){
                if (duplicate+m+1 < len){
                    appear[m] = appear[duplicate+m+1];
                }else{
                    appear[m] = 0;
                }
            }

            int alen = strlen(appear);
            for (int n = 0 ; n < alen ; n++){
                printf(" is %d \n",appear[n]);
            }
        }else{
            printf("not need to delete \n");
            appear[len] = str[j];
            j++;
            if (maxlen < len+1){
                maxlen = len+1;
            }
        }
    }
    printf("max length is %d \n",maxlen);
    return maxlen;
}


void array_delete(char *c,int index)
{
    int len = strlen(c);
    for (int i = 0;i < len ; i++){
        if (index+i+1 < len){
            c[i] = c[index+i+1];
        }else{
            c[i] = 0;
        }
    }

    int alen = strlen(c);
    for (int j = 0 ; j < alen ; j++){
        printf(" is %d \n",c[j]);
    }

}
