#include "operations.h"

#include <stdlib.h>
#include <string.h>
#include <math.h>


int int_add_int(int a, int b) { return a + b; }
int int_sub_int(int a, int b) { return a - b; }
int int_mul_int(int a, int b) { return a * b; }
int int_div_int(int a, int b) { return a / b; }
int int_mod_int(int a, int b) { return a % b; }
int int_pow_int(int a, int b) { return (int)powf((float)a, (float)b); }
bool int_eq_int(int a, int b) { return a == b; }
bool int_neq_int(int a, int b) { return a != b; }
bool int_gt_int(int a, int b) { return a > b; }
bool int_gte_int(int a, int b) { return a >= b; }
bool int_lt_int(int a, int b) { return a < b; }
bool int_lte_int(int a, int b) { return a <= b; }

float int_add_float(int a, float b) { return a + b; }
float int_sub_float(int a, float b) { return a - b; }
float int_mul_float(int a, float b) { return a * b; }
float int_div_float(int a, float b) { return a / b; }
float int_mod_float(int a, float b) { return fmodf((float)a, b); }
float int_pow_float(int a, float b) { return powf((float)a, b); }
bool int_eq_float(int a, float b) { return a == b; }
bool int_neq_float(int a, float b) { return a != b; }
bool int_gt_float(int a, float b) { return a > b; }
bool int_gte_float(int a, float b) { return a >= b; }
bool int_lt_float(int a, float b) { return a < b; }
bool int_lte_float(int a, float b) { return a <= b; }

float float_add_int(float a, int b) { return a + b; }
float float_sub_int(float a, int b) { return a - b; }
float float_mul_int(float a, int b) { return a * b; }
float float_div_int(float a, int b) { return a / b; }
float float_mod_int(float a, int b) { return fmodf(a, (float)b); }
float float_pow_int(float a, int b) { return powf(a, (float)b); }
bool float_eq_int(float a, int b) { return a == b; }
bool float_neq_int(float a, int b) { return a != b; }
bool float_gt_int(float a, int b) { return a > b; }
bool float_gte_int(float a, int b) { return a >= b; }
bool float_lt_int(float a, int b) { return a < b; }
bool float_lte_int(float a, int b) { return a <= b; }

float float_add_float(float a, float b) { return a + b; }
float float_sub_float(float a, float b) { return a - b; }
float float_mul_float(float a, float b) { return a * b; }
float float_div_float(float a, float b) { return a / b; }
float float_mod_float(float a, float b) { return fmodf(a, b); }
float float_pow_float(float a, float b) { return powf(a, b); }
bool float_eq_float(float a, float b) { return a == b; }
bool float_neq_float(float a, float b) { return a != b; }
bool float_gt_float(float a, float b) { return a > b; }
bool float_gte_float(float a, float b) { return a >= b; }
bool float_lt_float(float a, float b) { return a < b; }
bool float_lte_float(float a, float b) { return a <= b; }

bool bool_eq_bool(bool a, bool b) { return a == b; }
bool bool_neq_bool(bool a, bool b) { return a != b; }
bool bool_and_bool(bool a, bool b) { return a && b; }
bool bool_or_bool(bool a, bool b) { return a || b; }
bool not_bool(bool a) { return !a; }

string string_add_string(string a, string b) {
    u64 len = string_length(a) + string_length(b);
    i8* buf = (i8*)gemalloc(sizeof(i8) * (len + 1));
    if (buf == NULL)
        return make_string("NULL", 4);

    memcpy(buf, a.buf, string_length(a));
    memcpy(buf + string_length(a), b.buf, string_length(b));
    buf[len] = '\0';
    return make_string(buf, len);
}

bool string_eq_string(string a, string b) {
    return strcmp(a.buf, b.buf) == 0;
}

bool string_neq_string(string a, string b) {
    return strcmp(a.buf, b.buf) != 0;
}

bool string_gt_string(string a, string b) {
    return a.len > b.len;
}

bool string_gte_string(string a, string b) {
    return a.len >= b.len;
}

bool string_lt_string(string a, string b) {
    return a.len < b.len;
}

bool string_lte_string(string a, string b) {
    return a.len <= b.len;
}
