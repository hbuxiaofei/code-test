#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
    struct node * next;
    int data;
} node;

typedef int bool;
typedef bool (* remove_fn)(node const * v);

// Remove all nodes from the supplied list for which the
// supplied remove function returns true.
// Returns the new head of the list.
node *remove_if2(node *head, remove_fn rm)
{
    node *prev = NULL;
    node *curr = NULL;

    for (prev = NULL, curr = head; curr != NULL; ) {
        node *next = curr->next;
        if (rm(curr)) {
            if (prev)
                prev->next = curr->next;
            else
                head = curr->next;
            free(curr);
        } else
        prev = curr;
        curr = next;
    }
    return head;
}

void remove_if(node **head, remove_fn rm)
{
    node **curr = head;

    while (*curr) {
        node *entry = *curr;
        if (rm(entry)) {
            *curr = entry->next;
            free(entry);
        }
        else
            curr = &entry->next;
    }
}

bool is_remove(node const *v)
{
    return !(v->data % 2);
}

void test_remove_if()
{
    struct node *head = malloc(sizeof(struct node));
    head->next = NULL;
    head->data = 0;

    struct node *v = head;

    int nr = 10;
    int i;

    for (i = 0; i < nr; i++) {
        v->next = malloc(sizeof(struct node));
        v->next->next = NULL;
        v->next->data = i + 1;

        v = v->next;
    }

    remove_if(&head, is_remove);

    v = head;
    while (v) {
        printf("%d ", v->data);
        v = v->next;
    }
    printf("\n");

    struct node *tmp = NULL;
    v = head;
    while (v) {
        tmp = v->next;
        free(v);
        v = tmp;
    }
    free(head);
}

int main()
{
    test_remove_if();
    return 0;
}

