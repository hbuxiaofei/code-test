#include <stdio.h>
#include <unistd.h>
#include "func1.h"

void func()
{
    printf("start func...\n");
    sleep(1);
    printf("end func...\n");
}

int main()
{
    int i = 0;
    for (i = 0; i < 5; i++) {
        func();
        func_test1();
    }
    return 0;
}
