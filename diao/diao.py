# Python 3.4.1
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
print("Config loaded.")
sta = config["settings"]["start"]
sto = config["settings"]["stop"]
ox = float(config["settings"]["offset_x"])
oy = float(config["settings"]["offset_y"])
f_head_name = config["io"]["head"]
f_inp_name = config["io"]["input"]
f_outp_name = config["io"]["output"]

# 转换读取的一行内容为便于处理的list
def convert_in(t):
    li = t.split(" ")
    r = []
    r.append(int(li[1][1:]))
    r.append(float(li[2][1:]))
    r.append(float(li[3][1:]))
    r.append(float(li[4][1:]))
    return r

def offset(p):
    if p:
        return 1
    else:
        return -1

f_outp = open(f_outp_name, "w")
f_head = open(f_head_name, "r")
f_outp.write(f_head.read())
f_head.close()
f_inp = open(f_inp_name, "r")

first = True
# x方向是否正朝正方向移动
x_p = True
# y方向是否正朝正方向移动
y_p = True
# 调整量
x_offset = 0
y_offset = 0
# 处理的行数
count = 0

for l in f_inp:
    now = convert_in(l)
    if first:
        pre = list(now)
        first = False
        tail = ""
    else:
		# 按要求的格式输出到文件
        f_outp.write("G{0} X{1} Y{2} \n{3}".format(pre[0],
                                                   format(pre[1] + x_offset, ".5f"),
                                                   format(pre[2] + y_offset, ".5f"),
                                                   tail))
        tail = ""
		# 判断是否需要start和stop标记
        if ((now[3] < 0) and (pre[3] >= 0)):
            f_outp.write(sta + " \n")
        elif ((now[3] >= 0) and (pre[3] < 0)):
            tail = sto + " \n"
        count += 1
		# 判断各轴移动方向是否改变，若是则调整offset
        if ((offset(x_p) * (now[1] - pre[1])) < 0):
            x_offset += - offset(x_p) * ox
            x_p = not x_p
        if ((offset(y_p) * (now[2] - pre[2])) < 0):
            y_offset += - offset(y_p) * oy
            y_p = not y_p

        pre = list(now)
        

f_outp.write("G{0} X{1} Y{2} \n{3}".format(pre[0],
                                           format(pre[1] + x_offset, ".5f"),
                                           format(pre[2] + y_offset, ".5f"),
                                           tail))
count += 1
print("{nrow} rows processed.".format(nrow = count))
f_inp.close()
f_outp.close()
print("******************Completed******************")
