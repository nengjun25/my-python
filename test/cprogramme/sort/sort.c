#include<stdio.h>
#include<stdlib.h>

extern int fast_sort(int a[*],int,int);
extern void quick_sort(int a[*],int,int);

void main()
{
    int a[]={
       5,2,8,5,1,4,3,8,6,9,5,0
    };
    //int a[]={
    //    0,1,2,3,4,5,6,7,8,9
    //};
    int len = sizeof(a)/sizeof(int);
    //quick_sort(a,0,len-1);
    //int *b;
    //b = (int *)malloc(sizeof(int)*len);
    //merge_sort_iterate(a,b,len);
    //merge_sort1(a,b,0,len-1);
    count_sort(a,len);
    for(int i = 0;i<len;i++){
        printf("%d",a[i]);
    }
}

void quick_sort(int a[],int low,int high){
    if(low >= high){
        return;
    }
    int index = fast_sort(a,low,high);
    quick_sort(a,low,index-1);
    quick_sort(a,index+1,high);
}

int fast_sort(int a[],int low,int high){
    int start = low;
    int p = a[start];
    while(low < high){
        while(low <high && a[high] >= p){
            high--;
        }

        while(low < high && a[low] < p){
            low++;
        }

        if(high != low){
            int t = a[low];
            a[low] = a[high];
            a[high] = t;
        }
    }
    if(a[low] < a[start]){
        a[start]=a[low];
        a[low] = p;
    }
    
    for(int i =0;i<11;i++){
        printf("%d",a[i]);
    }
    
    printf("\n");

    return low;

}

void bubble_sort(int a[],int len){
    for(int i = 0;i<len;i++){
        for(int j = 0;j<len-1-i;j++){
            if(a[j] > a[j+1]){
                int t = a[j];
                a[j] = a[j+1];
                a[j+1] = t;
            }

        }
    }
}

void choose_sort(int a[],int len){
    for(int i = 0;i < len -1; i++){
        for(int j = i+1;j<len;j++){
            if(a[i] > a[j]){
                int t = a[i];
                a[i] = a[j];
                a[j] = t;
            }
        }
    }
}

void insert_sort(int a[],int len){
    for(int i = 0;i<len;i++){
        int tmp = a[i];
        for(int j =i-1 ;j >= 0 ;j--){
            if(a[j] > tmp){
                a[j+1] = a[j];
                if(j == 0){
                    a[j] = tmp;
                }
            }else{
                a[j+1] = tmp;
                break;
            }
        }
    }
}

void shell_sort(int a[],int len){
    int h = len/2;
    while(h >= 1){
        for (int i = 0; i<len; i++){
            int tmp = a[i];
            for(int j = i-h ;j>=0;j= j-h){
                if(a[j] > tmp){
                    a[j+h] = a[j];
                    if(j-h <0){
                        a[j] = tmp;
                    }
                }else{
                    a[j+h] = tmp;
                    break;
                }
            }
        }
        for(int i = 0;i<len ;i++){
            printf("%d",a[i]);
        }
        printf("\n");
        h = h/2;
    }
}

void merge_sort(int a[],int len){
 
    if(len == 1){
        return;
    }

    int mid = (len-1)/2;
    int left[mid+1];
    int right[len-1-mid];
    memset(left,0,mid+1);
    memset(right,0,len-1-mid);

    for(int i = 0;i<mid+1;i++){
        left[i] = a[i];
        printf("%d",left[i]);
    }
    printf("\n");
    for(int j = 0; j<len-1-mid;j++){
        right[j]= a[mid+1+j];
        printf("%d",right[j]);
    }
    printf("\n");

    merge_sort(left,mid+1);
    merge_sort(right,len-mid-1);
    
    merge(left,right,a,mid+1,len-1-mid,len);
    
    
}

void merge(int a[],int b[],int res[],int la,int lb,int lr)
{
    int i = 0;
    int j = 0;
    int k = 0;
    while(i < la || j < lb){
        if(i >= la){
            res[k] = b[j];
            k++;
            j++;
            continue;
        }

        if(j >= lb){
            res[k]=a[i];
            k++;
            i++;
            continue;
        }

        if(a[i] <= b[j]){
            res[k] = a[i];
            i++;
        }else{
            res[k] = b[j];
            j++;
        }
        k++;
    }

}

void merge_sort1(int a[],int h[],int left,int right){
    if(left == right){
        return;
    }
    
    int mid = left+(right - left)/2;

    merge_sort1(a,h,left,mid);
    merge_sort1(a,h,mid+1,right);
    
    int i = left;
    int j = mid+1;
    int k = left;

    while(i<=mid || j<=right){
        if(i>mid){
            h[k++] = a[j++];
            continue;
        }

        if(j > right){
            h[k++] = a[i++];
            continue;
        }

        if(a[i] <= a[j]){
            h[k++] = a[i++];
        }else{
            h[k++] = a[j++];
        }
    }
    
    for(k = left;k<=right;k++){
        a[k] = h[k];
    }
}

void merge_sort_iterate(int a[],int h[],int len){
    int l = 1;
    while(l<=len){
        int left = 0;
        while(left < len){
            int mid = (left+l-1 <= len-1)?left+l-1:len-1;
            int right = (left+l+l-1 <= len-1)?left+l+l-1:len-1;
            printf("left is %d r is %d \n",left,right);
            int i = left;
            int j = mid+1;
            int k = left;

            while(i<= mid && j<= right){
                if(a[i] <= a[j]){
                    h[k++] = a[i++];
                }else{
                    h[k++] = a[j++];
                }
            }

            while(i<=mid){
                h[k++] = a[i++];
            }

            while(j<= right){
                h[k++] = a[j++];
            }

            for(k = left;k<=right;k++){
                a[k] = h[k];
            }
            left = left +l+l;
            
       }
       for(int i =0;i<len;i++){
           printf("%d",a[i]);
       }
       printf("\n");
       l=l*2;
    }
}

void count_sort(int a[],int len){
    int max = a[0];
    int min = a[0];
    for(int i =0;i<len;i++){
        if(a[i] > max){
            max = a[i];
        }
        if(a[i]<min){
            min = a[i];
        }
    }

    int *count;
    
    count = (int *)malloc((max-min+1)*sizeof(int));


    for(int j = 0;j<len;j++){
        count[a[j-min]]++;
    }
    
    int k =0;
    for(int m = 0;m<max-min+1;m++){
        while(count[m]>0){
            a[k++] = m+min;
            count[m]--;
        }
    }

}
