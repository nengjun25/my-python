from output_v import VerilogWriter
from output_v import Variable
import cpads_dft_mux
from output_v import VectorVar
from output_v import Module
import collections
import functools
from xls_reader import XlsReader
import sys


# var list:
# # input output:
# # # var[fmux,fi,foen,fc] input : xc,fi,foen    differ:clk32k
# # # vector[sw,func_sw,egpio _reg,CATIP_DEBUG_IO] output: fc_egpio
#
#
#
# # local:
# # var [hw_fmux] XOEN XI
# # vector [UCN]

# module instance:
# cpads_io_out_mux (XOEN,XI)(
#   xi({a,b,c,d})
#   sel({a,b})
#   xout(a)
# )
#
#
# cpads_io_in_mux (XC)(
#   xi(a)
#   sel(a,b)
#   xout({a,b,c,d})
# )
# end



pad_args = []
xtal_args = ["DS0", "DS1", "DS2", "XE"]
f_args = ["i", "c"]
hw_fmux_args = ["OEN", "I"]
global f_interval

func_columns = []
mux_func_value = []
module_func_value = []

fmux_vars = []
f_vars = []
xtal_vars = []
clock_vars = []
vector_vars = []
hw_vars = []
ucn_vars = []

rsap_external_ap = 'RSAP_EXTERNAL_PA_ENABLE'
rsap_dio_num = 'RSAP_DIO_NUM'
rsap_am29_num = 'RSAP_AM29_IIN_NUM'

dio_num_vector = ["mode_bit0_reg", "mode_bit1_reg", "sw_ds0_reg", "sw_ds1_reg",
                  "sw_ds2_reg", "sw_pu_reg", "sw_pd_reg", "sw_ie_reg", "sw_st_reg",
                  "func_sw_sel_reg", "sw_oen_reg", "fmux_sel_reg"]

am29_vector = ["fi_EGPIO", "foen_EGPIO", "fc_EGPIO"]

ucn_vector = ["UCN0", "UCN1", "UCN2", "UCN3"]

clock_vector = [
    {"sw_xtal_reg": 4},
    {"sw_tmode_reg": 8},
    {"sw_nreset_reg": 8},
    {"sw_clk32k_reg": 8}
]

io_out_args = ["xi", "sel", "xout"]
io_in_args = ["xi", "sel", "xout"]

io_out_oen = []
io_out_xi = []
io_in_xc = []

file_dir = "SF19A28C_IO_Mux.xlsx"
sheet_name = "IO MUX"

if len(sys.argv) == 2:
    file_dir = sys.argv[1]

if len(sys.argv) == 3:
    sheet_name = sys.argv[2]

xls_reader = XlsReader(file_dir, sheet_name)
max_row = xls_reader.sheet.max_row
max_column = xls_reader.sheet.max_column


def read_pad_args():
    for j in range(27, 35):
        value = xls_reader.get_cell_value(row=2, column=j)
        if value is not None and value != "CODE":
            if value.startswith("DS"):
                pad_args.append("DS0")
                pad_args.append("DS1")
                pad_args.append("DS2")
            else:
                if value.startswith("X"):
                    value = value[1:]
                pad_args.append(value)


def read_f_args():
    interval = 0
    for i in range(1, max_column):
        value = xls_reader.get_cell_value(row=2, column=i)
        if value is not None and "func_name" in value:
            if interval != 0:
                j = i + 1
                while j < max_column - i:
                    v1 = xls_reader.get_cell_value(row=2, column=j)
                    if v1 is not None and "func_name" in v1:
                        interval = j - i
                        break
                    else:
                        v2 = xls_reader.get_cell_value(row=2, column=j)
                        if v2 is not None and v2 in pad_args:
                            f_args.append(v2.lower())
                    j = j + 1
            func_columns.append(i)
    global f_interval
    f_interval = interval

    for k in range(3, 55):
        v = xls_reader.get_cell_value(row=k, column=func_columns[0])
        le = len(func_columns)
        for m in range(1, le):
            if xls_reader.get_cell_value(row=k, column=func_columns[m]) != v:
                module_func_value.append(k)
                break
            if m == le-1:
                mux_func_value.append(k)


def create_fmux_vars(m_vars):
    interface_name = None
    for i in range(0, len(pad_args)):
        for j in range(3, 55):
            interface_value = xls_reader.get_cell_value(row=j, column=2)
            if j > 51:
                interface_name = "CLOCK"
            elif interface_value is not None:
                interface_name = interface_value
            cv = xls_reader.get_cell_value(row=j, column=4)
            if cv is not None:
                prefix = "fmux_X"
                name = prefix + pad_args[i] + "_" + cv
                var = Variable(name, VerilogWriter.wire)
                if pad_args[i] == "C":
                    var.set_inout(VerilogWriter.input)
                else:
                    var.set_inout(VerilogWriter.output)
                if interface_name is not None:
                    var.set_annotation(interface_name)
                if interface_name == "RF GPIO":
                    var.set_macro("ifdef  " + rsap_external_ap)
                m_vars.append(var)


def create_xtal_var(xtalvars):
    for i in range(0, len(xtal_args)):
        prefix = "fmux_X"
        name = prefix + xtal_args[i] + "_XTAL_XIO"
        var = Variable(name, VerilogWriter.wire)
        var.set_inout(VerilogWriter.output)
        var.set_annotation("CLOCK")
        xtalvars.append(var)


def create_f_vars(m_vars):
    interface_name = None
    var_len = 0
    fl = len(f_args)
    for i in range(19, 27, 2):
        vars_index = {}
        for j in range(3, 55):
            interface_value = xls_reader.get_cell_value(row=j, column=2)
            if j > 51:
                interface_name = "CLOCK"
            elif interface_value is not None:
                interface_name = interface_value

            value = xls_reader.get_cell_value(row=j, column=i)
            if value is not None and value != "NC":
                if "/" in value:
                    value = value[0:value.index("/")]
                if "RGMII0" in value:
                    value = value.replace("RGMII0", "RGMII")
                v_name, count = VectorVar.get_vector_name(value)
                if v_name is not None:
                    if v_name not in vars_index:
                        # create vector var
                        for k in range(0, fl):
                            prefix = "f" + f_args[k] + "_"
                            name = prefix + v_name
                            var = VectorVar(name, VerilogWriter.wire, count, 0)
                            if f_args[k] == "c":
                                var.set_inout(VerilogWriter.output)
                            else:
                                var.set_inout(VerilogWriter.input)
                            if interface_name is not None:
                                var.set_annotation(interface_name)
                            if interface_name == "RF GPIO":
                                var.set_macro("ifdef  " + rsap_external_ap)
                            m_vars.append(var)
                        var_len = var_len + fl
                        vars_index[v_name] = var_len - 1
                    else:
                        # update vector high
                        index = vars_index[v_name]
                        if int(count) > int(m_vars[index].high):
                            for m in range(index - fl+1, index+1):
                                m_vars[m].high = count
                else:
                    if value not in vars_index:
                        # create var
                        for k in range(0, fl):
                            prefix = "f" + f_args[k] + "_"
                            name = prefix + value
                            var = Variable(name, VerilogWriter.wire)
                            if f_args[k] == "c":
                                var.set_inout(VerilogWriter.output)
                            else:
                                var.set_inout(VerilogWriter.input)
                            if interface_name is not None:
                                var.set_annotation(interface_name)
                            if interface_name == "RF GPIO":
                                var.set_macro("ifdef  " + rsap_external_ap)
                            m_vars.append(var)
                        var_len = var_len + fl
                        vars_index[value] = var_len - 1


def create_clock_var(vectors):
    for i in range(0, len(clock_vector)):
        for k, v in clock_vector[i].items():
            vector = VectorVar(k, VerilogWriter.wire, str(v - 1), "0")
            vector.set_inout(VerilogWriter.input)
            vector.set_annotation("CLOCK")
            vectors.append(vector)


def create_vector_var(vectors):
    for name in dio_num_vector:
        vector = VectorVar(name, VerilogWriter.wire, VerilogWriter.get_invoke_macro(rsap_dio_num) + "-1", "0")
        vector.set_inout(VerilogWriter.input)
        vectors.append(vector)

    for am in am29_vector:
        inout = VerilogWriter.input
        if am.startswith("fc"):
            inout = VerilogWriter.output
        vector = VectorVar(am, VerilogWriter.wire, VerilogWriter.get_invoke_macro(rsap_am29_num) + "-1", "0")
        vector.set_inout(inout)
        vectors.append(vector)


# todo code differ with excel CLK32K
def assign_clock(verilog_writer):
    for i in range(0, len(xtal_vars)):
        if "XTAL_XIO" in xtal_vars[i].name:
            for j in range(0, len(clock_vars)):
                if "xtal" in clock_vars[j].name:
                    bit = get_testmode_nreset_bit(xtal_vars[i].name)
                    if type(bit) == int:
                        invoke = clock_vars[j].invoke_vector_var(bit)
                        exp = v_writer.get_assign_expression(xtal_vars[i].name, invoke)
                        verilog_writer.write_expression(exp)
                    else:
                        exp = v_writer.get_assign_expression(xtal_vars[i].name, bit)
                        verilog_writer.write_expression(exp)

    for i in range(0, len(fmux_vars)):
        if "TEST_MODE" in fmux_vars[i].name:
            for j in range(0, len(clock_vars)):
                if "tmode" in clock_vars[j].name:
                    bit = get_testmode_nreset_bit(fmux_vars[i].name)
                    if type(bit) == int:
                        invoke = clock_vars[j].invoke_vector_var(bit)
                        exp = v_writer.get_assign_expression(fmux_vars[i].name, invoke)
                        verilog_writer.write_expression(exp)
                    else:
                        exp = v_writer.get_assign_expression(fmux_vars[i].name, bit)
                        verilog_writer.write_expression(exp)

        elif "NRESET" in fmux_vars[i].name:
            for j in range(0, len(clock_vars)):
                if "nreset" in clock_vars[j].name:
                    bit = get_testmode_nreset_bit(fmux_vars[i].name)
                    if type(bit) == int:
                        invoke = clock_vars[j].invoke_vector_var(bit)
                        exp = v_writer.get_assign_expression(fmux_vars[i].name, invoke)
                        verilog_writer.write_expression(exp)
                    else:
                        exp = v_writer.get_assign_expression(fmux_vars[i].name, bit)
                        verilog_writer.write_expression(exp)
        elif "CLK32K" in fmux_vars[i].name:
            for j in range(0, len(clock_vars)):
                if "clk32k" in clock_vars[j].name:
                    bit = get_testmode_nreset_bit(fmux_vars[i].name)
                    if type(bit) == int:
                        invoke = clock_vars[j].invoke_vector_var(bit)
                        exp = v_writer.get_assign_expression(fmux_vars[i].name, invoke)
                        verilog_writer.write_expression(exp)
                    else:
                        exp = v_writer.get_assign_expression(fmux_vars[i].name, bit)
                        verilog_writer.write_expression(exp)


def create_hw_vars(m_vars):
    interface_name = None
    for i in range(0, len(hw_fmux_args)):
        for j in range(5, 55):
            interface_value = xls_reader.get_cell_value(row=j, column=2)
            if j == 52 or j == 53 or j == 5:
                interface_name = "CLOCK"
            elif interface_value is not None:
                interface_name = interface_value
            value = xls_reader.get_cell_value(row=j, column=4)
            if value is not None:
                prefix = "hw_fmux_X"
                name = prefix + hw_fmux_args[i] + "_" + value
                var = Variable(name, VerilogWriter.wire)
                if interface_name is not None:
                    var.set_annotation("X" + hw_fmux_args[i] + " " + interface_name)
                if interface_name == "RF GPIO":
                    var.set_macro("ifdef  " + rsap_external_ap)
                m_vars.append(var)


def define_hw_vars(writer):
    writer.define_var_list(hw_vars, VerilogWriter.semicolon)


def assign_oen_i(writer):
    t = 0
    k = 0
    for i in range(0, len(hw_vars)):
        if "XOEN" in hw_vars[i].name:
            t = 1
            index = hw_vars[i].name.index("XOEN")
            p = hw_vars[i].name[index:]
            for j in range(0, len(fmux_vars)):
                if p in fmux_vars[j].name:
                    left = fmux_vars[j].name
                    c1 = VectorVar.invoke_vector("func_sw_sel_reg", i)
                    c2 = VerilogWriter.p_thesis_expression(VerilogWriter.equal_expression(
                        VectorVar.invoke_vector("fmux_sel_reg", i), VerilogWriter.create_num(1, 2, 1)))
                    t2 = VectorVar.invoke_vector("foen_EGPIO", i)
                    f2 = hw_vars[i].name
                    t1 = VerilogWriter.p_thesis_expression(VerilogWriter.ternary_expression(c2, t2, f2))
                    f1 = VectorVar.invoke_vector("sw_oen_reg", i)
                    right = VerilogWriter.ternary_expression(c1, t1, f1)
                    writer.write_expression(writer.get_assign_expression(left, right))
        elif "XI" in hw_vars[i].name:
            if t == 1:
                v_writer.write_enter()
                t = 2

            index = hw_vars[i].name.index("XI")
            p = hw_vars[i].name[index:]
            for j in range(0, len(fmux_vars)):
                if p in fmux_vars[j].name:
                    left = fmux_vars[j].name
                    c = VerilogWriter.p_thesis_expression(VerilogWriter.equal_expression(
                        VectorVar.invoke_vector("fmux_sel_reg", k), VerilogWriter.create_num(1, 2, 1)))
                    t = VectorVar.invoke_vector("fi_EGPIO", k)
                    f = hw_vars[i].name
                    right = VerilogWriter.ternary_expression(c, t, f)
                    writer.write_expression(writer.get_assign_expression(left, right))
                    k = k + 1


def assign_fmux_other(writer):
    for i in range(0, len(dio_num_vector)):
        if dio_num_vector[i].startswith("sw") and dio_num_vector[i].endswith("reg") and "oen" not in dio_num_vector[i]:
            s = dio_num_vector[i].split("_")
            su = s[1].upper()
            writer.write_enter()
            k = 0
            for j in range(0, len(fmux_vars)):
                if su in fmux_vars[j].name and "SYS" not in fmux_vars[j].annotation:
                    left = fmux_vars[j].name
                    right = VectorVar.invoke_vector(dio_num_vector[i], k)
                    writer.write_expression(writer.get_assign_expression(left, right))
                    k = k + 1
            ref_clk_sel = "fmux_X" + su + "_REF_CLK_SEL"
            writer.write_expression(writer.get_assign_expression(ref_clk_sel, VectorVar.invoke_vector(dio_num_vector[i],
                                                                                                      k)))


def create_io_out_module(oen_modules, xi_modules):
    k = 0
    for i in range(6, 55):
        module_oen = Module("cpads_io_out_mux", io_out_args)
        module_xi = Module("cpads_io_out_mux", io_out_args)
        value1 = xls_reader.get_cell_value(row=i, column=4)
        if value1 is None:
            continue
        bit_htl_oen = collections.deque()
        bit_htl_xi = collections.deque()
        for j in range(19, max_column):
            func_name = xls_reader.get_cell_value(row=2, column=j)
            if func_name is not None and "func_name" in func_name:
                value2 = xls_reader.get_cell_value(row=i, column=j)
                if value2 is not None and value2 != "NC":
                    if "/" in value2:
                        value2 = value2[0:value2.index("/")]
                    # todo code differ with xls
                    if "RGMII0" in value2:
                        value2 = value2.replace("RGMII0", "RGMII")
                    bit_htl_oen.appendleft("foen_" + value2)
                    bit_htl_xi.appendleft("fi_" + value2)
                else:
                    bit_htl_oen.appendleft("1'b1")
                    bit_htl_xi.appendleft("1'b1")
        sels = [
            VectorVar.invoke_vector("mode_bit1_reg", k),
            VectorVar.invoke_vector("mode_bit0_reg", k)
        ]
        arg_vals_oen = {
            "xi": VerilogWriter.create_vector(bit_htl_oen),
            "sel": VerilogWriter.create_vector(sels),
            "xout": "hw_fmux_XOEN_" + value1
        }
        module_oen.instance("u_fmux_XOEN_" + value1, arg_vals_oen)
        oen_modules.append(module_oen)
        arg_vals_oen = {
            "xi": VerilogWriter.create_vector(bit_htl_xi),
            "sel": VerilogWriter.create_vector(sels),
            "xout": "hw_fmux_XI_" + value1
        }
        module_xi.instance("u_fmux_XOEN_" + value1, arg_vals_oen)
        xi_modules.append(module_xi)
        k = k + 1


def create_io_in_module(xc_modules):
    k = 0
    for i in range(6, 55):
        module_xc = Module("cpads_io_in_mux", io_out_args)
        value1 = xls_reader.get_cell_value(row=i, column=4)
        if value1 is None:
            continue
        bit_htl_xc = collections.deque()
        m = 0
        for j in range(19, max_column):
            func_name = xls_reader.get_cell_value(row=2, column=j)
            if func_name is not None and "func_name" in func_name:
                value2 = xls_reader.get_cell_value(row=i, column=j)
                if value2 is not None and value2 != "NC":
                    if "/" in value2:
                        value2 = value2[0:value2.index("/")]
                    if "RGMII0" in value2:
                        value2 = value2.replace("RGMII0", "RGMII")
                    bit_htl_xc.appendleft("fc_" + value2)
                    m = m+1
                else:
                    bit_htl_xc.appendleft(VectorVar.invoke_vector(ucn_vector[m], k))
                    m = m + 1

        sels = [
            VectorVar.invoke_vector("mode_bit1_reg", k),
            VectorVar.invoke_vector("mode_bit0_reg", k)
        ]
        arg_vals_xc = {
            "xi": "hw_fmux_XC_" + value1,
            "sel": VerilogWriter.create_vector(sels),
            "xout": VerilogWriter.create_vector(bit_htl_xc)
        }
        module_xc.instance("u_fmux_XC_" + value1, arg_vals_xc)
        xc_modules.append(module_xc)
        k = k + 1


def define_ucn_vector(ucns, writer):
    for i in range(0, len(ucn_vector)):
        vector = VectorVar(ucn_vector[i], VerilogWriter.wire, VerilogWriter.get_invoke_macro(rsap_dio_num) + "-1", "0")
        ucns.append(vector)
    writer.define_var_list(ucns, VerilogWriter.semicolon)


def assign_egpio(writer):
    k = 0
    for i in range(6, 55):
        value = xls_reader.get_cell_value(row=i, column=4)
        if value is not None:
            right = "fmux_XC_"+value
            left = VectorVar.invoke_vector("fc_EGPIO", k)
            writer.write_expression(writer.get_assign_expression(left, right))
            k = k + 1
    ref_clk_sel = "fmux_XC_REF_CLK_SEL"
    writer.write_expression(writer.get_assign_expression(VectorVar.invoke_vector("fc_EGPIO", k), ref_clk_sel))


def write_invoke_module(modules, writer):
    for i in modules:
        writer.invoke_module(i)


def get_testmode_nreset_bit(name):
    if "DS0" in name:
        return 0
    elif "DS1" in name:
        return 1
    elif "DS2" in name:
        return 2
    elif "XIE" in name:
        return "1'b1"
    elif "XOEN" in name:
        return "1'b1"
    elif "XPU" in name:
        return 5
    elif "XPD" in name:
        return 6
    elif "XST" in name:
        return 7
    elif "XE" in name:
        return 3


def sort_f_arg_rfgpio_first(var1, var2):
    if var1.macro == "ifdef  RSAP_EXTERNAL_PA_ENABLE" and var2.macro != "ifdef  RSAP_EXTERNAL_PA_ENABLE":
        return -1
    elif var1.macro != "ifdef  RSAP_EXTERNAL_PA_ENABLE" and var2.macro == "ifdef  RSAP_EXTERNAL_PA_ENABLE":
        return 1
    else:
        return sort_by_f_args(var1, var2)


def move_key_to_vars_end(m_vars, key):
    p = None
    le = len(m_vars)
    pos = le
    for i in range(0, le):
        if key in m_vars[i].name:
            p = m_vars[i]
            pos = i
        else:
            if i != 0 and i > pos:
                m_vars[i-1] = m_vars[i]
            if p is not None:
                index = p.name.index(key)
                if i == le-1 or m_vars[i+1].name.startswith(p.name[:index]) is False:
                    m_vars[i] = p
                    p = None
                    pos = le


def sort_by_f_args(var1, var2):
    f1 = None
    f2 = None
    for f_arg in f_args:
        if var1.name.startswith("f" + f_arg):
            f1 = f_arg
        if var2.name.startswith("f" + f_arg):
            f2 = f_arg
    if f1 > f2:
        return 1
    elif f1 < f2:
        return -1
    else:
        return 0


read_pad_args()
read_f_args()
print(f_interval)
print(func_columns)
print(module_func_value)
print(mux_func_value)
create_xtal_var(xtal_vars)
create_fmux_vars(fmux_vars)
create_f_vars(f_vars)
create_clock_var(clock_vars)
create_vector_var(vector_vars)
create_hw_vars(hw_vars)
f_vars.sort(key=functools.cmp_to_key(sort_f_arg_rfgpio_first))
fmux_vars.sort(key=functools.cmp_to_key(cpads_dft_mux.var_sort_by_pin))
# move refcklsel to end
move_key_to_vars_end(hw_vars, "REF_CLK_SEL")

# start to write file
res = open("result.v", mode='w')
v_writer = VerilogWriter(res)
v_writer.write_copyright()
v_writer.macro_define("include", "\"rsap_bm_param.v\"")
v_writer.write_enter()

# define module
v_writer.define_module("cpads_dft_mux", fmux_vars + xtal_vars + f_vars + clock_vars + vector_vars)

v_writer.write_enter()
assign_clock(v_writer)
v_writer.write_enter()

define_hw_vars(v_writer)
v_writer.write_enter()

# lots of assign for fmux
# oen :
# func_sw_sel_reg? (fmux_sel_reg=1?foen_egpio:hw_fmux_oen):sw_oen_reg
#

# xi :
# fmux_sel_reg=1?fi_egpio:hw_fmux_xi
#

assign_oen_i(v_writer)

# ds012,pu,pd
# sw_*_reg
#
assign_fmux_other(v_writer)
v_writer.write_enter()

# todo module instance

create_io_out_module(io_out_oen, io_out_xi)
write_invoke_module(io_out_oen, v_writer)
v_writer.write_enter()
write_invoke_module(io_out_xi, v_writer)
v_writer.write_enter()
define_ucn_vector(ucn_vars, v_writer)
v_writer.write_enter()
create_io_in_module(io_in_xc)
write_invoke_module(io_in_xc, v_writer)
v_writer.write_enter()

# assign fc_REF_CLK_SEL
v_writer.write_expression(v_writer.get_assign_expression("fc_REF_CLK_SEL", "fmux_XC_REF_CLK_SEL"))
v_writer.write_enter()

# assign egpio
assign_egpio(v_writer)

v_writer.write_end_module()

res.close()
