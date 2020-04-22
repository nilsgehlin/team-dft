#include "region_growing.h"
#include "math.h"

int inline map_index(int i, int j, int k, int m, int n, int p) {
    return n*p*i + p*j + k;
}

void add_neighbors(int i, int j, int k, int m, int n, int p,
                   stack * needs_check, bool * checked) {
    int l;
    element * el;
    if (i >= 1) {
        l = map_index(i-1,j,k,m,n,p);
        if (!checked[l]) {
            el = (element *) malloc(sizeof(element));
            element_init(el, i-1, j, k);
            stack_push(needs_check, el);
        }
    }

    if (j >= 1) {
        l = map_index(i,j-1,k,m,n,p);
        if (!checked[l]) {
            el = (element *) malloc(sizeof(element));
            element_init(el, i, j-1, k);
            stack_push(needs_check, el);
        }
    }

    if (k >= 1) {
        l = map_index(i,j,k-1,m,n,p);
        if (!checked[l]) {
            el = (element *) malloc(sizeof(element));
            element_init(el, i, j, k-1);
            stack_push(needs_check, el);
        }
    }

    if (i < m-1) {
        l = map_index(i+1,j,k,m,n,p);
        if (!checked[l]) {
            el = (element *) malloc(sizeof(element));
            element_init(el, i+1, j, k);
            stack_push(needs_check, el);
        }
    }

    if (j < n-1) {
        l = map_index(i,j+1,k,m,n,p);
        if (!checked[l]) {
            el = (element *) malloc(sizeof(element));
            element_init(el, i, j+1, k);
            stack_push(needs_check, el);
        }
    }

    if (k < p-1) {
        l = map_index(i,j,k+1,m,n,p);
        if (!checked[l]) {
            el = (element *) malloc(sizeof(element));
            element_init(el, i, j, k+1);
            stack_push(needs_check, el);
        }
    }
}

void grow(int m, int n, int p, double * img, bool * seg, int si, int sj, int sk, double t) {
    int l, i, j, k;
    bool * checked = malloc(sizeof(bool)*m*n*p);
//    bool checked[m*n*p]; // Leads to stack overflow for larger arrays
    stack needs_check;
    element * el;
    for(int ii=0; ii < m*n*p; ii++) {
        seg[ii]     = false;
        checked[ii] = false;
    }
    stack_init(&needs_check);

    l = map_index(si,sj,sk,m,n,p);
    seg[l]     = true;
    checked[l] = true;
    add_neighbors(si, sj, sk, m, n, p, &needs_check, checked);

    stack to_average;
    stack_init(&to_average);
    bool * dummy = malloc(sizeof(bool)*m*n*p);
    add_neighbors(si, sj, sk, m, n, p, &to_average, dummy);
    free(dummy);
    double init_aver = img[l];
    int aver_count = 1;
    while (to_average.n_elements > 0) {
        printf("%d\n", aver_count);
        el = stack_pop(&to_average);
        i = el->i;
        j = el->j;
        k = el->k;
        free(el);
        l = map_index(i, j, k, m, n, p);
        aver_count++;
        init_aver += (img[l] - init_aver) / aver_count;
    }
    double seg_avg = init_aver;
    int count = 1;
    while (needs_check.n_elements > 0) {
        el = stack_pop(&needs_check);
        i = el->i;
        j = el->j;
        k = el->k;
        free(el);

        l = map_index(i, j, k, m, n, p);
        if (checked[l]) continue;

        checked[l] = true;
        if (fabs(img[l] - seg_avg) / (seg_avg) < t) {
            seg[l] = true;
            add_neighbors(i, j, k, m, n, p, &needs_check, checked);
            count++;
            seg_avg += (img[l] - seg_avg) / count;
        }
    }
}