#ifndef REGION_GROWING_REGION_GROWING_H
#define REGION_GROWING_REGION_GROWING_H
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "stack.h"

int map_index(int i, int j, int k, int m, int n, int p);
void add_neighbors(int i, int j, int k, int m, int n, int p, stack * needs_check, bool * checked);
void grow(int m, int n, int p, double * img, bool * seg, int si, int sj, int sk, double t);

#endif //REGION_GROWING_REGION_GROWING_H
