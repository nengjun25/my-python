import sys
import xlwt
import os

print(sys.argv)
if len(sys.argv) < 2:
    print("arguments error ! please run : python check_test_ret_to_xls.py file_name")
    sys.exit()

file_name = sys.argv[1]

workbook = xlwt.Workbook(encoding='gbk')

res = open(file_name, mode='r')
xls_name = "./result.xls"
if os.path.exists("./result.xls"):
    os.remove("./result.xls")

s = res.read()
s_list = s.splitlines(False)
s_list.pop()
s_list.pop()

sheet_names = []

font = xlwt.Font()
font.height = 20 * 11
style = xlwt.XFStyle()
style.font = font

sheet = None
k = 0
for i in range(0,len(s_list)):
    one_list = s_list[i].split(" ")
    state = one_list[0]
    all_name = one_list[-1]

    if "_" in all_name:
        s_index = all_name.index("_")
        sheet_name = all_name[:s_index]
        item_name = all_name[s_index+1:]

        if sheet_name not in sheet_names:
            sheet_names.append(sheet_name)
            sheet = workbook.add_sheet(sheet_name)
            sheet.write(0, 1, "name", style=style)
            sheet.write(0, 2, "state", style=style)
            sheet.write(0, 3, "time", style=style)
            sheet.col(1).width = 256 * 100
            k = 1
        sheet.write(k, 1, item_name, style=style)
    sheet.write(k, 0, k, style=style)
    sheet.write(k, 2, state, style=style)
    if state == "PASS" or state == "FAILED":
        time = one_list[-2]
        tn = float(time)/1000000000
        if len(time) > 6:
            time = time[:-3]
            tl = list(time)
            tl.insert(-3, ".")
            ss = "%.3f" % tn
        else:
            tn = float(time)
            ss = "%.3f" % tn
        sheet.write(k, 3, "%.3f" % tn, style=style)
    sheet.row(k).height = 20 * 15
    k = k+1

workbook.save(xls_name)



