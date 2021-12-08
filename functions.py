import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def clusterDemographics(folder, years, field_names, n_clusters):
    
    clusters_over_time = []
    demographic_dfs = []
    fields = field_names[0:-1]
    
    for year in years:
        
        
        if year > 2017:
            
            df = pd.read_csv(folder + "ISBE_" + str(year) + ".csv", sep = ",", low_memory = False)
            
            df = df[df['School Type']=='HIGH SCHOOL']
            df = df[df['District'] == 'City of Chicago SD 299']
            df = df.filter(field_names)
            
            
            demographic_df = df.filter(field_names[0:-1])
        
        else:
            
            if year == 2017:
                
                num_fields = [3,13,14,15,16,53,69,137,241,881,20]
                
            elif year == 2016:
                
                num_fields = [3,13,14,15,16,53,69,137,141,837,20]
                
            elif year == 2015:
                
                num_fields = [3,13,14,15,16,53,69,137,141,741,20]
                
            
            df = pd.read_csv(folder + "ISBE_" + str(year) + ".csv", sep = ",",header = None ,low_memory = False)
            
            df = df[df[11] == 'HIGH SCHOOL']
            df = df[df[4] == 'City of Chicago SD 299           ']
            
            df = df.filter(num_fields)
            
            for i in range(5):
                
                j = i+6
                temp = list(df[num_fields[j]])
                
                for k in range(len(temp)):
                    
                    try:
                        if j == 10:
                            if "," in temp[k]:
                                temp[k] = int(temp[k].split(",")[0])*1000 + int(temp[k].split(",")[1])   
                            else:
                                temp[k] = int(temp[k])
                        else:
                            temp[k] = float(temp[k])
                        
                    except:
                        temp[k] = 0
                
                df[num_fields[j]] = temp
        
            df.columns = field_names
            
            demographic_df = df.filter(field_names[0:-1])
            
            
        
        X = np.delete(demographic_df.values, [0,6,7,8,9], axis = 1)
        X = X.astype(float)
        X[np.isnan(X)] = 0
        
        clusters = KMeans(n_clusters = n_clusters).fit(X)
        labels = list(clusters.labels_)
        
        demographic_df['Cluster Position'] = labels
        df['Cluster Position'] = labels
        
        
        demographic_df['# Student Enrollment'] = df['# Student Enrollment']
        demographic_df = demographic_df.fillna(0)
        cluster_means = []
        
        for i in range(n_clusters):
            
            # print('AVERAGES OF CLUSTER: ' + str(i+1) )
            # print(round(demographic_df[demographic_df['Cluster Position']==i].mean(),2))
            # print('\n')
        
            current_df = demographic_df[demographic_df['Cluster Position']==i]
            
            means = []
            
            for j in range(len(fields)-1):
                
                total_in_cluster = np.dot(current_df[fields[j+1]],current_df['# Student Enrollment'])
                
                means.append(total_in_cluster/sum(current_df['# Student Enrollment']))
                
            means.append(i)
            cluster_df = pd.Series(data = means, index = fields[1:]+['Cluster Position'], dtype = float)
            
            cluster_means.append(cluster_df)
            
            
        clusters_over_time.append(cluster_means)
        
        demographic_dfs.append(demographic_df)
    
    demographic_dfs[0].to_csv('Demographic Clusters/demographics_' + str(years[0]) + '.csv')

    return demographic_dfs,clusters_over_time

def order_min(array):
    
    index = dict(zip(array,np.arange(0,len(array))))
    rev_index = dict(zip(np.arange(0,len(array)),array))
    array.sort()
    
    order_index = []
    new_array = list(rev_index.values())
    
    for i in range(len(array)):
        
        order_index.append(index[array[i]])
    
    return order_index,new_array


def swapPositions(matchings, lst, n_clusters):
     
    newlst= []
    
    for i in range(len(matchings)):
        
        if matchings[i][0] == i:
            
            newlst.append(matchings[i][1])
        
        else:
            for j in range(n_clusters):
                if matchings[j][0] == i:
                    newlst.append(matchings[j][1])
    
    for i in range(len(newlst)):
        
        newlst[i] = lst[newlst[i]]
        
    return newlst

def cluster_pref(cluster1, cluster2):
    
    cluster_vec_1 = np.asarray(cluster1[0:-1])
    cluster_vec_2 = np.asarray(cluster2[0:-1])
    
    distance = np.linalg.norm(cluster_vec_1 - cluster_vec_2)
    
    return distance

def check_matchings(num, matchings, right = True):
    
    check = False
    index_loc = False
    
    if right:
        index = 1
    else:
        index = 0
    
    for matching in matchings:    
        
        if num == matching[index]:
            check = True
            index_loc = matchings.index(matching)
            break
        
        else:
            continue
        
    return [check,index_loc]

def GaleShapleyAlgo(clusters_over_time,demographic_dfs, years,n_clusters):

    for i in range(len(clusters_over_time)-1):
        
        year = years[i+1]
        
        matchings = []
        
        prev_clusters = clusters_over_time[i]
        post_clusters = clusters_over_time[i+1]
        
        while len(matchings) <n_clusters:
            
            for j in range(n_clusters):
                
                if check_matchings(j,matchings,False)[0]:
                    
                    continue
                
                else:
                    
                    cluster1 = prev_clusters[j]
                    
                    preferences = []
                    
                    for k in range(n_clusters):
                        
                        cluster2 = post_clusters[k]
                        
                        preferences.append(cluster_pref(cluster1, cluster2))
                        
                    order_pref, preferences = order_min(preferences)
                    pref_index = order_pref[0]
                    
                    if check_matchings(pref_index,matchings)[0]:
                        
                        for l in range(len(order_pref)):
                            
                            pref_index = order_pref[l]
                            pref = preferences[order_pref[l]]
                            
                            if check_matchings(pref_index, matchings)[0]:
                                
                                alt_index = check_matchings(pref_index, matchings)[1]
                                alt_matching = matchings[alt_index]
                                
                                if alt_matching[0] == j:
                                    
                                    break
                                
                                else:
                                
                                    alt_cluster = prev_clusters[alt_matching[0]]
                                    alt_pref = cluster_pref(alt_cluster,post_clusters[pref_index])
                                    
                                    if pref<alt_pref:
                                        
                                        matchings.pop(alt_index)
                                        matchings.append((j,pref_index))
                                        break
                                        
                                    else:
                                        print("YEAR: " + str(year) + ". Does not prefer new match for", j)
                                        continue
                                
                            else:
                                
                                matchings.append((j,pref_index))
                    else:
                        
                        matchings.append((j,pref_index))
                        
                    
        clusters_over_time[i+1] = swapPositions(matchings, clusters_over_time[i+1], n_clusters)
        
        match_dict = {}
        for j in range(n_clusters):
            match_dict[matchings[j][1]] = matchings[j][0]
            
        for j in range(len(demographic_dfs[i+1])):
            temp = match_dict[demographic_dfs[i+1]['Cluster Position'].iloc[j]]
            demographic_dfs[i+1]['Cluster Position'].iloc[j] = temp
            
        demographic_dfs[i+1].to_csv('Demographic Clusters/demographics_' + str(years[i+1]) + '.csv')
    
    return demographic_dfs, clusters_over_time

def plotData(feature,demographic_dfs,clusters_over_time, years, n_clusters):

    data_for_plot = np.zeros(shape = (len(years),n_clusters+1))
    data_for_total = []
    
    for i in range(len(years)):
        
        data_for_total.append(np.dot(demographic_dfs[i][feature].to_numpy(),demographic_dfs[i]['# Student Enrollment'].to_numpy())/sum(demographic_dfs[i]['# Student Enrollment'].to_numpy()))
    
        for j in range(n_clusters):
            
            data_for_plot[i,j] = clusters_over_time[i][j][feature]
    
    data_for_plot[:,n_clusters] = data_for_total
    
    
    data_for_plot = pd.DataFrame(data_for_plot, index = years, columns = list(range(n_clusters)) + ['Total'])
    
    data_for_plot.plot()
    plt.title(feature + " Over Time")
    plt.grid()
    plt.xlabel("Year")
    plt.ylabel("Percentage")
    plt.show()
    
    return data_for_plot

def summaryStats(cluster_indexnum, clusters_over_time, years):
    print('AVERAGES OF CLUSTER: ' + str(cluster_indexnum))
    print("\n")
    for i in range(len(years)):
        
        print("YEAR: ", years[i])
        print(clusters_over_time[i][cluster_indexnum])
        print('\n')