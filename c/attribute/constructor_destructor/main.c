#include <stdio.h>
#include "submodule.h"

void __attribute__((constructor)) init(void)
{
    printf("constructor run...\n");;
}

void __attribute__((destructor)) fini(void)
{
    printf("destructor run...\n");;
}

int main()
{
    printf("Hello world!\n");
    submodule_run();
    return 0;
}
