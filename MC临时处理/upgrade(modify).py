import yaml
from pathlib import Path

path = Path('.')
for userDataPath in path.iterdir():
    if (userDataPath.suffix == '.yml'):
        with userDataPath.open() as oldData:
            dataMap = yaml.load(oldData)
        dataMap.pop('lastlocation', None)
        dataMap.pop('uuid', None)
        newData = open(userDataPath.name, 'w')
        yaml.dump(dataMap, newData, default_flow_style = False)
        newData.close()
print('done')
