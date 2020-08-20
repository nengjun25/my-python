# Filename: output_v.py

import re
import collections


class VerilogWriter:
    copyright = '''
    /*******************************************************************************
    *  Copyright (C) Siflower 2020
    *  This software is property of Siflower
    *******************************************************************************/

    /*******************************************************************************
    *      GENERATED CONTENT ==>  D O   N O T    E D I T !
    ********************************************************************************
    *         - source file version 0.1
    *         - source file date Monday, July 24, 2020
    *******************************************************************************/



    /*******************************************************************************
    *  Copyright (C) Siflower 2020
    *  This software is property of Siflower
    ******************************************************************************/
    '''

    # special char
    back_quote = "`"
    space = " "
    tab = "    "
    slash = '''/'''
    enter = "\n"
    comma = ","
    dot = "."

    # separate
    colon = ":"
    semicolon = ";"

    # operator
    evaluation = "="
    equal = "=="
    bit_op_or = "|"
    question = "?"
    bit_op_and = "&"

    # braces
    braces = "{"
    back_braces = "}"
    brackets = "["
    back_brackets = "]"
    p_thesis = "("
    back_p_thesis = ")"

    # keywords
    reg = "reg"
    wire = "wire"
    input = "input"
    output = "output"
    begin = "begin"
    end = "end"
    always = "always"
    case = "case"
    end_case = "endcase"
    module = "module"
    assign = "assign"
    end_module = "endmodule"

    # macro commands
    include = "include"
    define = "define"
    if_def = "ifdef"
    endif = "endif"
    if_ndef = "ifndef"

    def __init__(self, file):
        self.file = file
        self.res = ""
        self.indent_manager = IndentManager()

    def write(self, content):
        self.file.write(content)
        # self.res += content

    def write_expression(self, content):
        if content is not None:
            self.file.write(content+self.get_enter())

    def write_enter(self):
        s = self.enter+self.indent_manager.write()
        self.write(s)
        return s

    def get_enter(self):
        s = self.enter+self.indent_manager.write()
        return s

    def write_copyright(self):
        s = self.copyright+self.get_enter()
        self.write(s)
        return s

    def macro_define(self, command, desc):
        s = self.back_quote + command + self.space*2 + desc+self.indent_manager.write()
        self.write(s)
        return s

    def invoke_macro(self, name):
        self.write(self.get_invoke_macro(name))

    @staticmethod
    def get_invoke_macro(name):
        return VerilogWriter.back_quote + name

    def write_annotation(self, slash_count, desc, space_count):
        self.write(self.get_annotation(slash_count, desc, space_count))

    def get_annotation(self, slash_count, desc, space_count):
        e_list = [self.enter, self.space * space_count]
        for i in range(0, slash_count):
            e_list.append(self.slash)
        e_list.append(desc)
        e_list.append(self.get_enter())
        s = "".join(e_list)
        return s

    def define_module(self, module_name, args):
        e_list = [self.module, self.space, module_name, self.space, self.p_thesis, self.enter]
        self.indent_manager.add_indent(4)
        e_list.append(self.indent_manager.write())
        le = len(args)
        annotation = None
        macro = None
        for i in range(0, le):
            if args[i].annotation is not None and args[i].annotation != annotation:
                e_list.append(self.get_annotation(2, args[i].annotation, 4))
                e_list.append(self.get_enter())
                annotation = args[i].annotation
            if args[i].macro is not None and macro is None:
                e_list.append(self.get_invoke_macro(args[i].macro))
                e_list.append(self.get_enter())
                macro = args[i].macro
            elif args[i].macro is not None and macro is not None and args[i].macro != macro:
                e_list.append(self.get_invoke_macro(self.endif))
                e_list.append(self.get_enter())
                e_list.append(self.get_invoke_macro(args[i].macro))
                macro = args[i].macro

            var_len = len(args[i].name)
            if isinstance(args[i], VectorVar):
                e_list.append(args[i].define_vector_var())
            elif isinstance(args[i], Variable):
                e_list.append(args[i].define_var())
            if i != le - 1:
                e_list.append(self.space * (24 - var_len))
                e_list.append(self.comma)
            e_list.append(self.get_enter())
            if (i == le - 1 or args[i+1].macro is None) and macro is not None:
                e_list.append(self.get_invoke_macro(self.endif))
                e_list.append(self.get_enter())
                macro = None

        self.indent_manager.pop_indent()
        e_list.append(self.get_enter())
        e_list.append(self.back_p_thesis)
        e_list.append(self.semicolon)
        self.indent_manager.add_indent(4)
        e_list.append(self.get_enter())
        s = "".join(e_list)
        self.write(s)
        return s

    def define_var_list(self, args, split):
        e_list = []
        le = len(args)
        annotation = None
        macro = None
        for i in range(0, le):
            if args[i].annotation is not None and args[i].annotation != annotation:
                e_list.append(self.get_annotation(2, args[i].annotation, 4))
                e_list.append(self.get_enter())
                annotation = args[i].annotation
            if args[i].macro is not None and macro is None:
                e_list.append(self.get_invoke_macro(args[i].macro))
                e_list.append(self.get_enter())
                macro = args[i].macro
            elif args[i].macro is not None and macro is not None and args[i].macro != macro:
                e_list.append(self.get_invoke_macro(self.endif))
                e_list.append(self.get_enter())
                e_list.append(self.get_invoke_macro(args[i].macro))
                macro = args[i].macro

            var_len = len(args[i].name)
            if isinstance(args[i], VectorVar):
                e_list.append(args[i].define_vector_var())
            elif isinstance(args[i], Variable):
                e_list.append(args[i].define_var())
            e_list.append(self.space * (24 - var_len))
            e_list.append(split)
            e_list.append(self.get_enter())
            if (i == le - 1 or args[i + 1].macro is None) and macro is not None:
                e_list.append(self.get_invoke_macro(self.endif))
                e_list.append(self.get_enter())
                macro = None
        s = "".join(e_list)
        self.write(s)
        return s

    def invoke_module(self, module):
        self.write(module.name+self.space+module.instance_name+self.p_thesis)
        self.indent_manager.add_indent(4)
        self.write_enter()
        for arg in module.arg_vals:
            self.write(self.dot+arg+self.space*2+self.p_thesis+module.arg_vals[arg]+self.back_p_thesis+self.comma)
            self.write_enter()
        self.indent_manager.pop_indent()
        self.write_enter()
        self.write(self.back_p_thesis+self.semicolon)
        self.write_enter()

    def write_case(self, item):
        s = self.case + self.space + self.p_thesis + item + self.back_p_thesis+self.space*2
        self.indent_manager.add_indent(4)
        self.write(s)
        return s

    def case_item(self, value):
        s = value + self.space * 3 + self.colon
        self.indent_manager.add_indent(4)
        self.write(s)
        return s

    def enter_space(self):
        s = self.enter + self.space * 4
        self.write(s)
        return s

    def write_always(self, desc):
        self.indent_manager.add_indent(4)
        s = self.always + self.space * 2 + desc
        self.write(s)
        return s

    def write_begin(self):
        s = self.begin+self.get_enter()
        self.write(s)
        return s

    def write_end(self):
        self.indent_manager.pop_indent()
        self.write_enter()
        s = self.end+self.get_enter()
        self.write(s)
        return s

    def write_end_case(self):
        self.indent_manager.pop_indent()
        self.write_enter()
        s = self.end_case+self.get_enter()
        self.write(s)
        return s

    def write_end_module(self):
        self.indent_manager.pop_indent()
        self.write_enter()
        s = self.end_module+self.get_enter()
        self.write(s)
        return s

    @staticmethod
    def create_num(length, system, count):
        if system == 2:
            return str(length) + "'" + "b" + str(count)
        elif system == 10:
            return str(length) + "'" + "d" + str(count)
        elif system == 16:
            return str(length) + "'" + "h" + str(count)

    @staticmethod
    def create_vector(args):
        e_list = [VerilogWriter.braces]
        for i in range(0, len(args)):
            e_list.append(args[i])
            if i != len(args) - 1:
                e_list.append(VerilogWriter.space*2+VerilogWriter.comma)
        e_list.append(VerilogWriter.back_braces)
        return "".join(e_list)

    @staticmethod
    def ternary_expression(condition, val1, val2):
        return condition + VerilogWriter.space + VerilogWriter.question + \
               VerilogWriter.space + val1 + VerilogWriter.space * 4 + \
               VerilogWriter.colon + VerilogWriter.space * 4 + val2

    def get_assign_expression(self, left, right):
        if left is not None and right is not None:
            e_list = [self.assign, self.space * 2, left, self.space * 8,
                    self.evaluation, self.space * 3, right,
                    self.semicolon]
            return "".join(e_list)

    @staticmethod
    def and_expression(left, right):
        return left + VerilogWriter.space + VerilogWriter.bit_op_and + VerilogWriter.space + right

    @staticmethod
    def or_expression(left, right):
        return left + VerilogWriter.space + VerilogWriter.bit_op_or + VerilogWriter.space + right

    @staticmethod
    def p_thesis_expression(expression):
        return VerilogWriter.p_thesis + expression + VerilogWriter.back_p_thesis

    @staticmethod
    def equal_expression(left, right):
        return left + VerilogWriter.space + VerilogWriter.equal + VerilogWriter.space + right


class Module:
    def __init__(self, name, args):
        self.args = args
        self.name = name
        self.instance_name = None
        self.arg_vals = {}
        for arg in args:
            self.arg_vals[arg] = None

    def instance(self, instance_name, arg_values):
        self.instance_name = instance_name
        for arg in self.args:
            if arg in arg_values:
                self.arg_vals[arg] = arg_values[arg]


class Variable:
    default_space_type_name = 16

    def __init__(self, name, vtype):
        self.name = name
        self.inout = None
        self.vtype = vtype
        self.annotation = None
        self.value = None
        self.macro = None
        self.prefix = None

    def set_prefix(self, prefix):
        self.prefix = prefix

    def set_annotation(self, annotation):
        self.annotation = annotation

    def set_macro(self, macro):
        self.macro = macro

    def set_inout(self, inout):
        self.inout = inout

    def set_value(self, value):
        self.value = value

    def define_var(self):
        e_list = []
        if self.inout is not None:
            e_list.append(self.inout + VerilogWriter.space*2)
        if self.vtype is not None:
            e_list.append(self.vtype)
        e_list.append(VerilogWriter.space * 16)
        e_list.append(self.name)
        return "".join(e_list)

    def set_var_value(self):
        if self.value is None:
            return None
        count = 28 - len(self.name)
        e_list = [self.name, VerilogWriter.space * count, VerilogWriter.evaluation, VerilogWriter.space * 3, self.value,
                  VerilogWriter.semicolon]
        return "".join(e_list)

    def assign_var_value(self):
        if self.value is None:
            return None
        count = 28 - len(self.name)
        e_list = [VerilogWriter.assign, VerilogWriter.space * 2, self.name, VerilogWriter.space * count,
                  VerilogWriter.evaluation, VerilogWriter.space * 3, self.value, VerilogWriter.semicolon]
        return "".join(e_list)


class VectorVar(Variable):
    default_space_type_vector = 4

    def __init__(self, name, vtype, high, low):
        Variable.__init__(self, name, vtype)
        self.high = high
        self.low = low
        self.xls_name = None

    def set_xls_name(self, xls_name):
        self.xls_name = xls_name

    def write_vector(self):
        return VerilogWriter.brackets + "%s:%s" % (self.high, self.low) + VerilogWriter.back_brackets

    def define_vector_var(self):
        vector = self.write_vector()
        count = 16 - 4 - len(vector)
        if count <= 0:
            count = 4
        e_list = collections.deque([self.vtype, VerilogWriter.space * 4,
                                    vector, VerilogWriter.space * count, self.name])
        if self.inout is not None:
            e_list.appendleft(self.inout + VerilogWriter.space*2)

        return "".join(e_list)

    def invoke_vector_var(self, index):
        # if (index < self.low or index > self.high):
        #     return
        if index is not None:
            return self.name + VerilogWriter.brackets + str(index) + VerilogWriter.back_brackets

    def assign_var_value(self, *args):
        if self.value is None:
            return ""
        if len(args) == 0:
            return Variable.assign_var_value(self)
        index = args[0]
        v = self.invoke_vector_var(index)
        count = 28 - len(v)
        e_list = [VerilogWriter.assign, VerilogWriter.space * 2, v, VerilogWriter.space * count,
                  VerilogWriter.evaluation, VerilogWriter.space * 3, self.value, VerilogWriter.semicolon]

        return "".join(e_list)

    @staticmethod
    def is_vector(name):
        res = re.search('\[.*\]$', name)
        return res

    @staticmethod
    def get_vector_name(name):
        res = re.search('\[.*\]$', name)
        if res is None:
            return None,None
        v_name = name[:res.span()[0]]
        index = name[res.span()[0] + 1:res.span()[1] - 1]
        return v_name, index


    @staticmethod
    def invoke_vector(name, index):
        # if (index < self.low or index > self.high):
        #     return
        if index is not None:
            return name + VerilogWriter.brackets + str(index) + VerilogWriter.back_brackets


class IndentManager:
    def __init__(self):
        self.indent = []
        self.total = 0

    def add_indent(self, space_count):
        self.indent.append(space_count)
        self.total += space_count

    def pop_indent(self):
        if self.total == 0:
            return
        val = self.indent.pop()
        self.total -= val
        return val

    def write(self):
        return VerilogWriter.space*self.total
