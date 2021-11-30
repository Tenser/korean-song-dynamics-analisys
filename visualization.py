import sys
import numpy as np
import matplotlib.pyplot as plt
import analisys

data = np.load('data/songs_final.npy')
years = analisys.years
genre_dict = analisys.genre_dict
plt.plot(years, analisys.getGroupRate(data))
plt.title('그룹여부비율')
plt.show()

plt.plot(years, analisys.getManRate(data))
plt.title('남자가수비율')
plt.show()

plt.plot(years, analisys.getFeaturingRate(data))
plt.title('피쳐링유무비율')
plt.show()

genre_rates = analisys.getGenreRates(data)
for genre in genre_dict:
    plt.plot(years, genre_rates[genre])
    plt.title('{} 비중'.format(genre))
    plt.show()