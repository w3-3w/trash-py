from pathlib import Path
import yaml

rootPath = Path('.')
resultUsername = open('username.txt', 'w')
resultUuid = open('uuid.txt', 'w')
for essDataPath in rootPath.iterdir():
    with essDataPath.open() as essData:
        if (essDataPath.suffix == '.yml'):
            print('processing ' + essDataPath.stem)
            dataMap = yaml.load(essData)
            if ('logoutlocation' in dataMap):
                if (dataMap['logoutlocation']['world'] in ['mczju', 'mczju_nether', 'mczju_the_end', 'ZJU']):
                    resultUsername.write(dataMap['lastAccountName'] + '\n')
                    resultUuid.write(essDataPath.stem + '\n')
resultUsername.close()
resultUuid.close()
print('done')
