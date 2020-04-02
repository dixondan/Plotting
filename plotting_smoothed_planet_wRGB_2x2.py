# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 08:05:26 2020

@author: 22631228
"""



''' plotting smoothing windows and seeing what makes sense'''



import statsmodels.api as sm
import geopandas as gpd
import os
import pandas as pd
import rasterio
import fiona
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from osgeo import gdal, ogr
from collections import OrderedDict
#import time
import itertools
import rasterio.mask
def makemydir(newfile):
  try:
    os.makedirs(newfile)
  except OSError:
    pass
  os.chdir(newfile)

import numpy as np
import scipy
import warnings
import functools

warnings.filterwarnings("ignore")
from rasterio.enums import Resampling



pixels = [("2110_ID", "HF"),
          ("2077_ID", "HF"),
          ("2109_ID", "HF"),
          ("2008_ID", "HF"),
          ("367_ID", "HF"),
          ("198_ID", "HF"),
          ("431_ID", "HF"),
          ("148_ID", "HF - single"),
          ("299_ID", "NF"),
          ("651_ID", "NF"),
          ("808_ID", "NF"),
          ("779_ID", "NF"),
          ("3278_ID", "HF"),  
          ("3448_ID","NF"),
          ("3496_ID","NF"),
          ("3335_ID","NF"),
          ("3091_ID","NF"), 
          ("1005_ID","HF"),
          ("654_ID","HF"),
          ("1870_ID","NF Dense"),
          ("1795_ID","NF - Buds"),
          ("3496_ID","NF - Buds"),
          ("1358_ID","NF - Buds"),
          ("1286_ID","HF - Edge"),
          ("394_ID","HF - Edge")]









'''first plots for each pixel'''
l=[]
for window in ['9','15','21','25','31','39','45','51']:
    print(window)
    f = r"D:\#DATA\ee_2020\Planet\Dandaragan\GEE_Processed\smooth\smooth{}.csv".format(window)
    d = pd.read_csv(f)
    #d = d[d.ID1.isin(list(pd.DataFrame(pixels)[0].unique()))] 
    d = d[['ID1','mean','uid']]
    d['w'] = window
    l.append(d)
df = pd.concat(l)

    
    

#
#for pixel in pixels:
#    pass
#    ID1 = pixel[0]
#    ftype = pixel[1]
#    
#    fig, ax = plt.subplots(1, figsize=(12,6))
#    ax.grid(True)
#    df1 = df[df.ID1 == ID1]
#    ax.axvline(72, color = 'black', lw = 4)
#    for window in windows: 
#        w = window[0]
#        c = window[1]
#        dft = df1[df1.w == w]
#        dft['year'] = dft['uid'].str.split("-").str[0]
#        dft['j'] = dft['uid'].str.split("-").str[-1].str.zfill(3)
#        dft['date'] = pd.to_datetime(dft['year'] + dft['j'], format='%Y%j')
#        dft['ms'] = dft.date.astype('int64')
#        dft['j'] = dft['j'].astype(int)
#        dft = dft[dft.j < 140]
#        x = np.array(dft.j)
#        y = np.array(dft['mean'])
#        ax.plot(x, y, color=c, lw = 3 ,label=  w)
#        plt.title(ID1 + " " + ftype)
#        ax.set_facecolor('grey')
#        plt.ylim(0.4, 0.7)
#        ax.legend(loc = 'lower left')
#        
#    plt.savefig(r"D:\#DATA\ee_2020\Planet\Dandaragan\GEE_Processed\smooth\plots\{}.png".format(pixel[0]))
#    plt.show()
#  
    
    
    
    
    



windows = [("9", "#FF0000"),
          ("15", "#FF2400"),
          ("21", "#FF4800"),
          ("25", "#FF6D00"),
          ("31", "#FF9100"),
          ("39", "#FFB600"),
          ("45", "#FFDA00"),
          ("51", "#FFFF00")]



#    
#
#pixels = ["2110_ID",
#          "2077_ID",
#          "2109_ID",
#          "2008_ID",
#          "367_ID",
#          "198_ID",
#          "431_ID",
#          "148_ID",
#          "299_ID",
#          "651_ID",
#          "808_ID",
#          "779_ID",
#          "3278_ID",  
#          "3448_ID",
#          "3496_ID",
#          "3335_ID",
#          "3091_ID", 
#          "1005_ID",
#          "654_ID",
#          "1870_ID",
#          "1795_ID",
#          "3496_ID",
#          "1358_ID",
#          "1286_ID",
#          "394_ID"]
#    

# This program will make the plot above with a cutout of the image next to it: 
# First cut out each pixel crop whatevr
    
raster = r"D:\#DATA\dandaragan\drone_images\2019\dandaragan_w_auspos_2019_13_03.tif"
#shp = r"D:\#DATA\ee_2020\Planet\template6m_32750.shp"
#shp = gpd.read_file(shp)
#shp['geometry'] = shp['geometry'].centroid
#shp['geometry'] = shp.buffer(9).envelope
#shp = shp.to_crs({'init': 'epsg:28350'})
#shp.to_file(r"D:\#DATA\ee_2020\Planet\template6m_28350_buffer.shp")
#
#shp = r"D:\#DATA\ee_2020\Planet\template6m_32750.shp"
#shp = gpd.read_file(shp)
#shp = shp.to_crs({'init': 'epsg:28350'})
#shp.to_file(r"D:\#DATA\ee_2020\Planet\template6m_28350.shp")
#shp = r"D:\#DATA\ee_2020\Planet\template6m_28350.shp"
#


shp = gpd.read_file(r"D:\#DATA\ee_2020\Planet\template6m_28350.shp")
buffer = r"D:\#DATA\ee_2020\Planet\template6m_28350_buffer.shp"

from matplotlib import pyplot
from shapely.geometry.polygon import LinearRing, Polygon

poly = Polygon([(300, 300), (300, 600), (600,600),(600,300)])
x1,y1 = poly.exterior.xy

with rasterio.open(raster) as src:
    for feat in fiona.open(buffer):
        ID1 = feat['properties']['ID1'] 
        df1 = df[df.ID1 == ID1]
        if len(df1) > 1:
            print(ID1)
            #if ID1 in pixels:
            fig, axs = plt.subplots(1,2, figsize=(12,4), dpi = 120)
            #fig = plt.figure(1, figsize=(16,8))
            coords = [feat['geometry']]
            array, out_transform  = rasterio.mask.mask(src, coords, crop = True)
            array2 = array[0:3, :,:]
            array2 = np.moveaxis(array2, 0, 2)
            axs[1].imshow(array2)            
            axs[0].grid(True)
            axs[0].axvline(72, color = 'black', lw = 4)
            for window in windows: 
                w = window[0]
                c = window[1]
                dft = df1[df1.w == w]
                dft['year'] = dft['uid'].str.split("-").str[0]
                dft['j'] = dft['uid'].str.split("-").str[-1].str.zfill(3)
                dft['date'] = pd.to_datetime(dft['year'] + dft['j'], format='%Y%j')
                dft['ms'] = dft.date.astype('int64')
                dft['j'] = dft['j'].astype(int)
                dft = dft[dft.j < 140]
                x = np.array(dft.j)
                y = np.array(dft['mean'])
                axs[0].plot(x, y, color=c, lw = 3 ,label=  w)
                axs[0].set_facecolor('grey')
                axs[0].set_ylim(0.4, 0.7)
                axs[0].legend(loc = 'lower right')
            plt.axis('off')        
            axs[1].plot(x1, y1, color='black', 
                    linewidth=3)#), zorder=2)
            #plt.text(150,130,"6 m pixel",color='orange')
            plt.savefig(r"D:\#DATA\ee_2020\Planet\Dandaragan\GEE_Processed\smooth\plots\pixel_extractions\{}.png".format(ID1))
            plt.title(ID1)    
            plt.show()
            #sys.exit()
           




with rasterio.open(raster) as src:    
    fig, axs = plt.subplots(1,2, figsize=(14,4))
    coords = [feat['geometry']]
    array, out_transform  = rasterio.mask.mask(src, coords, crop = True)
    array2 = array[0:3, :,:]
    array2 = np.moveaxis(array2, 0, 2)
    axs[1].imshow(array2)
    plt.axis('off')        
    axs[1].plot(x1, y1, color='black', 
        linewidth=3)#), zorder=2)
    #plt.text(150,130,"6 m pixel",color='orange')
    plt.savefig(r"D:\#DATA\ee_2020\Planet\Dandaragan\GEE_Processed\smooth\plots\pixel_extractions\{}.png".format(ID1))
    plt.show()    
    sys.exit()

