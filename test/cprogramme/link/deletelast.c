#include<stdio.h>
#include<stdlib.h>

struct node {
    struct node *next;
    int data;
};

struct node *create_node();
struct node *switch_between();

void main()
{
    struct node *head;
    struct node *head2;

    head = create_node(10);
    //head2 = create_node(3);
    
        
    //delete_last_n(head,2);
    printf("head is %d \n",head->data); 
    // merge_two_link(head,head2);
    head2 = switch_between(head);
    struct node *p;
    p = head2;
    while(p !=NULL){
        printf("p data is %d \n",p->data);
        p = p->next;
    }


}

struct node *create_node(int num){
    struct node *head;
    struct node *p;
    struct node *q;
    head = 0;
    for (int i = 0;i< num;i++){
        p=(struct node *)malloc(sizeof(struct node));
        p->data = i+1;
        
        if(head == 0){
            head = p;
            q = p;
        }else{
            q->next = p;
            q = p;
        }
    }
    q->next = NULL;
    return head;
}

void delete_last_n(struct node *head,int n)
{
    int i = 1;
    int k = 0;
    struct node *no;
    no = head;
    while(no->next != NULL){
        i++;
        no = no->next;
    }
    struct node *no2;
    no2 = head;
    while(no2 != NULL){
        printf("k is %d data is %d \n",k,no2->data);
        if(k+n == i-1){
            struct node *p = no2->next;
            if (p != NULL){
                no2->next = p->next;
                free(p);
            }
            break;
        }
        no2 = no2->next;
        k++;
    }

}

void merge_two_link(struct node *head1,struct node *head2){
    struct node *head3;
    struct node *q;
    head3 = NULL;
     
    while(head1 != NULL || head2 != NULL){
        printf("no1 null %d no2 null %d \n",(head1 == NULL),(head2 ==NULL));
        struct node *t;
        if(head1 == NULL){
            t = head2;
            head2 = head2->next;
            printf("merge no2 \n");
        }else if(head2 == NULL){
            t = head1;
            head1 = head1->next;
            printf("merge no1 \n");
        }else if(head1->data <= head2->data){
            t = head1;
            head1 = head1->next;
            printf("merge no1 \n");
        }else {
            t= head2;
            head2 = head2->next;
            printf("merge no2 \n");
        }
        
        if(head3 ==NULL){
            head3 = t;
            q = t;
        }else{
            q->next = t ;
            q = t;
        }


         
    }
    q->next = NULL;

    struct node *p;
    p = head3;
    while(p != NULL){
        printf("%d \n",p->data);
        p = p->next;
    }
    
}

struct node *switch_between(struct node *head){
    
    struct node *p,*q,*head1,*t;
    
    t = NULL;
    head1 = 0;
    p = head;
    printf("p is %d \n",p->next->data);
    q = p->next;
    
    printf("loop 11111 \n");
    while (p != NULL && q != NULL){
        p->next = q->next;
        q->next = p;
        if(t != NULL){
            t->next = q;
        }
        if(head1 == 0){
            head1 = q;
        }

        t = p;
        p=p->next;
        if (p != NULL){
            q=p->next;
        }

    }
    
    return head1;

}

void has_circle(struct node *head){
    struct node *p,*q;

    p = head;
    q = head;
    int h = 0;
    int d = 0;
    int index;

    while(p != NULL && p->next != NULL){
        if (p == q){
            break
        }

        p = p->next->next;

        q = q->next;

        d++;

    }

    if (p == NULL || p->next = NULL){
        return
    }

    struct node *r;
    r = head;

    while(p != r){
        p = p->next;
        r = r->next;
        index++;
    }

    int t = 0;

    struct node *m;
    m = q;
    while (q != m){
        q = q -> next;
        t++;
    }
    
    int l = t+index;

}

