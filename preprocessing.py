import sys
import numpy as np
import re
import time
import datetime

def preprocessing(datas):
    res = np.zeros((1, 9))
    for data in datas:
        collect_row = []
        for i in range(data.shape[0]):
            t = data[i][1].split('.')
            genre = data[i][6]
            if len(t) > 1 and genre != '-':
                collect_row.append(i)
        data = data[collect_row]
        data = data[data[:,1].argsort()]
        res = np.concatenate((res, data), axis=0)
    return res


start = int(sys.argv[1])
end = int(sys.argv[2])
datas = []
for i in range(start, end+1):
    data = np.load('data/songs_{0}.npy'.format(i))
    years = np.full((data.shape[0], 1), i)
    data = np.concatenate((years, data), axis=1)
    datas.append(data)

res = preprocessing(datas)[1:]
print(res.shape)
np.save('data/songs_preprocessed', res)