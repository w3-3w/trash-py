import yaml
import csv
from pathlib import Path

with open('usermap.csv', 'w', newline='') as usermap:
    path = Path('userdata')
    writer = csv.writer(usermap)
    for userdatapath in path.iterdir():
        with userdatapath.open() as olduser:
            dataMap = yaml.load(olduser)
            username = userdatapath.name[:-4]
            if ('uuid' in dataMap):
                uuid = dataMap['uuid']

                dataMap['lastAccountName'] = username

                newuser = open(uuid + '.yml', 'w')
                yaml.dump(dataMap, newuser, default_flow_style = False)
                newuser.close()
                writer.writerow([username, uuid])
                print(username + ' done')
            else:
                print(username + ' skipped')
