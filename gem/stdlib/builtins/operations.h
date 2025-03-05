#pragma once

#include "builtins.h"


// @public
int int_add_int(int a, int b);
// @public
int int_sub_int(int a, int b);
// @public
int int_mul_int(int a, int b);
// @public
int int_div_int(int a, int b);
// @public
int int_mod_int(int a, int b);
// @public
int int_pow_int(int a, int b);
// @public
bool int_eq_int(int a, int b);
// @public
bool int_neq_int(int a, int b);
// @public
bool int_gt_int(int a, int b);
// @public
bool int_gte_int(int a, int b);
// @public
bool int_lt_int(int a, int b);
// @public
bool int_lte_int(int a, int b);

// @public
float int_add_float(int a, float b);
// @public
float int_sub_float(int a, float b);
// @public
float int_mul_float(int a, float b);
// @public
float int_div_float(int a, float b);
// @public
float int_mod_float(int a, float b);
// @public
float int_pow_float(int a, float b);
// @public
bool int_eq_float(int a, float b);
// @public
bool int_neq_float(int a, float b);
// @public
bool int_gt_float(int a, float b);
// @public
bool int_gte_float(int a, float b);
// @public
bool int_lt_float(int a, float b);
// @public
bool int_lte_float(int a, float b);

// @public
float float_add_int(float a, int b);
// @public
float float_sub_int(float a, int b);
// @public
float float_mul_int(float a, int b);
// @public
float float_div_int(float a, int b);
// @public
float float_mod_int(float a, int b);
// @public
float float_pow_int(float a, int b);
// @public
bool float_eq_int(float a, int b);
// @public
bool float_neq_int(float a, int b);
// @public
bool float_gt_int(float a, int b);
// @public
bool float_gte_int(float a, int b);
// @public
bool float_lt_int(float a, int b);
// @public
bool float_lte_int(float a, int b);

// @public
float float_add_float(float a, float b);
// @public
float float_sub_float(float a, float b);
// @public
float float_mul_float(float a, float b);
// @public
float float_div_float(float a, float b);
// @public
float float_mod_float(float a, float b);
// @public
float float_pow_float(float a, float b);
// @public
bool float_eq_float(float a, float b);
// @public
bool float_neq_float(float a, float b);
// @public
bool float_gt_float(float a, float b);
// @public
bool float_gte_float(float a, float b);
// @public
bool float_lt_float(float a, float b);
// @public
bool float_lte_float(float a, float b);

// @public
string string_add_string(string a, string b);

// @public
bool string_eq_string(string a, string b);

// @public
bool string_neq_string(string a, string b);

// @public
bool string_gt_string(string a, string b);

// @public
bool string_gte_string(string a, string b);

// @public
bool string_lt_string(string a, string b);

// @public
bool string_lte_string(string a, string b);

// @public
bool bool_eq_bool(bool a, bool b);
// @public
bool bool_neq_bool(bool a, bool b);
// @public
bool bool_and_bool(bool a, bool b);
// @public
bool bool_or_bool(bool a, bool b);
// @public
bool not_bool(bool a);
