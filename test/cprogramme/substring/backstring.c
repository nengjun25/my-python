#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char * from_middle(char *s);

void main()
{
    char str[] = "babad";
    char str1[] = "cbbd";

    force(str);
    force(str1);

    char *back1 = from_middle(str);
    char *back2 = from_middle(str1);
    free(back1);
    free(back2);

}


char * from_middle(char *s)
{
    int len =strlen(s);
    int maxlen = 0;
    int mid = 0;
    int start = 0;
    int end = 0;


    for( int mid = 1 ; mid < len-1 ; mid++ ){
        int ln = 0;
        int rn = 0;

        int left = mid -1;
        int right = mid +1;

        int backlen = 0;
        int backstart = 0;
        int backend = 0;
        if((s[mid] != s[left] && s[mid] != s[right]) || (s[mid] == s[left] && s[mid] == s[right])){
            printf("ln rn = mid \n");
            ln = mid;
            rn = mid;
            backlen = 1;
        }else{
            backlen = 2;
            if(s[left] == s[mid]){
                ln = left;
                rn = mid;
            }else{
                ln = mid;
                rn = right;
            }
        }
        backstart = ln;
        backend = rn;
        for (int j = 1 ; j<= ln ; j++){
            if(s[ln -j] == s [rn + j]){
                backlen = backlen +2;
                backstart--;
                backend++;
            }else{
                printf("not equal break start is %d end is %d backlen is %d \n",backstart,backend,backlen);
                break;
            }
            if (rn+j ==len -1){
                break;
            }
        }

        if (backlen > maxlen){
            maxlen = backlen;
            start = backstart;
            end = backend;
        }

    }

    char *p;
    p = (char *)malloc(sizeof(maxlen));
    for (int i = 0 ; i < maxlen ; i++){
        p[i] = s[start+i];
    }
    
    printf("max back is %s \n",p);
    printf("start is %d end is %d \n",start,end); 
    return p;
    // while(mid ){

    //     int left = mid-1;
    //     int right = mid+1;

    //     if((s[mid] != s[left] && s[mid] != s[right]) || (s[mid] == s[left] && s[mid] == s[right])){
    //         int backlen = 1;
    //         for (int j = 1 ; j <= mid ; j++){
    //             if(s[mid - j] == s[mid +j]){
    //                 backlen = backlen + 2;
    //             }else{
    //                 if(backlen > maxlen){
    //                     maxlen = backlen;
    //                 }
    //                 mid--;
    //                 break;
    //             }
    //         }
    //     }else {
    //         int ln = 0;
    //         int rn = 0;
    //         if(s[left] == s[mid]){
    //             ln = left;
    //             rn = mid;
    //         }else{
    //             ln = mid;
    //             rn = right;
    //         }
    //         int backlen = 2;
    //         for (int j = 1 ; j <= ln ; j++){
    //             if(s[ln - j] == s[rn +j]){
    //                 backlen = backlen + 2;
    //             }else{
    //                 if(backlen > maxlen){
    //                     maxlen = backlen;
    //                 }
    //                 mid--;
    //                 break;
    //             }
    //         }

    //     }
    // }


}

int force(char *s)
{
    int len = strlen(s);
    int maxlen = 0;
    for (int i = 0 ; i<len ; i++){
        for (int j = i+1; j < len ; j++){
           for(int k = i ; k <= j ; k++){
                if (s[k] != s[j-k+i]){
                    break;
                }
                if (k == j){
                    len = j - i +1;
                    if (len > maxlen){
                        maxlen = len;
                    }
                }
           }
        }
    }

    printf("max back is %d \n",maxlen);
}


int is_back_string(char *s){

    int len = strlen(s);
    for (int i = 0 ; i < len ; i ++){
        if(s[i] != s[len - 1 - i]){
            return 1;
        }
    }

    return 0;

}
