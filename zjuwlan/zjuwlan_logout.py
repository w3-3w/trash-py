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
    print("Account info loaded. Trying log out...")
    data_un = {
        "action": "auto_dm",
        "username": f["account"]["username"],
        "password": f["account"]["password"]
    }
    req_un = urllib.request.Request("https://net.zju.edu.cn/rad_online.php",
                                    urllib.parse.urlencode(data_un).encode())
    req_un.add_header("Content-Type", "application/x-www-form-urlencoded")
    res_un = urllib.request.urlopen(req_un).read().decode()
    if (res_un == "ok"):
        print("******************Log out success.******************")
    else:
        print("Log out failed!")
except:
    print("Failed!")
    print("Check if ZJUWLAN is connected or file 'config.ini' exists!")
    print("Did you input the correct password in 'config.ini' ?\n")
    time.sleep(4)
finally:
    print("Program terminates.")
    time.sleep(1)
