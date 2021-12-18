import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas


def mapClusters(n_clusters):
    
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
    
    df = pd.read_csv('CPSSchoolLocations2020.csv')
    df = df[df['Grade_Cat'] == 'HS']
    
    
    cluster_df = pd.read_csv('Demographic Clusters/demographics_2020.csv')
    cluster_df = cluster_df.sort_values(by = ['School Name'])
    
    
    for i in range(len(cluster_df)):
        
        cluster_df['School Name'].iloc[i] = namesDict[cluster_df['School Name'].iloc[i]]
    
    
    new_df = pd.merge(cluster_df, df, how = 'inner', left_on = 'School Name', right_on = 'School_Nm')
    gdf = geopandas.GeoDataFrame(new_df, geometry=geopandas.points_from_xy(new_df.X, new_df.Y))
    
    gdfs = []
    for i in range(n_clusters):
        temp = new_df[new_df['Cluster Position']==i]
        
        gdfs.append(geopandas.GeoDataFrame(temp, geometry=geopandas.points_from_xy(temp.X, temp.Y)))
    
    
    colors = ['blue','orange','green','red','magenta','brown','pink','grey','yellow']
    
    gdf_colors = []
    for i in range(len(gdf)):
        gdf_colors.append(colors[gdf['Cluster Position'].iloc[i]])

    gdf['Colors'] = gdf_colors
    
    chicri_map = chicri_geo.plot(figsize=(10,10), edgecolor='b', facecolor = 'k', alpha=0.1, linewidth=1) 
    chicri_geo.apply(lambda x: chicri_map.annotate(text=x.community, xy=x.geometry.centroid.coords[0], ha='center', size=6),axis=1);
    gdf.plot(figsize=(10,10),ax=chicri_map, column = 'Cluster Position', 
             categorical = True,legend = True,color = gdf['Colors'], markersize=100, alpha=1)
    chicri_map.set_title("Clusters over Map of Chicago c. 2020")
    


#'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 
#'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 
#'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 
#'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 
#'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 
#'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1',
# 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 
#'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 
#'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 
#'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 
#'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 
#'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 
#'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 
#'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 
#'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 
#'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 
#'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 
#'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight',
# 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 
#'winter_r'