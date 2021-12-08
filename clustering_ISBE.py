from mappingClusters import mapClusters
from functions import GaleShapleyAlgo, clusterDemographics, plotData, summaryStats

n_clusters = 3
folder = "ISBE_ReportCards/"
years = [2015,2016,2017,2018,2019,2020]
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
feature_index = 5
cluster_indexnum = 2


#############RUN CLUSTER ALGO#####################
demographic_dfs, clusters_over_time = clusterDemographics(folder, years, field_names, n_clusters)


##############GALE SHAPLEY ALGORITHM##############
demographic_dfs,clusters_over_time = GaleShapleyAlgo(clusters_over_time, demographic_dfs, years, n_clusters)


#################FOR PLOTS########################
data_for_plot = plotData(field_names[feature_index], demographic_dfs, clusters_over_time, years, n_clusters)


################PRINT SUMMARY STATS###############    
summaryStats(cluster_indexnum, clusters_over_time, years)


###################DISPLAY GEOMAP#################
mapClusters(n_clusters)













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