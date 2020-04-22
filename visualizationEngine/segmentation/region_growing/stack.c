#include "stack.h"

void stack_init(stack * S) {
    S->n_elements = 0;
    S->top = NULL;
}

void element_init(element * el, int i, int j, int k) {
    el->next = NULL;
    el->i = i;
    el->j = j;
    el->k = k;
}

void stack_push(stack * S, element * el) {
    // Increment number of elements.
    S->n_elements++;
    // Set el to point to current stack top as its next element.
    el->next = (S->top);
    // Set el to be the top element of S.
    S->top = el;
}

element * stack_pop(stack * S) {
    element * el;

    if (S->n_elements == 0) {
        // Return NULL pointer if stack is empty.
        return NULL;
    }
    else {
        // Decrement stack count and set `el` to the top element of stack.
        S->n_elements--;
        el = S->top;

        // If stack is empty after pop, then set the top element
        // to the NULL pointer. Otherwise, set the stack top to the
        // next element after top.
        if (S->n_elements == 0)
            S->top = NULL;
        else
            S->top = el->next;

        return el;
    }
}

