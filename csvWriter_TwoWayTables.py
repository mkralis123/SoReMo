import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

n_clusters = 4

folder = "ISBE_ReportCards/"


years = [2015,2016,2017,2018,2019,2020]
clusters_over_time = []
kwaytables_over_time = []

field_names = ['School Name',
               '% Student Enrollment - White',
               '% Student Enrollment - Black or African American',
               '% Student Enrollment - Hispanic or Latino',
               '% Student Enrollment - Asian',
               '% Student Enrollment - Low Income',
               'Student Attendance Rate',
               'High School Dropout Rate - Total',
               'High School 4-Year Graduation Rate - Total',
               '% Graduates enrolled in a Postsecondary Institution within 12 months',
               '# Student Enrollment']

fields = field_names[0:-1]


for year in years:
    
    
    if year > 2017:
        
        df = pd.read_csv(folder + "ISBE_" + str(year) + ".csv", sep = ",", low_memory = False)
        
        df = df[df['School Type']=='HIGH SCHOOL']
        df = df[df['District'] == 'City of Chicago SD 299']
        df = df.filter(field_names)
        
    
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
        
        
    X = np.delete(df.values, [0,1,2,3,4,5,10], axis = 1)
    X = X.astype(float)
    X[np.isnan(X)] = 0
    
    clusters = KMeans(n_clusters = n_clusters).fit(X)
    labels = list(clusters.labels_)
    
    df['Cluster Position'] = labels
    
    
    df = df.fillna(0)
    
    table = np.zeros((4,n_clusters))
    
    for j in range(n_clusters):
        
        temp = df[df['Cluster Position']==j]
        
        for i in range(4):
            
            if i == 0:
                table[i,j] = int(np.dot(temp['% Student Enrollment - White'].to_numpy()/100,temp['# Student Enrollment'].to_numpy()))
                
            elif i == 1:
                table[i,j] = int(np.dot(temp['% Student Enrollment - Black or African American'].to_numpy()/100,temp['# Student Enrollment'].to_numpy()))
                
            elif i == 2:
                table[i,j] = int(np.dot(temp['% Student Enrollment - Hispanic or Latino'].to_numpy()/100,temp['# Student Enrollment'].to_numpy()))
            
            elif i == 3:
                table[i,j] = int(np.dot(temp['% Student Enrollment - Asian'].to_numpy()/100,temp['# Student Enrollment'].to_numpy()))
    
    table = pd.DataFrame(table, columns = list(range(n_clusters)), index = ['White', 'Black or African American', 'Hispanic or Latino', 'Asian'])
    kwaytables_over_time.append(table)
    
    table.to_csv("AlgStatsData/" + str(year) + "TwoWayTable.csv")
    
    cluster_means = []
    
    for i in range(n_clusters):
    
        current_df = df[df['Cluster Position']==i]
        
        means = []
        
        for j in range(len(fields)-1):
            
            total_in_cluster = np.dot(current_df[fields[j+1]],current_df['# Student Enrollment'])
            
            means.append(total_in_cluster/sum(current_df['# Student Enrollment']))
            
        means.append(i)
        cluster_df = pd.Series(data = means, index = fields[1:]+['Cluster Position'], dtype = float)
        
        cluster_means.append(cluster_df)
        cluster_df.to_csv("AlgStatsData/SummaryStats/" + str(year) + "Cluster" + str(i) + "SummaryStats.csv")
        
    clusters_over_time.append(cluster_means)
    
    