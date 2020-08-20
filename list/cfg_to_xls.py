import sys
import xlwt
import os

print(sys.argv)
if len(sys.argv) < 4:
    print("arguments error ! please run : python xlsx_to_cfg.py name1.txt name2.xlsx sheet_name column_index")
    sys.exit()

txt_dir = sys.argv[1]
sheet_name = sys.argv[2]
column_index = sys.argv[3]

if os.path.exists("./result") is not True:
    os.mkdir("./result")

cfgs = os.listdir(txt_dir)
for cfg in cfgs:
    if cfg.endswith(".cfg"):
        workbook = xlwt.Workbook(encoding='gbk')
        sheet = workbook.add_sheet(sheet_name)
        res = open(txt_dir+cfg, mode='r')
        xls_name = "./result/"+cfg[:-4]+".xls"
        print(xls_name)
        s = res.read()
        s_list = s.splitlines(False)

        if len(s_list) > 2:
            del s_list[0]
            s_list.pop()

        font = xlwt.Font()
        font.height = 20 * 11
        style = xlwt.XFStyle()
        style.font = font

        for i in range(0, len(s_list)):
            sheet.write(i, 0, i + 1)
            res = None
            if "," in s_list[i]:
                index = s_list[i].rindex(",")
                res = s_list[i][:index]
            else:
                res = s_list[i]
            sheet.write(i, int(column_index), res, style=style)

        for j in range(0, len(s_list) + 5):
            sheet.row(j).height = 20 * 15
            sheet.col(int(column_index)).width = 256 * 100

        workbook.save(xls_name)
