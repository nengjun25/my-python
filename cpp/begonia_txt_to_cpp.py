import sys
import os
sys.path.append('/home/zx/my-python/iomux')
from output_c import CppWriter

includes = '''
#include "USBIO.H"
#include <iostream>
#include <windows.h>
#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
'''

if len(sys.argv) < 2:
    print("arguments error !")
    sys.exit()

txt_dir = sys.argv[1]

if os.path.exists("./result") is not True:
    os.mkdir("./result")

txts = os.listdir(txt_dir)

for txt in txts:
    # and txt.startswith("Begonia_ATE_Aux_ADC_1v2")
    if txt.endswith(".txt"):
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
                print(line)
                if start is False:
                    c_writer.define_function(CppWriter.void, txt[:-4], None)
                    start = True
                line_list = line.split(" ")
                ll = len(line_list)
                if ll > 1:
                    if line_list[0] == "W":
                        print(line_list)
                        arg1 = line_list[1][0:4]
                        arg2 = line_list[2][0:4]
                        c_writer.call_function(line_list[0], ["0x"+arg1, "0x"+arg2])
                        c_writer.write(c_writer.space*2)
                        if ll > 3:
                            i = 3
                            for i in range(2, ll):
                                if line_list[i] == "//":
                                    break
                                elif "//" in line_list[i]:
                                    line_list[i] = line_list[i][line_list[i].index("//")    :]
                                    break
                            if i != ll-1:
                                c_writer.write(" ".join(line_list[i:]))
                        c_writer.write_enter()
                    elif line_list[0] == "R":
                        print(line_list)
                        c_writer.call_function(line_list[0], ["0x" + line_list[1]])
                        c_writer.write(c_writer.space * 2)
                        if ll > 3:
                            i = 3
                            for i in range(2, ll):
                                if line_list[i] == "//":
                                    break
                            if i != ll - 1:
                                c_writer.write(" ".join(line_list[i:]))
                        c_writer.write_enter()
                    elif line_list[0] == "wait":
                        print(line_list)
                        if "ms" in line_list[1]:
                            f = float(line_list[1][:line_list[1].index("ms")])
                            if f >= 1:
                                c_writer.call_function("sleep", [str(int(f))])
                            else:
                                c_writer.call_function("MySleep", [str(int(f*1000))])
                        c_writer.write(c_writer.space*2+"//"+line)
                        c_writer.write_enter()
                    elif line_list[0] == "M":
                        print(line_list)
                        c_writer.write("//"+line)

            else:
                c_writer.write(line)
                c_writer.write_enter()
        c_writer.end_function()
        res.close()



