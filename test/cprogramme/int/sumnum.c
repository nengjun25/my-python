#include<stdio.h>
#include<stdlib.h>
#include<string.h>

void triple_for();
void double_p();
void nearlest();

void main()
{
    //triple_for();
    //double_p();
    char *p,j;
    p = "13";
    char *q = "1234"; 
    printf("q size is %d ,p size %d , j size %ld \n",sizeof(q),sizeof(p),sizeof(j));

    nearlest(-1);
}

void double_p(){
    int a[] = {-1,-1,-1,0,1,2};
 
    int len = sizeof(a) / sizeof(int);
 
    int m = 0;
    
    for(int i = 0;i<len ;i++){
        if (i != 0 && a[i] == a[i-1]){
            continue;
        }
        int j = i+1;
        int k = len-1;
        int l = -3-a[i];
        while(j < k){
            if(j != i+1 && a[j] == a[j-1]){
                j++;
                continue;
            }

            if(k != len -1 && a[k] == a[k+1]){
                k--;
                continue;
            }

            if(a[j]+a[k] == l){

                m++;
                printf("m is %d j is %d k is %d \n",m,j,k);
                j++;
                k--;
            }else if(a[j]+a[k] > l){
                k--;
            }else {
                j++;
            }
        }

    }

    printf("m is %d \n",m);

}

void triple_for()
{
     int a[] = {-1,-1,-1,0,1,2};
 
     int len = sizeof(a) / sizeof(int);
 
     int max = len * (len-1) * (len - 2)/6;
 
     int result[max][3];
     memset(result,0,sizeof(result));

     int m = 0;
 
     for(int i = 0;i<len ; i++){
         if (i == 0 || a[i] != a[i-1]){
             for (int j = i+1;j<len ;j++){
                if(j == i+1 || a[j] != a[j-1]){
                     for(int k = j+1;k <len;k++){
                        if(a[i]+a[j]+a[k] == -3){
                             result[m][0] = a[i];
                             result[m][1] = a[j];
                             result[m][2] = a[k];
                             printf("m0 is %d m1 is %d m2 is %d \n",result[m][0],result[m][1],result[m][2]);
                             m++;
                             break;

                        }
                     }
                 }
             }
         }
     }

     for (int x =0 ; x < m ; x++){
         printf("%d%d%d \n ",result[x][0],result[x][1],result[x][2]);
     }

}

void nearlest(int total){
    int a[] = {
        -33,-5,-2,0,45,90,138,888
    };

    int len = sizeof(a) /sizeof(int);
    int d = a[0]+a[1]+a[2];
    printf("total is %d \n",total);
    if(d >= total){
        printf("nearlest is %d \n",d);
        return;
    }
    d = a[len-1]+a[len-2]+a[len-3];
    if(d <= total){
        printf("nearlest is %d \n",d);
        return;
    }

    int nearlest = total - a[0]-a[1]-a[2];
    for (int i = 0;i< len ;i++){
        int j = i+1;
        int k = len-1;

        while(j<k){
            int m = a[i]+a[j]+a[k];
            int dis = 0;
            int dif = m - total;
            if(dif > 0){
                dis = dif;
                if(dis < nearlest){
                    nearlest = dis;
                    d = m;
                }
                k--;
            }else if(dif < 0){
                dis = -dif;
                if(dis < nearlest){
                    nearlest = dis;
                    d = m;
                }
                j++;
            }else{
                nearlest = 0;
                printf("nearlest is 0");
                return;
            }
        }
    }

    printf("nearlest is %d dis is %d \n",d,nearlest);


}
