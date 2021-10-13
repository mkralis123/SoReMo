import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

n_clusters = 5

folder = "ISBE_ReportCards/"

df = pd.read_csv(folder + "ISBE_2020.csv", sep = ",")

df = df.dropna(subset = ['School Name'])
df = df[df['School Type']=='HIGH SCHOOL']
df = df[df['District'] == 'City of Chicago SD 299']


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
    
    print('AVERAGES OF CLUSTER: ' + str(i+1) )
    print(round(demographic_df[demographic_df['Cluster Position']==i].mean(),2))
    print('\n')
    
    cluster_means.append(demographic_df[demographic_df['Cluster Position']==i].mean())