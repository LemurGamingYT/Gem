#pragma once

#include "builtins.h"


// @public @property @static
int System_pid(void);

// @public @property @static
string System_os(void);

// @public @property @static
string System_cwd(void);

// @public @method @static
nil System_exit(int code);

// @public @method @static
int System_shell(string command);
