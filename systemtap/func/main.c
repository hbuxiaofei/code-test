#include <stdio.h>
#include <unistd.h>

void func()
{
    printf("start func...\n");
    sleep(2);
    printf("end func...\n");
}

int main()
{
    int i = 0;
    for (i = 0; i < 5; i++) {
        func();
    }
    return 0;
}
