import pandas as pd
import numpy as np
from sklearn.cluster import KMeans


df = pd.read_csv("SY2016_2017.csv", sep = ",")

lst = ['School_ID', 
'Legacy_Unit_ID', 
'Finance_ID', 
'Summary', 
'Administrator_Title', 
'Administrator', 
'Secondary_Contact_Title',  
'Secondary_Contact', 
'City', 
'State', 
'Zip', 
'Phone', 
'Fax', 
'Website', 
'Facebook', 
'Twitter', 
'Youtube', 
'Pinterest', 
'Attendance_Boundaries', 
'Grades_Offered_All', 
'Grades_Offered', 
'Statistics_Description', 
'Demographic_Description', 
'Dress_Code', 
'PreK_School_Day', 
'Kindergarten_School_Day', 
'School_Hours', 
'Freshman_Start_End_Time', 
'After_School_Hours', 
'Earliest_Drop_Off_Time', 
'Classroom_Languages', 
'Bilingual_Services', 
'Refugee_Services', 
'Title_1_Eligible', 
'PreSchool_Inclusive', 
'Preschool_Instructional', 
'Significantly_Modified', 
'Hard_Of_Hearing', 
'Visual_Impairments', 
'Transportation_Bus', 
'Transportation_El', 
'Transportation_Metra', 
'School_Latitude', 
'School_Longitude', 
'Rating_Status', 
'Rating_Statement', 
'Classification_Description', 
'School_Year', 
'Third_Contact_Title', 
'Third_Contact_Name', 
'Fourth_Contact_Title', 
'Fourth_Contact_Name', 
'Fifth_Contact_Title', 
'Fifth_Contact_Name', 
'Sixth_Contact_Title', 
'Sixth_Contact_Name', 
'Seventh_Contact_Title', 
'Seventh_Contact_Name', 
'Network', 
'Is_GoCPS_Participant', 
'Is_GoCPS_PreK', 
'Is_GoCPS_Elementary', 
'Is_GoCPS_High_School', 
'Open_For_Enrollment_Date', 
'Closed_For_Enrollment_Date',
'School_Type',
'ADA_Accessible',
'Location']

df = df.drop(lst, axis = 1, errors = "ignore")

df = df[df['Primary_Category']=='HS'].reset_index().drop(['index'], axis = 1)


lst = ['Long_Name',
'Primary_Category',
'Is_High_School',
'Is_Middle_School',
'Is_Elementary_School',
'Is_Pre_School',
'Address',
'CPS_School_Profile',
'Student_Count_Native_American',
'Student_Count_Other_Ethnicity',
'Student_Count_Asian_Pacific_Islander',
'Student_Count_Multi',
'Student_Count_Hawaiian_Pacific_Islander',
'Student_Count_Ethnicity_Not_Available',
'Student_Count_Special_Ed',
'Student_Count_English_Learners',
'Average_ACT_School',
'Mean_ACT',
'Student_Count_Total',
'College_Enrollment_Rate_School',
'College_Enrollment_Rate_Mean',
'Graduation_Rate_School',
'Graduation_Rate_Mean',
'Overall_Rating']


races = ['Student_Count_Low_Income',
'Student_Count_Special_Ed',
'Student_Count_English_Learners',
'Student_Count_Black',
'Student_Count_Hispanic',
'Student_Count_White',
'Student_Count_Asian',
'Student_Count_Native_American',
'Student_Count_Other_Ethnicity',
'Student_Count_Asian_Pacific_Islander',
'Student_Count_Multi',
'Student_Count_Hawaiian_Pacific_Islander',
'Student_Count_Ethnicity_Not_Available']

for i in range(len(df)):
    
    for j in range(len(races)):
        
        if df['Student_Count_Total'].iloc[i] == 0:
            
            df.drop([i])
        
        else:
            
            df[races[j]].iloc[i] = df[races[j]].iloc[i]/df['Student_Count_Total'].iloc[i]


df = df.dropna(subset = ['Student_Count_Total'])
high_schools = list(df['Short_Name'])
demographic_df = df.drop(lst, axis = 1)
X = np.delete(demographic_df.values, [0], axis = 1)


n_clusters = 5
clusters = KMeans(n_clusters = n_clusters).fit(X)
labels = list(clusters.labels_)


demographic_df['Cluster Position'] = labels
df['Cluster Position'] = labels

cluster_means = []

for i in range(n_clusters):
    
    print('AVERAGES OF CLUSTER: ' + str(i+1) )
    print(df[df['Cluster Position']==i].mean())
    print('\n')
    
    cluster_means.append(df[df['Cluster Position']==i].mean())
    

df['Low Income Count'] = np.multiply(df['Student_Count_Total'].values,df['Student_Count_Low_Income'].values).astype(int)
df['High Income Count'] = df['Student_Count_Total'] - df['Low Income Count']

low_income_probabilities = []
high_income_probabilities = []

for i in range(n_clusters):
    
    low_income_probabilities.append(sum(df[df['Cluster Position'] == i]['Low Income Count']))
    high_income_probabilities.append(sum(df[df['Cluster Position'] == i]['High Income Count']))

total_low_income = sum(low_income_probabilities)
total_high_income = sum(high_income_probabilities)

print("Total Amount of Low Income Students", total_low_income)
print("Total Amount of Non-Low Income Students", total_high_income)

for i in range(n_clusters):
    
    low_income_probabilities[i] = low_income_probabilities[i]/total_low_income
    print("\nProbability for Low Income Student to be in Cluster", i+1)
    print(low_income_probabilities[i])
    
    high_income_probabilities[i] = high_income_probabilities[i]/total_high_income
    print("Probability for High Income Student to be in Cluster", i+1)
    print(high_income_probabilities[i])
    
