import os

keepListFile = open('uuid.txt', 'r')
keepList = []
for line in keepListFile:
    keepList.append(line[:-1])
keepListFile.close()

for data in os.listdir():
    if (not (data[:-4] in keepList)) and (data[-4:] == '.dat'):
        os.remove(data)
        print('deleted ' + data)
print('done')
