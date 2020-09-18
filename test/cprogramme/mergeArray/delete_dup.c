#include<stdio.h>
#include<stdlib.h>

void main(){
    int a[]={
        0,0,1,1,2,2,3,3,3,3,3,6,7,8,9,9,9
    };
    
    int len = sizeof(a)/sizeof(int);
    
    delete_var(a,len,3);
}

void delete_dup(int a[],int len)
{
    int i = 0;
    int j = i+1;
    int k = 0;
        
    while(j<len){
        if(a[i] != a[j]){
            k++;
            a[k] = a[j];
            i = j;
        }   
        j++;
    }   

    for(int m=0;m<=k;m++){
        printf("%d \n",a[m]);
    } 
}

int delete_var(int a[],int len,int var){
    int k = 0;
    int i = 0;
    while(i<len){
        if(a[i] != var){
            a[k] = a[i];
            k++;
        }
        i++;
    }

    for(int l = 0 ;l<k;l++){
        printf("%d \n",a[l]);
    }
    printf("len is %d \n",k);
    return k; 

}
