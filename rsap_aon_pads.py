from output_v import VerilogWriter
from output_v import Variable
from output_v import Module
import sys
from xls_reader import XlsReader

pdwuw_h_args = []
modules = []
pdx_args = ["XOUT", "XC", "DS0", "DS1", "DS2", "XE", "XIN"]



print(sys.argv)

file_dir = "SF19A28C_IO_Mux.xlsx"
sheet_name = "IO MUX"

if len(sys.argv) == 2:
    file_dir = sys.argv[1]

if len(sys.argv) == 3:
    sheet_name = sys.argv[2]

xls_reader = XlsReader(file_dir, sheet_name)
max_row = xls_reader.sheet.max_row
max_column = xls_reader.sheet.max_column

for j in range(27, 43):
    value = xls_reader.get_cell_value(row=2, column=j)
    if value is not None and value != "CODE":
        if value.startswith("DS"):
            pdwuw_h_args.append("DS0")
            pdwuw_h_args.append("DS1")
            pdwuw_h_args.append("DS2")
        else:
            if value.startswith("X"):
                value = value[1:]
            pdwuw_h_args.append(value)

for i in range(3, 5):
    cv = xls_reader.get_cell_value(row=i, column=4)
    module = Module("PDWUWCDGRGM_H", pdwuw_h_args)
    for arg in pdwuw_h_args:
        module.arg_vals[arg] = "X" + arg + "_" + cv
    module.arg_vals["PAD"] = "XP_" + cv
    module.instance_name = cv
    modules.append(module)

pdx_module = Module("PDXOEDG8E_H_G", pdx_args)
pdx_module.instance_name = "XTAL_XIO"

for arg in pdx_args:
    pdx_module.arg_vals[arg] = "X" + arg + "_" + pdx_module.instance_name
pdx_module.arg_vals["XIN"] = xls_reader.get_cell_value(row=127, column=4)
pdx_module.arg_vals["XOUT"] = xls_reader.get_cell_value(row=128, column=4)


modules.append(pdx_module)

var_list = []

for m in modules:
    for k, v in m.arg_vals.items():
        inout = "input"
        if v == "XP_XTAL_XO" or v.startswith("XC") or v.startswith("XXC"):
            inout = "output"
        elif m.name == "PDWUWCDGRGM_H" and v.startswith("XP_"):
            inout = "inout"
        var = Variable(v, None)
        var.set_inout(inout)
        var_list.append(var)

res = open("result.v", mode='w')
v_writer = VerilogWriter(res)
v_writer.write_copyright()

v_writer.define_module("rsap_aon_pads", var_list)

for k in modules:
    v_writer.invoke_module(k)

v_writer.write_end_module()

res.close()
