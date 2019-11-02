#include <stdio.h>
#include <unistd.h>

void func_test1()
{
    static int count = 0;
    count++;
    printf("start func_test1, count is %d\n", count);
    sleep(1);
    printf("end func_test1...\n");
}

