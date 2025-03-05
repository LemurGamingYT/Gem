#include "builtins.h"

#include <stdio.h>


#define INT_BUF_SIZE 16
#define FLOAT_BUF_SIZE 64


string int_to_string(int i) {
    static char buf[INT_BUF_SIZE];
    snprintf(buf, INT_BUF_SIZE, "%d", i);
    return make_string(buf, INT_BUF_SIZE);
}

string float_to_string(float f) {
    static char buf[FLOAT_BUF_SIZE];
    snprintf(buf, FLOAT_BUF_SIZE, "%f", f);
    return make_string(buf, FLOAT_BUF_SIZE);
}

string string_to_string(string s) {
    return string_copy(s);
}

string bool_to_string(bool b) {
    return make_string(b ? "true" : "false", b ? 4 : 5);
}

int float_to_int(float f) {
    return (int)f;
}

float int_to_float(int i) {
    return (float)i;
}
