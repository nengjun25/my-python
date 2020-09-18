#include<stdio.h>
#include<stdlib.h>
#include<math.h>
void main()
{
    int p[]={
        1,8,6,2,5,4,8,3,7
    };

    //get_largest(p,9);
    double_index(p,9);
}

int get_largest(int *p,int size)
{

    int max = 0;
    for(int i = 0;i < size ; i++){
        for (int j = i+1;j< size; j++){
            int h = p[i] < p[j] ? p[i] : p[j];
            int l = h*(j-i);
            if(l > max){
                max = l;
            }

        }
    }
    
    printf("max is %d \n",max);

    return max;
}

int double_index(int *p,int size)
{
    int max = 0;
    int i = 0;
    int j = size-1;


    while(i != j){
        int h = p[i] <= p[j] ? p[i] : p[j];
        int l = h * (j-i);
        if (l > max){
            max = l;
        }
        
        if(p[i] <= p[j]){
            i++;
        }else{
            j--;
        }
    }
    printf("max is %d ",max);
    return max;
}
