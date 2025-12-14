from typing import Any, Optional, Callable, Iterable

from llvmlite import ir, binding as llvm


def NULL(type: Optional[ir.Type] = None):
    """Returns the NULL value of the type"""
    if type is None:
        type = ir.IntType(8).as_pointer() # void*
    
    if not isinstance(type, ir.PointerType):
        type = ir.PointerType(type)
    
    return ir.Constant(type, None)

def NULL_BYTE():
    """Returns a null-terminator (\\0)"""
    return ir.Constant(ir.IntType(8), 0) # \0

def zero(int_width: int):
    """Returns an integer constant with the given width with a value of 0"""
    return ir.Constant(ir.IntType(int_width), 0)

def llint(value: int, int_width: int = 32):
    """Returns an integer constant with the given width and value"""
    return ir.Constant(ir.IntType(int_width), value)

def sizeof(module: ir.Module, llvm_type: ir.Type, width: int = 32):
    """Get the size of a type at compile-time in bytes"""

    data = llvm.create_target_data(module.data_layout)
    return ir.Constant(ir.IntType(width), llvm_type.get_abi_size(data, module.context))

def index_of_type(type: ir.LiteralStructType | ir.IdentifiedStructType, elem_type: ir.Type):
    """Find the index of a type in a structure type (returns -1 if the type is not found)"""
    ref_index = -1
    elements = type.elements
    if elements is None:
        return ref_index
    
    for i, elem in enumerate(elements):
        if elem != elem_type:
            continue

        ref_index = i
        break

    return ref_index

def cast_value(builder: ir.IRBuilder, value: ir.Value, type: ir.Type, name: str = '') -> ir.Value:
    """Converts the value to the type in any possible way"""
    value_type = value.type
    if isinstance(type, ir.IntType) and isinstance(value_type, ir.IntType):
        if type.width > value_type.width:
            return builder.sext(value, type, name)
        elif type.width < value_type.width:
            return builder.trunc(value, type, name)
        else:
            # type.width == value_type.width
            return value
    elif isinstance(type, ir.FloatType) and isinstance(value_type, ir.IntType):
        return builder.sitofp(value, type, name)
    elif isinstance(type, ir.IntType) and isinstance(value_type, ir.FloatType):
        return builder.fptosi(value, type, name)
    elif isinstance(type, ir.DoubleType) and isinstance(value_type, ir.FloatType):
        return builder.fpext(value, type, name)
    elif isinstance(type, ir.FloatType) and isinstance(value_type, ir.DoubleType):
        return builder.fptrunc(value, type, name)
    elif isinstance(type, ir.IntType) and isinstance(value_type, ir.PointerType):
        return builder.ptrtoint(value, type, name)
    elif isinstance(type, ir.PointerType) and isinstance(value_type, ir.IntType):
        return builder.inttoptr(value, type, name)
    elif isinstance(type, ir.PointerType) and isinstance(value_type, ir.PointerType):
        return builder.bitcast(value, type, name)
    
    raise NotImplementedError(f'{value_type} -> {type}')

def get_or_add_global(module: ir.Module, name: str, global_value: Any, **kwargs):
    """Gets or adds a global value"""
    if name in module.globals:
        return module.get_global(name)
    
    module.add_global(global_value)
    for k, v in kwargs.items():
        setattr(global_value, k, v)
    
    return global_value

def define_identified_type(
    name: str, types: Iterable[ir.Type], context: ir.Context = ir.global_context
):
    typ = context.get_identified_type(name)
    if typ.is_opaque:
        typ.set_body(*types)
    
    return typ

def get_ptr(instr: ir.LoadInstr):
    """Get pointer from a load instruction"""
    return instr.operands[0]

def allocate(builder: ir.IRBuilder, value: ir.Value, name: str = ''):
    """Allocate a value on the stack as a pointer"""
    
    ptr = builder.alloca(value.type, name=name)
    builder.store(value, ptr)
    
    return ptr


def max_value(bits: int):
    return 2 ** (bits - 1) - 1

def min_value(bits: int):
    return -2 ** (bits - 1)


def create_struct_value(
    builder: ir.IRBuilder, struct_type: ir.Type, field_values: list[ir.Value],
    name: str = ''
):
    """Create a struct value from field values"""
    struct_val = ir.Constant(struct_type, ir.Undefined)
    for i, field_val in enumerate(field_values):
        struct_val = builder.insert_value(
            struct_val, field_val, i, name
        )
    
    return struct_val

def get_allocated_struct_field(builder: ir.IRBuilder, struct: ir.Value, field_index: int, name: str = ''):
    """Get pointer to a struct field (struct must be allocated)"""
    return builder.gep(struct, [zero(32), llint(field_index)], True, name)

def get_allocated_struct_field_value(
    builder: ir.IRBuilder, struct: ir.Value, field_index: int, name: str = ''
):
    """Get the value from a struct pointer's field (struct must be allocated)"""
    ptr = get_allocated_struct_field(builder, struct, field_index, f'{name}_ptr')
    return builder.load(ptr, name)

def get_struct_field(builder: ir.IRBuilder, struct: ir.Value, field_index: int, name: str = ''):
    """Extract a field value from a struct value"""
    return builder.extract_value(struct, field_index, name)

def set_allocated_struct_field(
    builder: ir.IRBuilder, struct: ir.Value, field_index: int, value: ir.Value, name: str = ''
):
    """Set a field in a struct (struct must be allocated)"""
    ptr = get_allocated_struct_field(builder, struct, field_index, name)
    builder.store(value, ptr)


def create_string_constant(
    module: ir.Module, text: str, name: str = '', builder: Optional[ir.IRBuilder] = None
):
    """Create a global string constant and return pointer to it"""
    if not text.endswith('\0'):
        text += '\0'
    
    const_type = ir.ArrayType(ir.IntType(8), len(text))
    if name == '' and builder is None:
        const = ir.GlobalVariable(
            module, const_type,
            module.get_unique_name('str')
        )
    else:
        const = ir.GlobalVariable(
            module, const_type,
            module.get_unique_name(name)
        )
    
    const.initializer = ir.Constant(const_type, bytearray(text.encode('utf-8')))
    const.global_constant = True
    const.linkage = 'internal'
    
    if builder is not None:
        return builder.gep(const, [zero(32), zero(32)], True, name)
    else:
        return ir.Constant.gep(const, [zero(32), zero(32)])


def create_static_buffer(
    module: ir.Module, element_type: ir.Type, size: int, name = '',
    builder: Optional[ir.IRBuilder] = None
):
    buf_type = ir.ArrayType(element_type, size)
    buf = ir.GlobalVariable(module, buf_type, module.get_unique_name('buf'))
    buf.initializer = ir.Constant(buf_type, None)
    buf.linkage = 'internal'

    if builder is None:
        return ir.Constant.gep(buf, [zero(32), zero(32)])
    else:
        return builder.gep(buf, [zero(32), zero(32)], True, name)

def create_while_loop(
    builder: ir.IRBuilder, condition_func: Callable[[ir.IRBuilder], ir.Value],
    body_func: Callable[[ir.IRBuilder], None]
):
    """Create a while loop"""
    
    function = builder.function
    
    # Create blocks
    condition_block = function.append_basic_block('while_condition')
    body_block = function.append_basic_block('while_body')
    exit_block = function.append_basic_block('while_exit')
    
    # Jump to condition block (only if current block isn't terminated)
    if not builder.block.is_terminated:
        builder.branch(condition_block)
    
    # Condition block
    builder.position_at_end(condition_block)
    condition = condition_func(builder)
    
    # Only add cbranch if the block isn't already terminated
    if not builder.block.is_terminated:
        builder.cbranch(condition, body_block, exit_block)
    
    # Body block
    builder.position_at_end(body_block)
    body_func(builder)
    
    # Loop back to condition (only if not terminated)
    if not builder.block.is_terminated:
        builder.branch(condition_block)
    
    # Exit block - position builder here for continuation
    builder.position_at_end(exit_block)

def create_for_loop(builder, start_val, end_val, step_val, loop_var_name, body_fn):
    """Create a for loop"""

    func = builder.function
    entry_block = builder.block

    loop_cond_block = func.append_basic_block(name=f"{loop_var_name}_cond")
    loop_body_block = func.append_basic_block(name=f"{loop_var_name}_body")
    loop_end_block = func.append_basic_block(name=f"{loop_var_name}_end")

    # Jump to condition block
    builder.branch(loop_cond_block)

    # Condition block
    builder.position_at_start(loop_cond_block)
    phi = builder.phi(start_val.type, name=loop_var_name)
    phi.add_incoming(start_val, entry_block)

    cond = builder.icmp_signed('<', phi, end_val, name=f"{loop_var_name}_cond")
    builder.cbranch(cond, loop_body_block, loop_end_block)

    # Body block
    builder.position_at_start(loop_body_block)
    body_fn(builder, phi)
    next_val = builder.add(phi, step_val, name=f"{loop_var_name}_next")
    builder.branch(loop_cond_block)
    phi.add_incoming(next_val, builder.block)

    # Continue at end block
    builder.position_at_start(loop_end_block)
