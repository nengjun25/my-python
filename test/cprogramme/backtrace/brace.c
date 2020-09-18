#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int n;

struct node {
    char *s;
    struct node *n; 
} *res;

void main(){
    n = 3;
    
    
}

void add(char *s){
    if (res = NULL){
        res = (struct node*)malloc(sizeof(node));
        res->s = s;
        return;
    }
    struct node *n;
    n = res;

    while (n->next !=NULL ){
        n = n->next;
    }
    
    struct *q = (struct node*)malloc(sizeof(struct node));
    q->s = s;
    q->next = NULL;
    n->next = q;
    
}

int get_size(){
    struct node *n;
    n = res;
    int count = 0;
    while(n != NULL){
        count++;
        n = n -> next;
    }
    return count;
}

void backtrace(char *s,char *trace)
{
    int sl = strlen(*s);
    int tl = strlen(*trace);

    if(tl == 2*n){
        char *p;
        memset(p,0,2*n);
        strcpy(p,trace);
        add(p);
        return;
    }
    
    char left;
    char right;
    for(int i = 0;i<sl;i++){

        trace[tl] = s[i];
        backtrace(*s,trace);
        trace[tl] = 0;

    }

}



