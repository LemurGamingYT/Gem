; ModuleID = "core"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

%"string" = type {i8*, i32}
define %"string" @"string.new"(i8* %"ptr_param", i32 %"length_param")
{
entry:
  %"ptr_ptr" = alloca i8*
  store i8* %"ptr_param", i8** %"ptr_ptr"
  %"length_ptr" = alloca i32
  store i32 %"length_param", i32* %"length_ptr"
  %"length" = load i32, i32* %"length_ptr"
  %"int.+.int" = add i32 %"length", 1
  %"__alloc" = call i8* @"malloc"(i32 %"int.+.int")
  %"__alloc_ptr" = icmp eq i8* %"__alloc", null
  br i1 %"__alloc_ptr", label %"entry.if", label %"entry.endif", !prof !0
entry.if:
  call void @"puts"(i8* getelementptr ([14 x i8], [14 x i8]* @"str", i32 0, i32 0))
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

@"str" = internal constant [14 x i8] c"out of memory\00"
declare external void @"llvm.memcpy.p0.p0.i32"(i8* %".1", i8* %".2", i32 %".3", i1 %".4")

define %"string" @"int.to_string"(i32 %"i_param")
{
entry:
  %"i_ptr" = alloca i32
  store i32 %"i_param", i32* %"i_ptr"
  %"__buffer" = getelementptr inbounds [16 x i8], [16 x i8]* @"buf", i32 0, i32 0
  %"buf_ptr" = alloca i8*
  store i8* %"__buffer", i8** %"buf_ptr"
  %"buf" = load i8*, i8** %"buf_ptr"
  %"i" = load i32, i32* %"i_ptr"
  %"int_fmt" = getelementptr inbounds [3 x i8], [3 x i8]* @"int_fmt", i32 0, i32 0
  %"__format_int" = call i32 (i8*, i32, i8*, ...) @"snprintf"(i8* %"buf", i32 16, i8* %"int_fmt", i32 %"i")
  %"length_ptr" = alloca i32
  store i32 %"__format_int", i32* %"length_ptr"
  %"buf.1" = load i8*, i8** %"buf_ptr"
  %"length" = load i32, i32* %"length_ptr"
  %"buf.2" = load i8*, i8** %"buf_ptr"
  %"length.1" = load i32, i32* %"length_ptr"
  %"string.new" = call %"string" @"string.new"(i8* %"buf.2", i32 %"length.1")
  ret %"string" %"string.new"
}

@"buf" = internal global [16 x i8] zeroinitializer
declare external i32 @"snprintf"(i8* %".1", i32 %".2", i8* %".3", ...)

@"int_fmt" = internal constant [3 x i8] c"%d\00"
define %"string" @"float.to_string"(float %"f_param")
{
entry:
  %"f_ptr" = alloca float
  store float %"f_param", float* %"f_ptr"
  %"__buffer" = getelementptr inbounds [64 x i8], [64 x i8]* @"buf.1", i32 0, i32 0
  %"buf_ptr" = alloca i8*
  store i8* %"__buffer", i8** %"buf_ptr"
  %"buf" = load i8*, i8** %"buf_ptr"
  %"f" = load float, float* %"f_ptr"
  %"float_fmt" = getelementptr inbounds [3 x i8], [3 x i8]* @"float_fmt", i32 0, i32 0
  %"__format_float" = call i32 (i8*, i32, i8*, ...) @"snprintf"(i8* %"buf", i32 64, i8* %"float_fmt", float %"f")
  %"length_ptr" = alloca i32
  store i32 %"__format_float", i32* %"length_ptr"
  %"buf.1" = load i8*, i8** %"buf_ptr"
  %"length" = load i32, i32* %"length_ptr"
  %"buf.2" = load i8*, i8** %"buf_ptr"
  %"length.1" = load i32, i32* %"length_ptr"
  %"string.new" = call %"string" @"string.new"(i8* %"buf.2", i32 %"length.1")
  ret %"string" %"string.new"
}

@"buf.1" = internal global [64 x i8] zeroinitializer
@"float_fmt" = internal constant [3 x i8] c"%f\00"
define %"string" @"string.to_string"(%"string" %"s_param")
{
entry:
  %"s_ptr" = alloca %"string"
  store %"string" %"s_param", %"string"* %"s_ptr"
  %"s" = load %"string", %"string"* %"s_ptr"
  ret %"string" %"s"
}

define %"string" @"bool.to_string"(i1 %"b_param")
{
entry:
  %"b_ptr" = alloca i1
  store i1 %"b_param", i1* %"b_ptr"
  %"b" = load i1, i1* %"b_ptr"
  %"string.new" = call %"string" @"string.new"(i8* getelementptr ([5 x i8], [5 x i8]* @"str.2", i32 0, i32 0), i32 4)
  %"string.new.1" = call %"string" @"string.new"(i8* getelementptr ([6 x i8], [6 x i8]* @"str.4", i32 0, i32 0), i32 5)
  %"ternary" = select  i1 %"b", %"string" %"string.new", %"string" %"string.new.1"
  ret %"string" %"ternary"
}

@"str.1" = internal constant [5 x i8] c"true\00"
@"str.2" = internal constant [5 x i8] c"true\00"
@"str.3" = internal constant [6 x i8] c"false\00"
@"str.4" = internal constant [6 x i8] c"false\00"
!0 = !{ !"branch_weights", i32 1, i32 99 }