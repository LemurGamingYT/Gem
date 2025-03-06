#include "builtins.h"

#include <stdlib.h>
#include <stdio.h>

#if OS_WINDOWS
#define MICROSOFT_WINDOWS_WINBASE_H_DEFINE_INTERLOCKED_CPLUSPLUS_OVERLOADS 0
#include <windows.h>

#define _CRTDBG_MAP_ALLOC
#include <crtdbg.h>
#else
#include <locale.h>
#endif


array args;

void error(const i8* msg) {
    fprintf(stderr, "%s\n", msg);
    exit(1);
}

string input(void) {
    static char buf[256];
    if (fgets(buf, sizeof(buf), stdin) != NULL) {
        size_t len = strlen(buf);
        if (len > 0 && buf[len - 1] == '\n') {
            buf[len - 1] = '\0';
            len--;
        }

        return make_string(buf, len);
    }

    return make_string("", 0);
}

string input_prompt(string prompt) {
    printf("%s", prompt.buf);
    return input();
}

void geminit(int argc, i8** argv) {
#if OS_WINDOWS
    SetConsoleOutputCP(CP_UTF8);
    _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#else
    setlocale(LC_ALL, "en_US.UTF-8");
#endif

    args = array_new();
    for (int i = 0; i < argc; i++) {
        Ref elem_ref = Ref_new((void*)(argv[i]));
        array_add(&args, &elem_ref);
    }
}

void gemexit(void) {
#if OS_WINDOWS
    _CrtDumpMemoryLeaks();
#endif

    free_array(&args);
}

void* gemalloc(u64 size) { return malloc(size); }
void* gemrealloc(void* ptr, u64 size) { return realloc(ptr, size); }
void gemfree(void* ptr) { free(ptr); }
