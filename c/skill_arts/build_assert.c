#include <stdio.h>
#include <stddef.h>

/**
 * BUILD_ASSERT - assert a build-time dependency.
 * @cond: the compile-time condition which must be true.
 *
 * Your compile will fail if the condition isn't true, or can't be evaluated
 * by the compiler.  This can only be used within a function.
 *
 * Example:
 *	#include <stddef.h>
 *	...
 *	static char *foo_to_char(struct foo *foo)
 *	{
 *		// This code needs string to be at start of foo.
 *		BUILD_ASSERT(offsetof(struct foo, string) == 0);
 *		return (char *)foo;
 *	}
 */
#define BUILD_ASSERT(cond) \
	do { (void) sizeof(char [1 - 2*!(cond)]); } while(0)

/**
 * BUILD_ASSERT_OR_ZERO - assert a build-time dependency, as an expression.
 * @cond: the compile-time condition which must be true.
 *
 * Your compile will fail if the condition isn't true, or can't be evaluated
 * by the compiler.  This can be used in an expression: its value is "0".
 *
 * Example:
 *	#define foo_to_char(foo)					\
 *		 ((char *)(foo)						\
 *		  + BUILD_ASSERT_OR_ZERO(offsetof(struct foo, string) == 0))
 */
#define BUILD_ASSERT_OR_ZERO(cond) \
	(sizeof(char [1 - 2*!(cond)]) - 1)


/******************************************************************************/


struct foo {
	char string[5];
	int x;
};

static char *foo_string(struct foo *foo)
{
	// This trick requires that the string be first in the structure
	BUILD_ASSERT(offsetof(struct foo, string) == 0);
	return (char *)foo;
}

#define foo_to_char(_foo) \
    ((char *)(_foo) \
    + BUILD_ASSERT_OR_ZERO(offsetof(struct foo, string) == 0))


int main()
{
    struct foo f;
    char *str1 = NULL;
    char *str2 = NULL;

    str1 = foo_string(&f);
    str2 = foo_to_char(&f);

    printf("f addr is: 0x%x\n", str1);
    printf("f addr is: 0x%x\n", str2);
    return 0;
}
