import sys
import numpy as np

def get_dict(data):
    genre_dict = dict()
    genre_id = 0
    for i in range(data.shape[0]):
        genres = data[i][6].split(', ')
        for genre in genres:
            if not genre in genre_dict:
                genre_dict[genre] = genre_id
                genre_id += 1
    return genre_dict

def data_to_num(data, genre_dict):
    res = np.zeros((data.shape[0], 5 + len(genre_dict)))
    for i in range(data.shape[0]):
        res[i,0] = int(data[i,0])

        res[i,1] = int(data[i,2])

        if data[i,8] == '그룹':
            res[i,2] = 1
        
        if data[i,7] == '남성':
            res[i,3] = 1
        elif data[i,7] == '혼성' or data[i,7] == '':
            res[i,3] = 0.5

        if data[i,5] == 'True':
            res[i,4] = 1
            
        genres = data[i][6].split(', ')
        for genre in genres:
            res[i,5+genre_dict[genre]] += 1 / len(genres)

    return res
        
np.set_printoptions(formatter={'float_kind': lambda x: "{0:0.1f}".format(x)})
data = np.load('data/songs_preprocessed.npy')
genre_dict = get_dict(data)
print(genre_dict)
res = data_to_num(data, genre_dict)
print(res.shape)
print(res)
np.save('data/songs_final', res)
#print(res[res[:,0] > 2012, 4].mean(axis=0))
