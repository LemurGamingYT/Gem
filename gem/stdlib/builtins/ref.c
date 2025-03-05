#include "builtins.h"

#include <stdlib.h>


Ref Ref_new(void* ptr) {
    return (Ref){ .ptr = ptr, .ref_count = 1 };
}

nil Ref_inc(Ref* ref) {
    ref->ref_count++;
    return NULL;
}

nil Ref_dec(Ref* ref) {
    ref->ref_count--;
    if (ref->ref_count == 0) {
        gemfree(ref->ptr);
    }

    return NULL;
}
