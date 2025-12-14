#include <stdlib.h>
#include <stdarg.h>
#include <stdio.h>


#if _WIN32
// asprintf is not defined on windows - only unix systems
// https://stackoverflow.com/questions/40159892/using-asprintf-on-windows
int vasprintf(char **strp, const char *fmt, va_list ap) {
    // _vscprintf tells you how big the buffer needs to be
    int len = _vscprintf(fmt, ap);
    if (len == -1) {
        return -1;
    }
    size_t size = (size_t)len + 1;
    char *str = malloc(size);
    if (!str) {
        return -1;
    }
    
    int r = vsprintf_s(str, len + 1, fmt, ap);
    if (r == -1) {
        free(str);
        return -1;
    }
    
    *strp = str;
    return r;
}

int asprintf(char **strp, const char *fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    int r = vasprintf(strp, fmt, ap);
    va_end(ap);
    return r;
}
#endif
