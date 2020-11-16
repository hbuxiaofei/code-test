#include <stdio.h>

void __attribute__((constructor)) sub2_init(void)
{
    printf("submodule2 constructor run...\n");;
}

void __attribute__((destructor)) sub2_fini(void)
{
    printf("submodule2 destructor run...\n");;
}

int submodule2_run()
{
    printf("Xixi submodule2!\n");
    return 0;
}
