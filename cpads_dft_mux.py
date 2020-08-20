import pad
from output_v import VerilogWriter
from output_v import Variable
from output_v import VectorVar
import io_mux_other
import collections
import functools
import re
from xls_reader import XlsReader
import sys

default_values = {
    "XDS0": "1'b0",
    "XDS1": "1'b0",
    "XDS2": "1'b0",
    "XIE": "1'b1",
    "XOEN": "1'b1",
    "XPU": "1'b0",
    "XPD": "1'b1",
    "XST": "1'b0",
    "XI": "1'b0",
    "XXE": "1'b1"
}

unchanged_attrs = ["PD", "PU", "DS0", "DS1", "DS2", "ST"]

rsap_external_ap = '''RSAP_EXTERNAL_PA_ENABLE'''

special_pins = [
    {"name": "dmux_XDS0_XTAL_XIO", "annotation": "Clock", "value": "1'b0", "macro": None, "inout": "output"},
    {"name": "dmux_XDS1_XTAL_XIO", "annotation": "Clock", "value": "1'b0", "macro": None, "inout": "output"},
    {"name": "dmux_XDS2_XTAL_XIO", "annotation": "Clock", "value": "1'b0", "macro": None, "inout": "output"},
    {"name": "dmux_XXE_XTAL_XIO", "annotation": "Clock", "value": "1'b1", "macro": None, "inout": "output"},
]

test_mode_cfgs = []

file_dir = "SF19A28C_IO_Mux.xlsx"
sheet_name = "IO MUX"

if len(sys.argv) == 2:
    file_dir = sys.argv[1]

if len(sys.argv) == 3:
    sheet_name = sys.argv[2]


def create_test_mode(test_mode_list):
    for i in range(27, max_column):
        val = xls_reader.get_cell_value(row=1, column=i)
        if val is not None:
            test_mode = pad.TestMode(val.replace("\n", ""))
            test_mode_list.append(test_mode)

    return test_mode_list


def create_data(test_mode_list):
    interface_name = None
    for i in range(3, max_row):
        # skip anolog
        if i > 54:
            break
        interface_value = xls_reader.get_cell_value(row=i, column=2)
        if i > 51:
            interface_name = None
        elif interface_value is not None:
            interface_name = interface_value
        pad_name = xls_reader.get_cell_value(row=i, column=4)
        # index of every foot
        k = 0
        # index of test_mode
        m = 0
        m_pad = None
        for j in range(27, max_column):
            # skip
            title = xls_reader.get_cell_value(row=2, column=j)
            if title == "CODE" or title == "comments":
                continue
            cv = xls_reader.get_cell_value(row=i, column=j)

            if k == 0:
                m_pad = pad.Pad(interface=interface_name, name=pad_name)
                m_pad.XC = cv
            elif k == 1:
                m_pad.XI = cv
            elif k == 2:
                m_pad.IE = cv
            elif k == 3:
                m_pad.OEN = cv
            elif k == 4:
                m_pad.PU = cv
            elif k == 5:
                m_pad.PD = cv
            elif k == 6:
                m_pad.ST = cv
            elif k == 7:
                m_pad.DS0 = cv[0]
                m_pad.DS1 = cv[1]
                m_pad.DS2 = cv[2]
                k = -1
                test_mode_list[m].pad_list.append(m_pad)
                m = m + 1
            k = k + 1


def assign_vars_not_in_conditions(variables, conditions):
    v_writer.write_enter()
    for i in range(0, len(variables)):
        if variables[i].inout == "output" and \
                variables[i].name != "efuse_test_user_in":
            if variables[i].xls_name not in conditions:
                v_writer.write_expression(v_writer.get_assign_expression(variables[i].name, "0"))
            else:
                v_writer.write_expression(v_writer.get_annotation(4,
                                                                  v_writer.get_assign_expression(variables[i].name,
                                                                                                 "0"), 0))


def var_sort_rfgpio_first(var1, var2):
    if var1.macro == "ifdef  RSAP_EXTERNAL_PA_ENABLE" and var2.macro != "ifdef  RSAP_EXTERNAL_PA_ENABLE":
        return -1
    elif var1.macro != "ifdef  RSAP_EXTERNAL_PA_ENABLE" and var2.macro == "ifdef  RSAP_EXTERNAL_PA_ENABLE":
        return 1
    else:
        return var_sort_by_pin(var1, var2)


def var_sort_special_first(var1, var2):
    e1 = val_in_special_pins(var1.name)
    e2 = val_in_special_pins(var2.name)

    if e1 is True and e2 is False:
        return -1
    elif e1 is False and e2 is True:
        return 1
    else:
        return var_sort_by_pin(var1, var2)


def var_sort_by_pin(var1, var2):
    pin1 = get_pin_name(var1.name)
    pin2 = get_pin_name(var2.name)
    if pin1 > pin2:
        return 1
    elif pin1 < pin2:
        return -1
    else:
        return 0


def get_pin_name(var_name):
    s = [i.start() for i in re.finditer('_+', var_name)]
    return var_name[s[0] + 1:s[1]]


def val_in_special_pins(p_name):
    for i in range(0, len(special_pins)):
        if p_name == special_pins[i]["name"]:
            return True
    return False


def create_pad_vars(m_vars, test_mode_list):
    attrs = dir(test_mode_list[0].pad_list[0])
    for j in range(0, len(test_mode_list[0].pad_list)):
        for i in range(0, len(attrs)):
            if not attrs[i].startswith("_") and not attrs[i].startswith("get"):
                prefix = "dmux_"
                if not attrs[i].startswith("X"):
                    prefix += "X"
                name = prefix + attrs[i] + "_" + test_mode_list[0].pad_list[j].get_name()
                if attrs[i] == "XC":
                    var = Variable(name, VerilogWriter.wire)
                    var.set_inout(VerilogWriter.input)
                    var.set_annotation(test_mode_list[0].pad_list[j].get_interface())
                    if var.annotation == "RF GPIO":
                        var.set_macro("ifdef  " + rsap_external_ap)
                    var_list.append(var)
                else:
                    var = Variable(name, VerilogWriter.reg)
                    var.set_inout(VerilogWriter.output)
                    var.set_annotation(test_mode_list[0].pad_list[j].get_interface())
                    if var.annotation == "RF GPIO":
                        var.set_macro("ifdef  " + rsap_external_ap)
                    m_vars.append(var)


def create_special_var():
    spe_vars = []
    for i in range(0, len(special_pins)):
        s_var = Variable(special_pins[i]["name"], VerilogWriter.reg)
        s_var.set_annotation(special_pins[i]["annotation"])
        s_var.set_inout(special_pins[i]["inout"])
        s_var.set_macro(special_pins[i]["macro"])
        s_var.set_value(special_pins[i]["value"])
        spe_vars.append(s_var)
    return spe_vars


def get_value_var_mapping():
    row_start = test_mode_cfgs[-1]+1
    print(row_start)
    for i in range(27, max_column):
        for j in range(row_start, 55):
            title = xls_reader.get_cell_value(row=2, column=i)
            if title == "CODE" or title == "comments":
                continue
            cv = xls_reader.get_cell_value(row=j, column=i)
            if type(cv) == str and str.isdigit(cv) is False:
                if title == "XC":
                    read_code(cv, j, i, io_mux_other.xc_map_list)
                else:
                    read_code(cv, j, i, io_mux_other.other_map_list)


def read_code(v, row, column, map_list):
    cev = xls_reader.get_cell_value(row=row, column=column+1)
    if v in map_list.keys():
        return
    if cev is not None:
        map_list[v] = cev
    else:
        vre = VectorVar.is_vector(v)
        if vre is not None:
            v_name = v[:vre.span()[0]]
            for key in map_list.keys():
                if v_name in key:
                    kv = map_list[key]
                    kre = VectorVar.is_vector(kv)
                    if kre is not None:
                        kv_name = kv[:kre.span()[0]]
                        map_list[v] = kv_name+v[vre.span()[0]:vre.span()[1]]
                        break


def read_test_mode_cfgs():
    for i in range(3, 55):
        color = xls_reader.get_cell_color(row=i, column=27)
        if color == "FF00B0F0":
            test_mode_cfgs.append(i)


xls_reader = XlsReader(file_dir, sheet_name)
max_row = xls_reader.sheet.max_row
max_column = xls_reader.sheet.max_column


test_modes = []
assign_vars = []
var_list = []
var_condition_list = collections.OrderedDict()
read_test_mode_cfgs()
print(test_mode_cfgs)

print("max row is %d max column is %d" % (max_row, max_column))

create_test_mode(test_modes)
create_data(test_modes)
get_value_var_mapping()


# create var from xls
create_pad_vars(var_list, test_modes)

# sort var list to make rf gpio together
var_list.sort(key=functools.cmp_to_key(var_sort_rfgpio_first))

# create test_usr_var
test_user_vars = io_mux_other.define_test_user_vectors()

all_var = io_mux_other.define_other_vars_vector()+io_mux_other.define_xc_vars()+io_mux_other.define_other_vars() + \
          test_user_vars

# start to write file
res = open("result.v", mode='w')
v_writer = VerilogWriter(res)
v_writer.write_copyright()
v_writer.macro_define("include", "\"rsap_bm_param.v\"")
v_writer.write_enter()

var_list = create_special_var() + var_list
# define module
v_writer.define_module("cpads_dft_mux", all_var + var_list)

# define test mode cfg
test_mode_cfg = VectorVar("test_mode_cfg", "wire", "4", "0")
v_writer.write_expression(test_mode_cfg.define_vector_var() + VerilogWriter.semicolon)

# define test mode sel
test_mode_sel = VectorVar("test_mode_sel", "wire", "31", "0")
v_writer.write_expression(test_mode_sel.define_vector_var() + VerilogWriter.semicolon)

# assign XC
for p in range(0, len(test_modes)):
    condition = io_mux_other.condition[p]
    # assign for every test mode
    for q in range(0, len(test_modes[p].pad_list)):
        # todo write interface annotation
        name = "dmux_XC_" + test_modes[p].pad_list[q].get_name()
        key = test_modes[p].pad_list[q].XC
        if key is not None:
            if key in io_mux_other.xc_map_list:
                if key not in var_condition_list:
                    # add new var assign
                    dit = {"var": io_mux_other.xc_map_list[key],
                           "condition": condition, "true_value": name, "false_value": '''1'b0''', "multi": False,
                           "test_mode_index": p}
                    var_condition_list[key] = dit
                else:
                    # add condition to existed var assign
                    condition_pre = var_condition_list[key]["condition"]
                    # replace condition with test_mode_sel
                    if var_condition_list[key]["test_mode_index"] != -1:
                        condition_pre = test_mode_sel.invoke_vector_var(var_condition_list[key]["test_mode_index"])
                    condition_pre = VerilogWriter.or_expression(condition_pre, test_mode_sel.invoke_vector_var(p))
                    var_condition_list[key]["condition"] = condition_pre
                    var_condition_list[key]["multi"] = True
                    var_condition_list[key]["test_mode_index"] = -1

# assign 0 for var not used
assign_vars_not_in_conditions(test_user_vars, var_condition_list)
v_writer.write_enter()

# write always case
v_writer.write_always("@(*)  ")
v_writer.write_begin()

var_list.sort(key=functools.cmp_to_key(var_sort_special_first))
macro = None
for ii in range(0, len(var_list)):
    name = get_pin_name(var_list[ii].name)
    if name in default_values:
        var_list[ii].set_value(default_values[name])
        if var_list[ii].macro is not None and macro is None:
            v_writer.invoke_macro(var_list[ii].macro)
            v_writer.write_enter()
            macro = var_list[ii].macro
        elif var_list[ii].macro is not None and macro is not None and var_list[ii].macro != macro:
            v_writer.invoke_macro("endif")
            v_writer.write_enter()
            v_writer.invoke_macro(var_list[ii].macro)
            macro = var_list[ii].macro
        elif var_list[ii].macro is None and macro is not None:
            v_writer.invoke_macro("endif")
            v_writer.write_enter()
            macro = None

        v_writer.write_expression(var_list[ii].set_var_value())
        if ii == len(var_list) - 1 and macro is not None:
            v_writer.get_invoke_macro("endif")
            v_writer.write_enter()

v_writer.write_case("1'b1")

# set value to vars
attrs = dir(test_modes[0].pad_list[0])
for k in range(0, len(test_modes)):
    v_writer.case_item(test_mode_sel.invoke_vector_var(k))
    v_writer.write(VerilogWriter.space * 3)
    v_writer.write_begin()
    tm_list = []
    for n in range(0, len(test_modes[k].pad_list)):
        for o in range(0, len(attrs)):
            if not attrs[o].startswith("_") and not attrs[o].startswith("get") and attrs[o] not in unchanged_attrs:
                prefix = "dmux_"
                if not attrs[o].startswith("X"):
                    prefix += "X"
                name = prefix + attrs[o] + "_" + test_modes[k].pad_list[n].get_name()

                var = Variable(name, VerilogWriter.reg)
                if test_modes[k].pad_list[n].get_interface() == "RF GPIO":
                    var.set_macro("ifdef  " + rsap_external_ap)
                var.set_annotation("X" + attrs[o])
                value = getattr(test_modes[k].pad_list[n], attrs[o])
                if value == 0 or value == "0":
                    var.set_value("1'b0")
                    tm_list.append(var)
                elif value == 1 or value == "1":
                    var.set_value("1'b1")
                    tm_list.append(var)
                elif value is not None:

                    if value in io_mux_other.other_map_list:
                        var.set_value(io_mux_other.other_map_list[value])
                        tm_list.append(var)

    tm_list.sort(key=functools.cmp_to_key(var_sort_rfgpio_first))

    vl = len(tm_list)
    print(vl)
    macro = None
    annotation = None

    for p in range(0, vl):
        val = tm_list[p].set_var_value()
        if val is not None:
            if tm_list[p].macro is not None and macro is None:
                v_writer.invoke_macro(tm_list[p].macro)
                v_writer.write_enter()
                macro = tm_list[p].macro
            elif tm_list[p].macro is not None and macro is not None and tm_list[p].macro != macro:
                v_writer.invoke_macro("endif")
                v_writer.write_enter()
                v_writer.invoke_macro(tm_list[p].macro)
                macro = tm_list[p].macro
            elif tm_list[p].macro is None and macro is not None:
                v_writer.invoke_macro("endif")
                v_writer.write_enter()
                macro = None
            if tm_list[p].annotation is not None and tm_list[p].annotation != annotation:
                v_writer.write_annotation(
                    3, tm_list[p].annotation, 16)
                annotation = tm_list[p].annotation
            v_writer.write_expression(val)
            if p == vl - 1 and macro is not None:
                v_writer.get_invoke_macro("endif")
                v_writer.write_enter()

    v_writer.write_end()

# end case
v_writer.write_end_case()
v_writer.write_end()

pll_test_mode = Variable("pll_test_mode", "wire")
usbphy_test_mode = Variable("usbphy_test_mode", "wire")
catip_test_mode0 = Variable("catip_test_mode0", "wire")
# ddrphy_scan_mode = Variable("ddrphy_scan_mode", "wire")
ddrphy_test_mode = Variable("ddrphy_test_mode", "wire")

v_writer.write_expression(pll_test_mode.define_var() + VerilogWriter.semicolon)
v_writer.write_expression(usbphy_test_mode.define_var() + VerilogWriter.semicolon)
v_writer.write_expression(catip_test_mode0.define_var() + VerilogWriter.semicolon)
v_writer.write_expression(ddrphy_test_mode.define_var() + VerilogWriter.semicolon)

assign_expressions = collections.deque()
tm_index = -1

for r, s in var_condition_list.items():
    multi = s["multi"]
    if multi:
        condition = v_writer.p_thesis_expression(s["condition"])
        three = v_writer.ternary_expression(
            condition, s["true_value"], s["false_value"])
        assign_expressions.appendleft(v_writer.get_assign_expression(s["var"], three) + v_writer.space * 4)
    else:
        if s["test_mode_index"] != tm_index:
            tm_index = s["test_mode_index"]
            anno = v_writer.enter + v_writer.space * 4
            condition = io_mux_other.condition[tm_index]
            # annotation
            anno += v_writer.get_annotation(2, test_modes[tm_index].name, 4)
            # assign test mode
            anno += v_writer.get_assign_expression(condition, test_mode_sel.invoke_vector_var(tm_index))
            assign_expressions.append(anno)

        condition = s["condition"]
        three = v_writer.ternary_expression(
            condition, s["true_value"], s["false_value"])
        assign_expressions.append(v_writer.get_assign_expression(s["var"], three) + v_writer.space * 4)

v_writer.write_enter()

for t in range(0, len(assign_expressions)):
    v_writer.write_expression(assign_expressions[t])


tmc_vector = []
for c in reversed(test_mode_cfgs):
    tmc_vector.append("dmux_XC_"+xls_reader.get_cell_value(c, 4))


v_writer.write_annotation(2, "TEST MODE DMUX", 4)
test_mode_cfg.set_value(v_writer.create_vector(tmc_vector))
v_writer.write_expression(test_mode_cfg.assign_var_value())

for q in range(0, len(test_modes)):
    equal = v_writer.equal_expression(
        test_mode_cfg.name, v_writer.create_num(len(test_mode_cfgs), 10, q))
    and_exp = v_writer.and_expression(
        v_writer.p_thesis_expression(equal), "test_mode")
    v_writer.write_expression(v_writer.get_assign_expression(
        test_mode_sel.invoke_vector_var(q), and_exp))

v_writer.write_end_module()
res.close()
