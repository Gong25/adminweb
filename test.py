
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

def get_graph():
    poverty_lever = pd.read_csv('static/PercentagePeopleBelowPovertyLevel.csv', encoding='windows-1252')
    poverty_lever.poverty_rate.replace(['-'],0.0,inplace=True)
    poverty_lever.poverty_rate = poverty_lever.poverty_rate.astype(float)
    area_list = list(poverty_lever['Geographic Area'].unique())
    area_poverty_rate_ratio = []
    
    data = pd.DataFrame({'area_list' : area_list, 'area_poverty_rate_ratio':area_poverty_rate_ratio})
    new_index = (data['area_poverty_rate_ratio'].sort_values(ascending=False)).index.values
    sort_data = data.reindex(new_index)

    plt.figure(figsize=(20,15))

    plt.savefig("cur_graph.png")
    

    if __name__ == "__main__":
        get_graph()