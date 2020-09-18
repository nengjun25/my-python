#include<stdio.h>
#include<stdlib.h>

void main()
{
    int a[] = {
        5,4,3,9,8,6,7,2,1,23,0,16,13,18
    };
    int len = sizeof(a)/sizeof(int);
    //for(int k = len/2-1;k >=0;k--){
        heap_sort(a,len);
    //}
    for(int i =0;i<len;i++)
        printf("%d \n",a[i]);
}

void heapify(int a[],int len,int p){
    int left = p*2+1;
    int right = p*2+2;
    if(left <= len-1){
        int min_index = 0;
        if(right > len-1){
            min_index = left;
        }else{
            min_index = (a[left]>= a[right])?right:left;
        }
            
        if(a[p]>a[min_index]){
            int tmp = a[p];
            a[p] = a[min_index];
            a[min_index] = tmp;
            heapify(a,len,min_index);
        }
    }
}

void heapify_iter(int a[],int len,int p)
{
    while (p < len){
        int left = p*2+1;
        if(left > len-1){
            break;
        }
        int right = p*2+2;
        int min_index = 0;
        if(right > len-1){
            min_index = left;
        }else{
            min_index = (a[left]>= a[right])?right:left;
        }   
                
        if(a[p]>a[min_index]){
            int tmp = a[p];
            a[p] = a[min_index];
            a[min_index] = tmp;
            p = min_index;
        }else{
            break;
        }
    }

}

void heap_sort(int a[],int len){
    for(int k = len/2-1;k >=0;k--){
        heapify_iter(a,len,k);
    }
    
    int i = len -1;
    while(i>0){
        int t = a[i];
        a[i] = a[0];
        a[0] = t;
        
        for(int j = i/2-1;j>=0;j--){
            heapify_iter(a,i,j);
        }

        i--;
    }
}
