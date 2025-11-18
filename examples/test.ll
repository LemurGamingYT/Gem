; ModuleID = "test"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

%"string" = type {i8*, i32}
declare void @"panic"(%"string" %"msg_param")

declare i1 @"__is_null"(i8* %"ptr_param")

declare i8* @"__buffer"(i32 %"size_param")

declare %"string" @"__create_string"(i8* %"ptr_param", i32 %"length_param")

declare i8* @"__alloc"(i32 %"size_param")

declare void @"__free"(i8* %"ptr_param")

declare i8* @"__memcpy"(i8* %"dest_param", i8* %"src_param", i32 %"size_param", i1 %"is_volatile_param")

declare i32 @"__format_int"(i8* %"buf_param", i32 %"length_param", i32 %"i_param")

declare i32 @"__format_float"(i8* %"buf_param", i32 %"length_param", float %"f_param")

declare void @"__print_pointer"(i8* %"ptr_param")

declare i32 @"__add_ints"(i32 %"a_param", i32 %"b_param")

declare external %"string" @"string.new"(i8* %".1", i32 %".2")

declare external %"string" @"int.to_string"(i32 %".1")

declare external %"string" @"float.to_string"(float %".1")

declare external %"string" @"string.to_string"(%"string" %".1")

declare external %"string" @"bool.to_string"(i1 %".1")

define i32 @"main"()
{
entry:
  %"string.new" = call %"string" @"new"(i8* getelementptr ([14 x i8], [14 x i8]* @"str.2", i32 0, i32 0), i32 13)
  %"s_ptr" = alloca %"string"
  store %"string" %"string.new", %"string"* %"s_ptr"
  ret i32 0
}

@"str" = internal constant [14 x i8] c"Hello, World!\00"
define %"string" @"new"(i8* %"ptr_param", i32 %"length_param")
{
entry:
  %"ptr_ptr" = alloca i8*
  store i8* %"ptr_param", i8** %"ptr_ptr"
  %"length_ptr" = alloca i32
  store i32 %"length_param", i32* %"length_ptr"
  %"length" = load i32, i32* %"length_ptr"
  %"__add_ints" = add i32 %"length", 1
  %"__alloc" = call i8* @"malloc"(i32 %"__add_ints")
  %"__alloc_ptr" = icmp eq i8* %"__alloc", null
  br i1 %"__alloc_ptr", label %"entry.if", label %"entry.endif"
entry.if:
  call void @"puts"(i8* getelementptr ([14 x i8], [14 x i8]* @"str.1", i32 0, i32 0))
  call void @"exit"(i32 1)
  unreachable
entry.endif:
  %"ptr_copy_ptr" = alloca i8*
  store i8* %"__alloc", i8** %"ptr_copy_ptr"
  %"ptr_copy" = load i8*, i8** %"ptr_copy_ptr"
  %"ptr" = load i8*, i8** %"ptr_ptr"
  %"length.1" = load i32, i32* %"length_ptr"
  call void @"llvm.memcpy.p0.p0.i32"(i8* %"ptr_copy", i8* %"ptr", i32 %"length.1", i1 false)
  %"ptr_copy.1" = load i8*, i8** %"ptr_copy_ptr"
  %"length.2" = load i32, i32* %"length_ptr"
  %"string" = insertvalue %"string" undef, i8* %"ptr_copy.1", 0
  %"string.1" = insertvalue %"string" %"string", i32 %"length.2", 1
  ret %"string" %"string.1"
}

declare external i8* @"malloc"(i32 %".1")

declare external void @"puts"(i8* %".1")

declare external void @"exit"(i32 %".1")

@"str.1" = internal constant [14 x i8] c"out of memory\00"
declare external void @"llvm.memcpy.p0.p0.i32"(i8* %".1", i8* %".2", i32 %".3", i1 %".4")

@"str.2" = internal constant [14 x i8] c"Hello, World!\00"