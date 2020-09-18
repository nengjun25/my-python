#include<stdio.h>
#include<stdlib.h>

void main(){
    int a[]={
        5,4,3,2,1
    };

    int len = sizeof(a)/sizeof(int);
    int i;
    for(i = len -1 ;i > 0;i--){
        if(a[i] > a[i-1]){
            int pj = a[i];
            int index = i;
            for(int j = i+1;j<len;j++){
                if(a[j] > a[i-1] && a[j] < pj){
                    pj = a[j];
                    index = j;
                }
            }
            
            int t = a[i-1];
            a[i-1] = pj;
            a[index] = t;

            for(int k = 0;k<(len-i)/2;k++){
                int t1 = a[i+k];
                a[i+k] = a[len-1-k];
                a[len-1-k] = t1;
            }
            break;
        }

    }

    printf("i is %d \n",i);
            
    if(i==0){
        for (int j = 0; j<len/2;j++){
            int t2 = a[j];
            a[j] = a[len-1-j];
            a[len-1-j] = t2;
        }
    }
    
    for(int j = 0 ; j < len ;j++){
        printf("%d \n",a[j]);
    }
    
}


