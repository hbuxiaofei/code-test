/**
 * From: http://ccodearchive.net/info/version.html
 */

#include <stdio.h>
#include <stdint.h>

struct version {
    uint32_t _v; /* major << 16  | minor */
};

/**
 * version_major - return the major version of the given struct
 * @v: the version number to obtain the major number from
 */
static inline uint16_t version_major(struct version v) {
    return (v._v & 0xFFFF0000) >> 16;
}

/**
 * version_minor - return the minor version of the given struct
 * @v: the version number to obtain the minor number from
 */
static inline uint16_t version_minor(const struct version v) {
    return v._v & 0xFFFF;
}

/**
 * version - create a new version number
 * @major: major version number
 * @minor: minor version number
 */
static inline struct version version(uint16_t major, uint16_t minor)
{
    struct version v = { ._v = major << 16 | minor };
    return v;
}

/**
 * version_cmp - compare two versions
 * @a: the first version number
 * @b: the second version number
 * @return a number greater, equal, or less than 0 if a is greater, equal or
 * less than b, respectively
 *
 * Example:
 *  struct version a = version(1, 0);
 *  struct version b = version(1, 3);
 *  if (version_cmp(a, b) < 0)
 *      printf("b is smaller than b\n");
 */
static inline int version_cmp(struct version a, struct version b)
{
    return  (a._v == b._v) ? 0 : (a._v > b._v) ? 1 : - 1;
}

int main()
{
    struct version a = version(1, 0);
    struct version b = version(2, 2);

    if (version_cmp(a, b) < 0)
        printf("Feature supported in version 2.2 but we have %d.%d\n",
                version_major(a), version_minor(a));

    if (version_cmp(a, version(3, 4)) < 0)
        printf("Feature only supported in version 3.4\n");

    return 0;
}
