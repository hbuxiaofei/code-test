#include <stdio.h>

void __attribute__((constructor)) sub_init(void)
{
    printf("submodule constructor run...\n");;
}

void __attribute__((destructor)) sub_fini(void)
{
    printf("submodule destructor run...\n");;
}

int submodule_run()
{
    printf("Haha submodule!\n");
    return 0;
}
