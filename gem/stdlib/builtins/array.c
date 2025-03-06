#include "builtins.h"

#include <stdlib.h>


#define ARRAY_INITIAL_CAPACITY 10


array array_new(void) {
    array a;
    a.len = 0;
    a.cap = ARRAY_INITIAL_CAPACITY;
    a.elements = (Ref**)gemalloc(sizeof(Ref*) * ARRAY_INITIAL_CAPACITY);
    if (a.elements == NULL)
        error("out of memory");
    
    return a;
}

nil free_array(array* a) {
    for (int i = 0; i < a->len; i++)
        Ref_dec(a->elements[i]);

    gemfree(a->elements);
    return NULL;
}

int array_length(array a) { return a.len; }
int array_capacity(array a) { return a.cap; }
nil array_reserve(array* a, int new_cap) {
    if (new_cap <= a->cap)
        return NULL;
    
    a->cap = new_cap;
    a->elements = (Ref**)gemrealloc(a->elements, sizeof(Ref) * a->cap);
    if (a->elements == NULL)
        error("out of memory");
    
    return NULL;
}

nil array_add(array* a, Ref* elem) {
    if (a->len == a->cap)
        array_reserve(a, a->cap * 2);

    a->elements[a->len++] = elem;
    return NULL;
}

nil array_insert(array* a, int index, Ref* elem) {
    if (index < 0)
        index = a->len + index;
    
    if (index < 0 || index > a->len)
        error("index out of bounds");
    
    if (a->len == a->cap)
        array_reserve(a, a->cap * 2);
    
    for (int i = a->len; i > index; i--)
        a->elements[i] = a->elements[i - 1];
    
    a->elements[index] = elem;
    a->len++;
    return NULL;
}

nil array_add_all(array* a, array b) {
    for (int i = 0; i < b.len; i++)
        array_add(a, b.elements[i]);
    
    return NULL;
}

nil array_clear(array* a) {
    for (int i = 0; i < a->len; i++)
        Ref_dec(a->elements[i]);
    
    a->len = 0;
    a->cap = ARRAY_INITIAL_CAPACITY;
    return NULL;
}

nil array_remove_at(array* a, int index) {
    if (index < 0)
        index = a->len + index;

    if (index < 0 || index >= a->len)
        error("index out of bounds");
    
    Ref_dec(a->elements[index]);
    for (int i = index; i < a->len - 1; i++)
        a->elements[i] = a->elements[i + 1];
    
    a->len--;
    return NULL;
}

nil array_remove(array* a, void* elem) {
    for (int i = 0; i < a->len; i++) {
        if (a->elements[i]->ptr == elem) {
            array_remove_at(a, (int)i);
            break;
        }
    }

    return NULL;
}

int array_find(array a, void* elem) {
    for (int i = 0; i < a.len; i++) {
        if (a.elements[i]->ptr == elem) return (int)i;
    }

    return -1;
}

Ref* array_get(array a, int index) {
    if (index < 0)
        index = a.len + index;
    
    if (index < 0 || index >= a.len)
        error("index out of bounds");

    return a.elements[index];
}
