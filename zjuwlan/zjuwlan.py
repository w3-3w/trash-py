# Python 3.4.0

#######################################################################
#                      Auto connect ZJUWLAN                           #
#                            by w3_3w                                 #
#######################################################################
import urllib.request
import urllib.parse
import configparser
import time
try:
    f = configparser.ConfigParser()
    f.read("config.ini")
    print("Account info loaded. Trying login...")
	# 登录用data
    data = {
        "type": 1,
        "username": f["account"]["username"],
        "local_auth": 1,
        "mac": "",
        "password": f["account"]["password"],
        "action": "login",
        "is_ldap": 1,
        "ac_id": 3,
        "wbaredirect": ""
    }
    req = urllib.request.Request("https://net.zju.edu.cn/cgi-bin/srun_portal",
                                 urllib.parse.urlencode(data).encode())
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
	# res存储登录操作的返回信息
    res = urllib.request.urlopen(req).read().decode()
    if (res == "\u60a8\u5df2\u5728\u7ebf\uff0c\u8bf7\u6ce8\u9500\u540e\u518d\u767b\u5f55\u3002"):
        if (int(f["settings"]["auto-kick"]) == 1):
            print("Already logged in. Trying log out...")
			# 注销用data
            data_un = {
                "action": "auto_dm",
                "username": f["account"]["username"],
                "password": f["account"]["password"]
            }
            req_un = urllib.request.Request("https://net.zju.edu.cn/rad_online.php",
                                            urllib.parse.urlencode(data_un).encode())
            req_un.add_header("Content-Type", "application/x-www-form-urlencoded")
			# res_un存储注销操作的返回信息
            res_un = urllib.request.urlopen(req_un).read().decode()
            if (res_un == "ok"):
                print("Log out success. Trying login...")
                res = urllib.request.urlopen(req).read().decode()
                if (("login_ok" in res) or ("help.html" in res)):
                    print("*****************Login success!*****************")
                else:
                    print("Login failed!")
            else:
                print("Log out failed!")
        else:
            print("Already logged in while auto-kick disabled!")
    elif (("login_ok" in res) or ("help.html" in res)):
        print("*****************Login success!*****************")
    else:
        print("Login failed!")
except:
    print("Failed!")
    print("Check if ZJUWLAN is connected or file 'config.ini' exists!")
    print("Did you input the correct password in 'config.ini' ?\n")
    time.sleep(4)
finally:
    print("Program terminates.")
    time.sleep(1)
