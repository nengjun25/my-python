import sys
import os
sys.path.append('/home/zx/my-python/iomux')
from output_c import CppWriter

includes = '''
#include "USBIO.H"
#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h>
'''

if len(sys.argv) < 2:
    print("arguments error !")
    sys.exit()

txt_dir = sys.argv[1]

if os.path.exists("./result") is not True:
    os.mkdir("./result")

txts = os.listdir(txt_dir)

for txt in txts:
    if txt.endswith(".mem"):
        source = open(txt_dir+txt, mode="r")
        res = open("./result/"+txt[:-4]+".cpp", mode="w")
        c_writer = CppWriter(res)
        c_writer.write(includes)

        s = source.read()
        s_list = s.splitlines(False)
        start = False
        for line in s_list:
            line = line.replace("\t", " ")
            if line.startswith('//') is False and line != "":
                line_list = line.split(" ")
                if start is False:
                    c_writer.define_function("USHORT", txt[:-4], None)
                    start = True
                if len(line_list) == 1:
                    c_writer.call_function("W", ["0x3802","0x"+line_list[0]])
                else:
                    c_writer.call_function("W", ["0x"+line_list[0], "0x"+line_list[1]])
                c_writer.write_enter()
            else:
                c_writer.write(line)
                c_writer.write_enter()
        c_writer.return_value("0")
        c_writer.end_function()
        res.close()



