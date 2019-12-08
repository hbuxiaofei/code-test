package util

/*
#include "util.h"
*/
import "C"

func GoSum(a, b int) _Ctype_int {
	s := C.sum(C.int(a), C.int(b))
	return s
}
