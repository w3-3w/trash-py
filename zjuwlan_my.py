print("Loading...")
import urllib.request
try:
    print("Trying login...")
    req = urllib.request.Request("https://net.zju.edu.cn/cgi-bin/srun_portal",
                                 b"type=1&user_ip=&username=3110103335&local_auth=1&mac=&password=V27xT6du&action=login&is_ldap=1&ac_id=3&wbaredirect=")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    res = urllib.request.urlopen(req).read().decode()
    if (res == "您已在线，请注销后再登录。"):
        print("Already logged in. Trying log out...")
        req_un = urllib.request.Request("https://net.zju.edu.cn/rad_online.php",
                                        b"action=auto_dm&username=3110103335&password=V27xT6du")
        req_un.add_header("Content-Type", "application/x-www-form-urlencoded")
        res_un = urllib.request.urlopen(req_un).read().decode()
        if (res_un == "ok"):
            print("Log out success. Trying login...")
            res = urllib.request.urlopen(req).read().decode()
            if (("login_ok" in res) or ("help.html" in res)):
                print("**********************Login success!**********************")
            else:
                print("Login failed!")
        else:
            print("Log out failed!")
    elif (("login_ok" in res) or ("help.html" in res)):
        print("**********************Login success!**********************")
    else:
        print("Login failed!")
except:
    print("Failed!")
import time
time.sleep(1)
