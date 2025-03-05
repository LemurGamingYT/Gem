#include "builtins.h"

#include <stdlib.h>
#include <string.h>


i8* duplicate_str(i8* str, u64 len) {
    i8* res = (i8*)gemalloc(len + 1);
    if (res == NULL)
        error("out of memory");
    
    memcpy(res, str, len);
    res[len] = '\0';
    return res;
}


string make_string(i8* str, const u64 len) {
    string s;
    s.buf = duplicate_str(str, len);
    s.len = len;
    return s;
}

nil free_string(string* s) {
    if (s->buf == NULL) return NULL;
    gemfree(s->buf);
    s->buf = NULL;
    s->len = 0;

    return NULL;
}

int string_length(string s) { return (int)s.len; }
bool string_is_empty(string s) { return s.len == 0; }
string string_copy(string s) {
    i8* buf = (i8*)gemalloc(s.len + 1);
    if (buf == NULL)
        error("out of memory");
    
    memcpy(buf, s.buf, s.len);
    buf[s.len] = '\0';
    return make_string(buf, s.len);
}

string string_at(string s, int index) {
    if (index < 0 || index >= s.len)
        error("index out of bounds");

    static char buf[2];
    buf[0] = s.buf[index];
    buf[1] = '\0';
    return make_string(buf, 1);
}

string iter_string(string s, int index) {
    return string_at(s, index);
}
