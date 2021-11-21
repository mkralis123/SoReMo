import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas

n_clusters = 4

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


colors = ['r','g','b','y','m','c','k','w']

chicri_map = chicri_geo.plot(figsize=(30,30), edgecolor='k', facecolor = 'b', alpha=0.25, linewidth=2) 
chicri_geo.apply(lambda x: chicri_map.annotate(text=x.community, xy=x.geometry.centroid.coords[0], ha='center', size=16),axis=1);
for i in range(n_clusters):
    gdfs[i].plot(figsize=(30,30),ax=chicri_map, markersize=500, color=colors[i], alpha=1)
chicri_map.set_axis_off()