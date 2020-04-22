#ifndef REGION_GROWING_STACK_H
#define REGION_GROWING_STACK_H

#include <stdlib.h>
#include <stdio.h>

// Stack element struct.
// This is a node of singly linked list.
typedef struct element {
    struct element * next;
    int i,j,k;
} element;

// Stack "element" struct.
// The struct has pointer to the next element
// and data, which is three integers, (i,j,k).
typedef struct stack {
    int n_elements;
    element * top;
} stack;

void stack_init(stack * S);
void element_init(element * el, int i, int j, int k);
void stack_push(stack * S, element * el);
element * stack_pop(stack * S);

#endif //REGION_GROWING_STACK_H
