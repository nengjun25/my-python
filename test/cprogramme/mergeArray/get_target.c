#include<stdio.h>
#include<stdlib.h>
void main(){
    int a[]={
        1,3,5,6
    };

    int target = 7;
    int len = sizeof(a)/sizeof(int);
    printf("%d \n",l);
    //leftside_dichotomy(a,len,target);
    //rightside_dichotomy(a,len,target);    
    printf("%d \n",get_position(a,len,target));    
}

void foreach(int a[],int len,int target){
    int i=0;
    int j=len-1;
    int start = -1;
    int end = -1;
    while (i < j){
        if(a[i] == target && a[j] == target){
            start = i;
            end = j;
            break;
        }
        if(a[i] == target){
            if(start != -1){
                start = i;
            }
            j--;
            continue;
        }
        if(a[j] == target){
            if(end != -1){
                end = j;
            }
            i++;
            continue;
        }
        i++;
        j--;

    }
    printf("start is %d , end is %d \n",start,end);
}


int dichotomy(int a[],int len,int target)
{
    int left = 0;
    int right = len-1;

    while(left <= right){
        int mid = left + (right-left)/2;

        if(a[mid] == target){
            return mid;
        }else if(a[mid] > target){
            right = mid-1;
        }else if(a[mid] < target){
            left = mid +1;
        }
   }

}

int leftside_dichotomy(int a[],int len,int target){
    int left = 0;
    int right = len - 1;
    while(left < right){
        int mid = left + (right - left)/2;
        if(a[mid] == target){
            right = mid;
        }else if(a[mid] < target){
            left = mid+1;
        }else if(a[mid] > target){
            right = mid-1;
        }
    }
    printf("left side is %d \n",right);
    return right;
}

int rightside_dichotomy(int a[],int len,int target){
    int left = 0;
    int right = len -1;

    while (left < right){
        int mid = right - (right - left)/2;

        if(a[mid] == target){
            left = mid;
        }else if(a[mid] < target){
            left = mid+1;
        }else if(a[mid] > target){
            right = mid -1;
        }
    }
    printf("right side is %d \n",right);
    return left;
}


int get_position(int a[],int len,int target){
    int left = 0;
    int right = len - 1;

    while(left <= right){
        int mid = left+(right - left)/2;

        if(a[mid] == target){
            return mid;
        }else if(a[mid] > target){
            right = mid-1;
        }else if (a[mid] < target){
            left = mid+1;
        }

    }
    return left;

}

