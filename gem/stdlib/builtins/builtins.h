#pragma once


typedef char i8;
typedef unsigned long long u64;
typedef void* nil;
typedef int bool;
#define true 1
#define false 0

// @public
typedef struct {
    i8* buf;
    u64 len;
} string;

typedef struct {
    void* ptr;
    u64 ref_count;
} Ref;

Ref Ref_new(void* ptr);
nil Ref_inc(Ref* ref);
nil Ref_dec(Ref* ref);

// @public
typedef struct {
    Ref** elements;
    int len, cap;
} array;


// @public
array array_new(void);

// @public
nil free_array(array* a);

// @public @property
int array_length(array a);

// @public @property
int array_capacity(array a);

// @public @method
nil array_reserve(array* a, int new_cap);

// @public @method
nil array_insert(array* a, int index, Ref* elem);

// @public @method
nil array_add(array* a, Ref* elem);

// @public @method
nil array_add_all(array* a, array b);

// @public @method
nil array_clear(array* a);

// @public @method
nil array_remove_at(array* a, int index);

// @public method
nil array_remove(array* a, void* elem);

// @public @method
int array_find(array a, void* elem);

// @public @method
Ref* array_get(array a, int index);


// @public @method
string int_to_string(int i);

// @public @method
string float_to_string(float f);

// @public @method
string string_to_string(string s);

// @public @method
string bool_to_string(bool b);

// @public @method
int float_to_int(float f);

// @public @method
float int_to_float(int i);


void error(const i8* msg);

string input(void);


string make_string(i8* str, const u64 len);

// @public
nil free_string(string* s);

// @public @property
int string_length(string s);

// @public @property
bool string_is_empty(string s);

// @public @method
string string_copy(string s);

// @public @method
string string_at(string s, int index);

// @public
string iter_string(string s, int index);


void geminit(int argc, i8** argv);
void gemexit(void);
void* gemalloc(u64 size);
void* gemrealloc(void* ptr, u64 size);
void gemfree(void* ptr);
