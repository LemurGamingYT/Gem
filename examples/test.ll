; ModuleID = "test"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

%"string" = type {i8*, i32}
declare external %"string" @"string.new"(i8* %".1", i32 %".2")

declare external %"string" @"int.to_string"(i32 %".1")

declare external %"string" @"float.to_string"(float %".1")

declare external %"string" @"string.to_string"(%"string" %".1")

declare external %"string" @"bool.to_string"(i1 %".1")

define i32 @"main"()
{
entry:
  %"string.new" = call %"string" @"string.new"(i8* getelementptr ([14 x i8], [14 x i8]* @"str.1", i32 0, i32 0), i32 13)
  %"s_ptr" = alloca %"string"
  store %"string" %"string.new", %"string"* %"s_ptr"
  ret i32 0
}

@"str" = internal constant [14 x i8] c"Hello, World!\00"
@"str.1" = internal constant [14 x i8] c"Hello, World!\00"