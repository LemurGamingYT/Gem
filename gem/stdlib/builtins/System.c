#include "System.h"

#include <stdio.h> // FILENAME_MAX


#if OS_WINDOWS
#include <windows.h>

#define OS_NAME "Windows"
#define getpid GetCurrentProcessId
#define getcwd GetCurrentDirectory
#elif OS_LINUX
#include <unistd.h>

#if OS_LINUX
#define OS_NAME "Linux"
#else
#define OS_NAME "MacOS"
#endif
#endif


int System_pid(void) { return getpid(); }
string System_os(void) { return make_string(OS_NAME, sizeof(OS_NAME) - 1); }
string System_cwd(void) {
    static char buf[FILENAME_MAX];
    getcwd(FILENAME_MAX, buf);
    return make_string(buf, FILENAME_MAX - 1);
}

nil System_exit(int code) {
    exit(code);
    return NULL;
}

int System_shell(string command) { return system(command.buf); }
