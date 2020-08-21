
# Filename: output_c.py

from output_v import IndentManager
from output_v import VerilogWriter

copy_right = '''
/*******************************************************************************
*  Copyright (C) Catena 2020
*  This software is property of Catena
*******************************************************************************/

/*******************************************************************************
*      GENERATED CONTENT ==>  D O   N O T    E D I T !
********************************************************************************
*         - source file version 0.3
*         - source file date Monday, October 28, 2019
*******************************************************************************/



/*******************************************************************************
*  Copyright (C) Catena 2018
*  This software is property of Catena
******************************************************************************/
/**
* @file trx_xdma.c
* @brief
*  provides the functions for DMA variable manipulation
*
* Detailed description
*
******************************************************************************/
'''

tab = "    "
braces = "{"
back_braces = "}"
brackets = "["
back_brackets = "]"
ptheses = "("
back_ptheses = ")"
enter = "\n"
tab_stack = []


def define_struct(struct_name, obj):
    #file = open("out.txt",mode=w)
    s = "struct "+struct_name+" "+braces+"\n"
    s += create_attr(obj)
    s += back_braces
    return s


def create_attr(obj):
    attrs = dir(obj)
    s = ""
    for i in range(0, len(attrs)):
        if(not attrs[i].startswith("__")):
            s += tab+"char "+"*"+attrs[i]+";\n"

    print(s)
    return s


def define_struct_variable(struct_name, var_name):
    s = "struct "+struct_name+" "+var_name+";\n"
    return s


def define_struct_point_variable(struct_name, var_name):
    s = "struct "+struct_name+" "+"*"+var_name+";\n"
    return s


def get_struct_attr(var_name, attr_name, point):
    s = None
    if(point):
        s = var_name+"->"+attr_name
    else:
        s = var_name+"."+attr_name
    return s


def var_assign(var_name, value):
    return var_name+" = "+value+";\n"


def call_func(func_name, func_args):
    s = func_name+ptheses
    le = len(func_args)

    for i in range(0, le):
        s += func_args[i]
        if(i != le - 1):
            s += ","

    s += back_ptheses
    return s


def define_func(func_name, ret_type, func_args, func_content):
    s = ret_type+" "+func_name+ptheses
    le = len(func_args)
    for i in range(0, le):
        s += func_args[i]
        if(i != le - 1):
            s += ","

    s += back_ptheses+braces+"\n"
    s += func_content+"\n"+back_braces+"\n"
    return s


def force_cast(var_type, point):
    s = ptheses+var_type
    if(point):
        s += " *"
    s += back_ptheses
    return s


def create_braces():
    s = braces+enter
    tab_stack.append(braces)
    return s


def back_braces():
    s = back_braces+enter
    tab_stack.pop()
    return s


def write_func_annotation(des,func_param,func_ret):
    s = '''/*******'''+enter+"*"
    s += des
    #todo


class CppWriter(VerilogWriter):

    void = "void"
    c_return = "return"

    def __init__(self, file):
        self.indent_manager = IndentManager()
        self.file = file
        self.res = ""

    def define_function(self, ret_type, func_name, args):
        s = ret_type+self.space+func_name+self.p_thesis+self.back_p_thesis+self.space+self.braces
        self.indent_manager.add_indent(4)
        self.write_expression(s)

    def end_function(self):
        self.indent_manager.pop_indent()
        self.write_enter()
        self.write(self.back_braces)

    def call_function(self, func_name, args):
        s = func_name+self.p_thesis+",".join(args)+self.back_p_thesis+self.semicolon
        self.write(s)

    def return_value(self,value):
        self.write(self.c_return+self.space+value+self.semicolon)