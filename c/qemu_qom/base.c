#include "base.h"
#include <stdio.h>

Base* Base_new(void)
{
    return (Base*)object_new(TYPE_BASE);
}

static void say(void *obj)
{
    printf("%s\n", BASE(obj)->greeting);
}

static void instance_init(Object *obj)
{
    Base *This = BASE(obj);
    This->greeting = "Hello, I am base instance";
}

static void class_init(ObjectClass *oc, void *data)
{
    BaseClass *base = BASE_CLASS(oc);
    base->say = say;
}

static const TypeInfo type_info = {
    .name = TYPE_BASE,
    .parent = TYPE_OBJECT,
    .abstract = false,
    .instance_size = sizeof(Base),
    .instance_init = instance_init,
    .class_size = sizeof(BaseClass),
    .class_init = class_init,
};

void Base_register(void)
{
    type_register_static(&type_info);
}
