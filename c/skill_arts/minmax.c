#include <stdio.h>

#if HAVE_BUILTIN_TYPES_COMPATIBLE_P
#define MINMAX_ASSERT_COMPATIBLE(a, b) \
	BUILD_ASSERT(__builtin_types_compatible_p(a, b))
#else
#define MINMAX_ASSERT_COMPATIBLE(a, b) \
	do { } while (0)
#endif

#define min(a, b) \
	({ \
		typeof(a) _a = (a); \
		typeof(b) _b = (b); \
		MINMAX_ASSERT_COMPATIBLE(typeof(_a), typeof(_b)); \
		_a < _b ? _a : _b; \
	})

#define max(a, b) \
	({ \
		typeof(a) _a = (a); \
		typeof(b) _b = (b); \
		MINMAX_ASSERT_COMPATIBLE(typeof(_a), typeof(_b)); \
		_a > _b ? _a : _b; \
	})

int main()
{
    printf("min 2 3 is: %d \n", min(2, 3));
    printf("max 2 3 is: %d \n", max(2, 3));
    return 0;
}
