#include "Math.h"

#include <math.h>


float Math_pi(void) {
    return 3.14159265358979323846f;
}

float Math_e(void) {
    return 2.71828182845904523536f;
}

float Math_abs(float x) {
    return fabsf(x);
}

float Math_sqrt(float x) {
    return sqrtf(x);
}

float Math_pow(float x, float y) {
    return powf(x, y);
}

float Math_exp(float x) {
    return expf(x);
}

float Math_log(float x) {
    return logf(x);
}

float Math_log10(float x) {
    return log10f(x);
}

int Math_floor(float x) {
    return (int)floorf(x);
}

int Math_ceil(float x) {
    return (int)ceilf(x);
}

int Math_round(float x) {
    return (int)roundf(x);
}

float Math_sin(float x) {
    return sinf(x);
}

float Math_cos(float x) {
    return cosf(x);
}

float Math_tan(float x) {
    return tanf(x);
}
