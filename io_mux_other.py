# Filename: io_mux_other.py

from output_v import VerilogWriter
from output_v import VectorVar
from output_v import Variable
import re
import collections
from enum import Enum


class Inout(Enum):
    IN = "IN"
    OUT = "OUT"


pll_macro = '''PLL_CTRL_WIDTH+12'''
efuse_in_macro = '''EFUSE_TIN_NUM  -1'''
efuse_out_macro = '''EFUSE_TOUT_NUM  -1'''
scan_clock_macro = '''SCAN_CLOCK_COUNT  -1'''


suffix_test_user_in = "_test_user_in"
suffix_test_user_out = "_test_user_out"

bus_count = 8
bm_count = 8
am_count = 32

condition = [
    "pll_test_mode",
    "cpu_mb_mode",
    "usbphy_test_mode",
    "test_mode_sel[3]",
    "catip_test_mode0",
    "scanmode",
    "ddrphy_test_mode"
]

test_user_vars = []

xc_map_list = collections.OrderedDict()
other_map_list = collections.OrderedDict()


def get_macro_rsap(name, inout=Inout.IN):
    reg = "[0-9]+"
    prog = re.compile(reg)
    res = prog.findall(name)
    s = ""
    if res is not None:
        if name.startswith("bus"):
            s = VerilogWriter.get_invoke_macro(
                "RSAP_B" + res[0] + "M" + res[1] + "_T" + inout.value + "_NUM   -1")
        elif name.startswith("am"):
            s = VerilogWriter.get_invoke_macro(
                "RSAP_AM" + res[0] + "_T" + inout.value + "_NUM   -1")
    # print(s)
    return s


def define_one_vector(name, high, inout=Inout.IN):
    test_user = VectorVar(name, VerilogWriter.wire, high, "0")
    test_user.set_inout("input" if (inout == Inout.IN) else "output")
    xls = has_xls_name(name, xc_map_list)
    if xls is not None:
        test_user.set_xls_name(xls)
    else:
        xls = has_xls_name(name, other_map_list)
        test_user.set_xls_name(xls)
    return test_user


def has_xls_name(name, var_list):
    for k, v in var_list.items():
        # print(v)
        if v == name:
            return k
        else:
            res = re.search('\[.*\]$', v)
            if res is not None:
                if v[0:res.span()[0]] == name:
                    return k
    return None


def define_xc_vars():
    vectors = collections.OrderedDict()
    m_vars = []

    for v in xc_map_list.values():
        if v.startswith("bus") is True or v.startswith("test_mode_cfg") is True:
            continue
        v_name, count = VectorVar.get_vector_name(v)
        if v_name is not None:
            if v_name in vectors.keys():
                if int(count) > int(vectors[v_name]):
                    vectors[v_name] = count
            else:
                vectors[v_name] = count
        else:
            m_vars.append(define_one_var(v, Inout.OUT))

    for key, value in vectors.items():
        high = value
        if key == "pll_test_user_in":
            high = VerilogWriter.get_invoke_macro(pll_macro)
        elif key == "scan_clock":
            high = VerilogWriter.get_invoke_macro(scan_clock_macro)
        if key.endswith(suffix_test_user_in) or key.endswith(suffix_test_user_out):
            test_user_vars.append(define_one_vector(key, high, Inout.OUT))
        else:
            m_vars.append(define_one_vector(key, high, Inout.OUT))
    return m_vars


def define_other_vars():
    vectors = collections.OrderedDict()
    m_vars = []

    for v in other_map_list.values():
        if v.startswith("bus") is True:
            continue
        v_name, count = VectorVar.get_vector_name(v)
        if v_name is not None:
            if v_name in vectors.keys():
                if int(count) > int(vectors[v_name]):
                    vectors[v_name] = count
            else:
                vectors[v_name] = count
        else:
            m_vars.append(define_one_var(v, Inout.IN))

    for key, value in vectors.items():
        if key.endswith(suffix_test_user_in) or key.endswith(suffix_test_user_out):
            test_user_vars.append(define_one_vector(key, value, Inout.OUT))
        else:
            m_vars.append(define_one_vector(key, value, Inout.IN))
    return m_vars


def define_test_user_vectors():
    test_user_vars.append(define_one_vector("iram" + suffix_test_user_in, "37", Inout.OUT))
    test_user_vars.append(define_one_vector("iram" + suffix_test_user_out, "15", Inout.IN))
    test_user_vars.append(define_one_vector("efuse" + suffix_test_user_in, VerilogWriter.get_invoke_macro(efuse_in_macro), Inout.OUT))
    test_user_vars.append(define_one_vector("efuse" + suffix_test_user_out, VerilogWriter.get_invoke_macro(efuse_out_macro), Inout.IN))

    for i in range(1, bus_count + 1):
        for j in range(1, bm_count + 1):
            s = "bus%d_bm%d" % (i, j)
            # output
            test_user_vars.append(define_one_vector(
                s + suffix_test_user_in, get_macro_rsap(s, Inout.IN), Inout.OUT))
            # input
            test_user_vars.append(define_one_vector(
                s + suffix_test_user_out, get_macro_rsap(s, Inout.OUT), Inout.IN))

    for k in range(0, am_count):
        s = "am%d" % k
        # output
        test_user_vars.append(define_one_vector(
            s + suffix_test_user_in, get_macro_rsap(s, Inout.IN), Inout.OUT))
        # input
        test_user_vars.append(define_one_vector(
            s + suffix_test_user_out, get_macro_rsap(s, Inout.OUT), Inout.IN))

    # for l in range(0, len(test_user_vars)):
    #    print(test_user_vars[l].define_vector_var())

    return test_user_vars


def define_one_var(name, inout=Inout.IN):
    var = Variable(name, VerilogWriter.wire)
    var.set_inout("input" if (inout == Inout.IN) else "output")
    return var


def define_other_vars_vector():
    return [
        define_one_var("test_mode", Inout.IN),
        define_one_var("scanmode", Inout.OUT),
        define_one_var("scan_mb_jtag_tdo_en", Inout.IN),
        define_one_var("cpu_mb_mode", Inout.OUT)]

