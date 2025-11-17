; ModuleID = "test"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

%"string" = type {i8*, i32}
define i32 @"main"()
{
entry:
  %"string.new" = call %"string" @"new"(i8* getelementptr ([12 x i8], [12 x i8]* @"str.2", i32 0, i32 0), i32 11)
  %"s_ptr" = alloca %"string"
  store %"string" %"string.new", %"string"* %"s_ptr"
  ret i32 0
}

@"str" = internal constant [12 x i8] c"Hello world\00"
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

@"str.2" = internal constant [12 x i8] c"Hello world\00"