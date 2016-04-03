print("Loading...")
import urllib.request
print("Trying log out...")
req_un = urllib.request.Request("https://net.zju.edu.cn/rad_online.php",
                                b"action=auto_dm&username=3110103335&password=V27xT6du")
req_un.add_header("Content-Type", "application/x-www-form-urlencoded")
res_un = urllib.request.urlopen(req_un).read().decode()
if (res_un == "ok"):
    print("***************Log out success.***************")
else:
    print("Log out failed!")
import time
time.sleep(1)
