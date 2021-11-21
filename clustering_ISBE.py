import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import geopandas

n_clusters = 5

folder = "ISBE_ReportCards/"


years = [2015,2016,2017,2018,2019,2020]
clusters_over_time = []

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
    
    demographic_df.to_csv("Demographic Clusters/demographics_" + str(year) + ".csv")


##############GALE SHAPLEY ALGORITHM##############

def order_min(array):
    
    index = dict(zip(array,np.arange(0,len(array))))
    rev_index = dict(zip(np.arange(0,len(array)),array))
    array.sort()
    
    order_index = []
    new_array = list(rev_index.values())
    
    for i in range(len(array)):
        
        order_index.append(index[array[i]])
    
    return order_index,new_array


def swapPositions(matchings, lst):
     
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

for i in range(len(clusters_over_time)-1):
    
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
                
    clusters_over_time[i+1] = swapPositions(matchings, clusters_over_time[i+1])
        
        
#################FOR PLOTS##################
cluster_indexnum = 0
feature = '% Student Enrollment - Low Income'

data_for_plot = []

for i in range(len(years)):
    
    data_for_plot.append(clusters_over_time[i][cluster_indexnum][feature])
    
fig, ax = plt.subplots()
ax.plot(years, data_for_plot)
ax.ticklabel_format(useOffset=False)
plt.title(feature + " Over Time in Cluster " + str(cluster_indexnum))
plt.grid()
plt.xlabel("Year")
plt.ylabel("Percentage")
plt.show()


print('AVERAGES OF CLUSTER: ' + str(cluster_indexnum))
print("\n")
for i in range(len(years)):
    
    print("YEAR: ", years[i])
    print(clusters_over_time[i][cluster_indexnum])
    print('\n')
    
    


##################################DISPLAY GEOMAP####################################
namesDict = {'Air Force Acad High School': 'AIR FORCE HS',
'Alcott College Prep':'ALCOTT HS',
'Amundsen High School': 'AMUNDSEN HS',
'Austin College and Career Academy High School': 'AUSTIN CCA HS',
'Back of The Yards IB HS': 'BACK OF THE YARDS HS',
'Bogan High School': 'BOGAN HS',
'Bowen High School': 'BOWEN HS',
'Bronzeville Scholastic HS': 'BRONZEVILLE HS',
'Brooks College Prep Academy HS': 'BROOKS HS',
'Carver Military Academy HS': 'CARVER MILITARY HS',
'Chicago Academy High School':'CHICAGO ACADEMY HS',
'Chicago Excel Academy HS':'CAMELOT - EXCEL HS',
'Chicago HS for Agricult Sciences':'CHICAGO AGRICULTURE HS',
'Chicago HS for the Arts': 'CHIARTS HS',
'Chicago Military Academy HS': 'CHICAGO MILITARY HS',
'Chicago Technology Academy HS': 'CHICAGO TECH HS',
'Chicago Vocational Career Acad HS': 'CHICAGO VOCATIONAL HS',
'Clark Acad Prep Magnet High Schl': 'CLARK HS',
'Clemente Community Academy HS': 'CLEMENTE HS',
'Collins Academy High School':'COLLINS HS',
'Corliss High School':'CORLISS HS',
'Crane Medical Prep HS':'CRANE MEDICAL HS',
'Curie Metropolitan High School':'CURIE HS',
'Devry Advantage Academy High Schl':'DEVRY HS',
'Disney II Magnet HS':'DISNEY II HS',
'Douglass Academy High School':'DOUGLASS HS',
'Dunbar Vocational Career Acad HS':'DUNBAR HS',
'Englewood STEM High School':'ENGLEWOOD STEM HS',
'Farragut Career Academy HS':'FARRAGUT HS',
'Fenger Academy High School':'FENGER HS',
'Foreman High School':'FOREMAN HS',
'Gage Park High School':'GAGE PARK HS',
'Goode STEM Academy HS':'GOODE HS',
'Hancock College Preparatory HS':'HANCOCK HS',
'Harlan Community Academy HS':'HARLAN HS',
'Harper High School':'HARPER HS',
'Hirsch Metropolitan High School':'HIRSCH HS',
'Hubbard High School':'HUBBARD HS',
'Hyde Park Academy High School':'HYDE PARK HS',
'Infinity Math  Science & Tech HS':'INFINITY HS',
'Jones College Prep High School':'JONES HS',
'Juarez Community Academy HS':'JUAREZ HS',
'Julian High School':'JULIAN HS',
'Kelvyn Park High School':'KELVYN PARK HS',
'Kennedy High School':'KENNEDY HS',
'Kenwood Academy High School':'KENWOOD HS',
'King College Prep High School':'KING HS',
'Lake View High School':'LAKE VIEW HS',
'Lane Technical High School':'LANE TECH HS',
'Lincoln Park High School':'LINCOLN PARK HS',
'Lindblom Math & Science Acad HS':'LINDBLOM HS',
'Manley Career Academy High School':'MANLEY HS',
'Marshall Metropolitan High School':'MARSHALL HS',
'Mather High School':'MATHER HS',
'Morgan Park High School':'MORGAN PARK HS',
'Multicultural Acad of Scholarshp HS':'MULTICULTURAL HS',
'North-Grand High School':'NORTH-GRAND HS',
'Northside College Preparatory Hs':'NORTHSIDE PREP HS',
'Ogden Int High School':'OGDEN HS',
'Orr Academy High School':'ORR HS',
'Payton College Preparatory HS':'PAYTON HS',
'Phillips Academy High School':'PHILLIPS HS',
'Phoenix Military Academy HS':'PHOENIX MILITARY HS',
'Prosser Career Academy HS':'PROSSER HS',
'Raby High School':'RABY HS',
'Richards Career Academy HS':'RICHARDS HS',
'Rickover Naval Academy High Schl':'RICKOVER MILITARY HS',
'Roosevelt High School':'ROOSEVELT HS',
'School of Social Justice HS':'SOCIAL JUSTICE HS',
'Schurz High School':'SCHURZ HS',
'Senn High School':'SENN HS',
'Simeon Career Academy High School':'SIMEON HS',
'Solorio Academy High School':'SOLORIO HS',
'South Shore Intl Col Prep HS':'SOUTH SHORE INTL HS',
'Spry Community Links High School':'SPRY HS',
'Steinmetz College Prep HS':'STEINMETZ HS',
'Sullivan High School':'SULLIVAN HS',
'Taft High School':'TAFT HS',
'Thomas Kelly College Preparatory':'KELLY HS',
'Tilden Career Communty Academy HS':'TILDEN HS',
'Uplift Community High School':'UPLIFT HS',
'Von Steuben Metro Science HS':'VON STEUBEN HS',
'Walter Henri Dyett High School for the Arts':'DYETT ARTS HS',
'Washington G High School':'WASHINGTON HS',
'Wells Community Academy HS':'WELLS HS',
'Westinghouse High School':'WESTINGHOUSE HS',
'Williams Medical Prep High Sch':'WILLIAMS HS',
'World Language High School':'WORLD LANGUAGE HS',
'Young Magnet High School': 'YOUNG HS'}

chicri_geo = geopandas.read_file('geo_export_33ca7ae0-c469-46ed-84da-cc7587ccbfe6.shp')

df = pd.read_csv('Chicago_Public_Schools_-_School_Locations_SY1920.csv')
df = df[df['Grade_Cat'] == 'HS']


cluster_df = pd.read_csv('Demographic Clusters/demographics_2020.csv')
cluster_df = cluster_df.sort_values(by = ['School Name'])


for i in range(len(cluster_df)):
    
    cluster_df['School Name'].iloc[i] = namesDict[cluster_df['School Name'].iloc[i]]


new_df = pd.merge(cluster_df, df, how = 'inner', left_on = 'School Name', right_on = 'School_Nm')

gdfs = []
for i in range(n_clusters):
    temp = new_df[new_df['Cluster Position']==i]
    
    gdfs.append(geopandas.GeoDataFrame(temp, geometry=geopandas.points_from_xy(temp.X, temp.Y)))


colors = ['r','g','b','k','m','y','c','w']

chicri_map = chicri_geo.plot(figsize=(30,30), edgecolor='k', facecolor = 'y', alpha=0.1, linewidth=2) 
chicri_geo.apply(lambda x: chicri_map.annotate(text=x.community, xy=x.geometry.centroid.coords[0], ha='center', size=16),axis=1);
for i in range(n_clusters):
    gdfs[i].plot(figsize=(30,30),ax=chicri_map, markersize=1000, color=colors[i], alpha=1)
chicri_map.set_axis_off()














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