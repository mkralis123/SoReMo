import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

n_clusters = 5

folder = "ISBE_ReportCards/"


years = [2019,2020]
clusters_over_time = []

for year in years:
    
    df = pd.read_csv(folder + "ISBE_" + str(year) + ".csv", sep = ",", low_memory = False)
    
    df = df.dropna(subset = ['School Name'])
    df = df[df['School Type']=='HIGH SCHOOL']
    df = df[df['District'] == 'City of Chicago SD 299']
    
    
    demographic_df = df.filter(['School Name',
                                '% Student Enrollment - White',
                                '% Student Enrollment - Black or African American',
                                '% Student Enrollment - Hispanic or Latino',
                                '% Student Enrollment - Asian',
                                '% Student Enrollment - Low Income',
                                'Student Attendance Rate',
                                'High School Dropout Rate - Total',
                                'High School 4-Year Graduation Rate - Total',
                                '% Graduates enrolled in a Postsecondary Institution within 12 months',
                                'Chronic Absenteeism'])
    
    X = np.delete(demographic_df.values, [0,6,7,8,9,10], axis = 1)
    X = X.astype(float)
    X[np.isnan(X)] = 0
    
    clusters = KMeans(n_clusters = n_clusters).fit(X)
    labels = list(clusters.labels_)
    
    demographic_df['Cluster Position'] = labels
    df['Cluster Position'] = labels
    
    
    cluster_means = []
    
    for i in range(n_clusters):
        
        # print('AVERAGES OF CLUSTER: ' + str(i+1) )
        # print(round(demographic_df[demographic_df['Cluster Position']==i].mean(),2))
        # print('\n')
        
        cluster_means.append(demographic_df[demographic_df['Cluster Position']==i].mean())
        
        
    clusters_over_time.append(cluster_means)


##############GALE SHAPLEY ALGORITHM##############


def swapPositions(lst, pos1, pos2):
     
    lst[pos1], lst[pos2] = lst[pos2], lst[pos1]
    return lst

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

for i in range(len(clusters_over_time)-1):
    
    matchings = []
    
    prev_clusters = clusters_over_time[i]
    post_clusters = clusters_over_time[i+1]
    
    matched = False    
    
    while len(matchings) <5:
        
        for j in range(n_clusters):
            
            cluster1 = prev_clusters[j]
            
            preferences = []
            
            for k in range(n_clusters):
                
                cluster2 = post_clusters[k]
                
                preferences.append(cluster_pref(cluster1, cluster2))
                
            
            pref = min(preferences)
            pref_index = preferences.index(pref)
            
            if check_matchings(pref_index, matchings)[0]:
                
                alt_matching = check_matchings(pref_index, matchings)[1]
                
                alt_cluster = prev_clusters[alt_matching]
                alt_pref = cluster_pref(alt_cluster,post_clusters[pref_index])
                
                if pref<alt_pref:
                    
                    matchings.pop(alt_matching)
                    matchings.append((j,pref_index))
                    
                else:
                    continue
                
            else:
                
                matchings.append((j,pref_index))
                
    swapped = []
    for matching in matchings:
        
        if matching[0]==matching[1]:
            swapped.append(matching[0])
            continue
        
        else:
            
            left = matching[0]
            right = matching[1]
            
            if left in swapped:
                continue
            
            else:
                clusters_over_time[i+1] = swapPositions(clusters_over_time[i+1], left, right)
                swapped.append(left)
                swapped.append(right)
        
        
#################FOR PLOTS##################
cluster_indexnum = 3
feature = '% Student Enrollment - Low Income'

data_for_plot = []

for i in range(len(years)):
    
    data_for_plot.append(clusters_over_time[i][cluster_indexnum][feature])
    
fig, ax = plt.subplots()
ax.plot(years, data_for_plot)
ax.ticklabel_format(useOffset=False)
plt.title(feature + " Over Time in Cluster " + str(cluster_indexnum))
plt.xlabel("Year")
plt.ylabel("Percentage")
plt.show()

print('AVERAGES OF CLUSTER: ' + str(cluster_indexnum) )
print(clusters_over_time[0][cluster_indexnum])
print('\n')


# df = df.filter(['School Name',
#                 '# Student Enrollment', 
#                 '% Student Enrollment - White',
#                 '% Student Enrollment - Black or African American',
#                 '% Student Enrollment - Hispanic or Latino',
#                 '% Student Enrollment - Asian'
#                 '% Student Enrollment - Native Hawaiian or Other Pacific Islander',
#                 '% Student Enrollment - American Indian or Alaska Native',
#                 '% Student Enrollment - Children with Disabilities',
#                 '% Student Enrollment - Low Income',
#                 '% Student Enrollment - Homeless',
#                 'Student Attendance Rate',
#                 'Student Mobility Rate',
#                 'Student Mobility Rate - Male',
#                 'Student Mobility Rate - Female',
#                 'Student Mobility Rate - White',
#                 'Student Mobility Rate - Black or African American',
#                 'Student Mobility Rate - Hispanic or Latino',
#                 'Student Mobility Rate - Asian',
#                 'Student Mobility Rate - Native Hawaiian or Other Pacific Islander',
#                 'Student Mobility Rate - American Indian or Alaska Native',
#                 'Student Mobility Rate - Low Income',
#                 'High School Dropout Rate - Total',
#                 'High School Dropout Rate - Male',
#                 'High School Dropout Rate - Female',
#                 'High School Dropout Rate - White',
#                 'High School Dropout Rate - Black or African American',
#                 'High School Dropout Rate - Hispanic or Latino',
#                 'High School Dropout Rate - Asian',
#                 'High School Dropout Rate - Native Hawaiian or Other Pacific Islander',
#                 'High School Dropout Rate - American Indian or Alaska Native',
#                 'High School Dropout Rate - Low Income',
#                 'High School 4-Year Graduation Rate - Total',
#                 'High School 4-Year Graduation Rate - Male',
#                 'High School 4-Year Graduation Rate - Female',
#                 'High School 4-Year Graduation Rate - White',
#                 'High School 4-Year Graduation Rate - Black or African American',
#                 'High School 4-Year Graduation Rate - Hispanic or Latino',
#                 'High School 4-Year Graduation Rate - Asian',
#                 'High School 4-Year Graduation Rate - Native Hawaiian or Other Pacific Islander',
#                 'High School 4-Year Graduation Rate - American Indian or Alaska Native',
#                 'High School 4-Year Graduation Rate - Low Income',
#                 'High School 4-Year Graduation Rate - Homeless',
#                 'Avg Class Size - High School',
#                 '% Graduates enrolled in a Postsecondary Institution within 12 months',
#                 '% Graduates enrolled in a Postsecondary Institution within 12 months - Public Institition',
#                 '% Graduates enrolled in a Postsecondary Institution within 12 months - Private Institution',
#                 '% Graduates enrolled in a Postsecondary Institution within 12 months - Four-year Institution',
#                 '% Graduates enrolled in a Postsecondary Institution within 12 months - Two-year Institution',
#                 '% Graduates enrolled in a Postsecondary Institution within 12 months - Trade/Vocational School',
#                 '% Graduates enrolled in a Postsecondary Institution within 16 months',
#                 '% Graduates enrolled in a Postsecondary Institution within 16 months - Public Institition',
#                 '% Graduates enrolled in a Postsecondary Institution within 16 months - Private Institution',
#                 '% Graduates enrolled in a Postsecondary Institution within 16 months - Four-year Institution',
#                 '% Graduates enrolled in a Postsecondary Institution within 16 months - Two-year Institution',
#                 '% Graduates enrolled in a Postsecondary Institution within 16 months - Trade/Vocational School',
#                 'Chronic Absenteeism',
#                 'Chronic Absenteeism - Male',
#                 'Chronic Absenteeism - Female',
#                 'Chronic Absenteeism - White',
#                 'Chronic Absenteeism - Black or African American',
#                 'Chronic Absenteeism - Hispanic or Latino',
#                 'Chronic Absenteeism - Asian',
#                 'Chronic Absenteeism - Native Hawaiian or Other Pacific Islander',
#                 'Chronic Absenteeism - American Indian or Alaska Native',
#                 'Chronic Absenteeism - Low Income'])