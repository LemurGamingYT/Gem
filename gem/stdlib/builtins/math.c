#include "builtins.h"

#include <math.h>


float Math_pi(void) {
    return 3.14159265358979323846f;
}

float Math_abs(float x) {
    return fabsf(x);
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
