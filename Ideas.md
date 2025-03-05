# Gem Todos
---

- [ ] first class functions
- [ ] generic functions (parameters without a type)
- [ ] function overloading (like generic functions but do different things based on the parameter types)
```
func add(int a, int b) -> int {
    return a + b
}

func add(float a, float b) -> float {
    return a + b
}

add(1, 2)
add(1.0, 2.0)
// add("Hello ", "world") // error: no matching overload
```
- [ ] function parameter references using `&`
```
func references(int& a) {
    a += 50
}

a = 10
references(a)
print(a) // 60
```
- [ ] `enum` keyword
- [ ] type extensions
```
func int.increase_by_one(int& i) -> int {
    i += 1
}

int a = 10
a.increase_by_one()
print(a) // 11
```
- [ ] `defer` keyword
- [ ] `extern` keyword
- [ ] optionals
```
func optional_func(int? a) -> int {
    if a.has_value {
        return a.value
    } else {
        return 0
    }
}

print(optional_func(10)) // 10
print(optional_func(nil)) // 0
```
- [x] `string`
    - [ ] `string.contains(string substr)`
    - [ ] `string.startswith(string prefix)`
    - [ ] `string.endswith(string suffix)`
    - [ ] `string.replace(string old, string replacement)`
    - [ ] `string.split(string sep)`
    - [ ] `string.find(string substr)`
    - [ ] `string.repeat(int times)`
    - [ ] `string.lowercased`
    - [ ] `string.uppercased`
    - [ ] `string.capitalized`
    - [ ] `string.trimmed`
    - [ ] `string.stripped`
- [ ] `StringBuilder` class
    - [ ] `.new(int? capacity)`
    - [ ] `.append(string contents)`
    - [ ] `.length`
    - [ ] `.clear()`
    - [ ] `.capacity`
- [ ] `System` class
    - [x] `System.exit(int? code)`
    - [ ] `System.sleep(int milliseconds)`
    - [ ] `System.get_env(string key)`
    - [ ] `System.set_env(string key, string value)`
    - [ ] `System.cwd`
    - [ ] `System.admin`
    - [x] `System.os`
    - [x] `System.pid`
    - [ ] `System.processor_count`
    - [ ] `System.cpu_usage`
    - [ ] `System.memory_usage`
    - [ ] `System.cursor_pos`
    - [ ] `System.atexit(() -> nil callback)`
    - [x] `System.shell(string command)`
    - [ ] `System.block_input()`
    - [ ] `System.clipboard`
    - [ ] `System.set_clipboard(string contents)`
    - [ ] `System.unblock_input()`
    - [ ] `System.is_key_pressed(string key)`
    - [ ] `System.is_mouse_pressed(int button)`
- [ ] `threads` library
    - [ ] `threads.current_thread()`
    - [ ] `threads.Thread`
        - [ ] `.new(function callback)`
        - [ ] `.start()`
        - [ ] `.join()`
        - [ ] `.is_alive`
        - [ ] `.terminate()`
        - [ ] `.id`
        - [ ] `.name`
    - [ ] `threads.MutexLock`
        - [ ] `.new()`
        - [ ] `.lock()`
        - [ ] `.unlock()`
        - [ ] `.is_locked`
    - [ ] `threads.Semaphore`
        - [ ] `.new(int count)`
        - [ ] `.acquire()`
        - [ ] `.release()`
        - [ ] `.count`
- [ ] `LL` (Low Level) library
    - [ ] `LL.Pointer`
        - [ ] `.new(int size)`
        - [ ] `.free()`
        - [ ] `.value`
        - [ ] `.zero()`
        - [ ] `.realloc(int size)`
        - [ ] `.write(any data)`
        - [ ] `.read(int size)`
        - [ ] `.set(any value, int size)`
        - [ ] `.copy(LL.Pointer other)`
        - [ ] `.move(LL.Pointer other)`
        - [ ] `.offset(int offset)`
    - [ ] `LL.asm(string asm_code)`
    - [ ] `LL.Process`
        - [ ] `.new()` -- opens current process
        - [ ] `.new(string name)`
        - [ ] `.new(int pid)`
        - [ ] `.read(int address)`
        - [ ] `.write(int address, string content)`
        - [ ] `.close()`
        - [ ] `.pid`
        - [ ] `.name`
- [ ] `fstream` library
    - [ ] `fstream.File`
        - [ ] `.new(string path)`
        - [ ] `.close()`
        - [ ] `.contents`
        - [ ] `.write(string contents)`
        - [ ] `.extension`
        - [ ] `.name`
        - [ ] `.absolute`
        - [ ] `.exists`
        - [ ] `.is_file`
        - [ ] `.is_dir`
    - [ ] `fstream.GzipCompressor`
        - [ ] `.compress(string | fstream.File content)`
        - [ ] `.decompress(string | fstream.File content)`
    - [ ] `fstream.ZlibCompressor`
        - [ ] `.compress(string | fstream.File content)`
        - [ ] `.decompress(string | fstream.File content)`
    - [ ] `fstream.LogFile`
        - [ ] `.new(fstream.File | string file)`
        - [ ] `.log_info(string)`
        - [ ] `.log_warning(string)`
        - [ ] `.log_error(string)`
    - [ ] `fstream.ImageFile`
        - [ ] `.new(fstream.File | string file)`
        - [ ] `.width`
        - [ ] `.height`
        - [ ] `.color_at(int x, int y)`
        - [ ] `.draw_line(int x, int y, int to_x, int to_y, color.Color? color)`
- [ ] `text` library
    - [ ] `text.sha1(string content)`
    - [ ] `text.sha256(string content)`
    - [ ] `text.sha3(string content)`
    - [ ] `text.sha512(string content)`
    - [ ] `text.md5(string content)`
    - [ ] `text.b64_encode(string content)`
    - [ ] `text.b64_decode(string content)`
    - [ ] `text.parse_json(string content)`
    - [ ] `text.parse_xml(string content)`
    - [ ] `text.parse_html(string content)`
    - [ ] `text.parse_csv(string content)`
    - [ ] `text.parse_yaml(string content)`
    - [ ] `text.parse_toml(string content)`
    - [ ] `text.parse_ini(string content)`
    - [ ] `text.parse_markdown(string content)`
    - [ ] `text.Regex`
        - [ ] `.new(string pattern)`
        - [ ] `.match(string s)`
        - [ ] `.replace(string s)`
        - [ ] `.split(string s)`
        - [ ] `.find(string s)`
        - [ ] `.find_all(string s)`
        - [ ] `.search(string s)`
        - [ ] `.count(string s)`
- [ ] `serialize` library
    - [ ] `serialize.Serializer`
        - [ ] `.new()`
        - [ ] `.serialize(any data)`
        - [ ] `.deserialize(any serialized_data)`
- [ ] `iterables` library
    - [ ] `iterables.LinkedList<T>`
        - [ ] `.new()`
        - [ ] `.append_back(T value)`
        - [ ] `.append_front(T value)`
        - [ ] `.append_after(int index, T value)`
        - [ ] `.get(int index)`
        - [ ] `.remove(T value)`
        - [ ] `.remove_at(int index)`
        - [ ] `.clear()`
        - [ ] `.length`
        - [ ] `.is_empty`
    - [ ] `iterables.Stack<T>`
        - [ ] `.new()`
        - [ ] `.push(T value)`
        - [ ] `.pop()`
        - [ ] `.peek()`
        - [ ] `.clear()`
        - [ ] `.length`
        - [ ] `.is_empty`
    - [ ] `iterables.Queue<T>`
        - [ ] `.new()`
        - [ ] `.enqueue(T value)`
        - [ ] `.dequeue()`
        - [ ] `.peek()`
        - [ ] `.clear()`
        - [ ] `.length`
        - [ ] `.is_empty`
    - [ ] `iterables.Buffer<T>`
        - [ ] `.new(int capacity)`
        - [ ] `.add(T value)`
        - [ ] `.get(int index)`
        - [ ] `.remove(T value)`
        - [ ] `.clear()`
        - [ ] `.length`
        - [ ] `.is_empty`
        - [ ] `.is_full`
- [ ] `color` library
    - [ ] `color.Color`
        - [ ] `.new(int r, int g, int b, int? a)`
        - [ ] `.r`
        - [ ] `.g`
        - [ ] `.b`
        - [ ] `.a`
        - [ ] `.hex`
        - [ ] `.h`
        - [ ] `.s`
        - [ ] `.v`
- [ ] `lua` library
    - [ ] `lua.Lua`
        - [ ] `.new()`
        - [ ] `.load_file(fstream.File | string file)`
- [ ] `http` library
    - [ ] `http.get(string url)`
    - [ ] `http.post(string url, string data)`
