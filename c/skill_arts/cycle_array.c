#include <stdio.h>

#define for_each_node(_i) \
    int __temp_node_idx ## _i = 0; \
        for ((_i) = tos_node_id; \
            __temp_node_idx ## _i < tos_nr_nodes; \
            __temp_node_idx ## _i ++, (_i) = ((_i)+1) & (tos_nr_nodes-1))

int main()
{
    int array[8] = {1, 2, 3, 4, 5, 6, 7, 8}; // length should be 2^x
    int tos_nr_nodes = sizeof(array)/sizeof(int);

    int tos_node_id = 3;
    int i = 0;

    for_each_node(i) {
        printf("%d ", i);
    }

    printf("\n");
    return 0;
}
