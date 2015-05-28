from __future__ import print_function
import pylab
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon
import matplotlib.patches as mpatches
import locale

# helps formatting numbers to currency values
locale.setlocale( locale.LC_ALL, '' )

# Lambert Conformal map of lower 48 states
m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

# draw state boundaries
# data from U.S Census Bureau
# http://www.census.gov/geo/www/cob/st2000.html
shp_info = m.readshapefile('st99_d00','states',drawbounds=True)

# medicare spending by state
stateSpending = {'Mississippi': 0.96, 'Oklahoma': 0.93, 'Delaware': 1, 
'Minnesota': 0.9,  'Illinois': 1.01,  'Arkansas': 0.99,  'New Mexico': 0.87,
'Indiana': 1.02,'Texas': 1.04,'Louisiana': 1.03, 'Idaho': 0.95, 'Wyoming': 0.93, 
'Tennessee': 0.99, 'Arizona': 0.93, 'Iowa': 0.92, 'Michigan': 0.97, 
'Kansas': 0.95, 'Utah': 1, 'Virginia': 0.96, 'Oregon': 0.89, 'Connecticut': 1, 
'Montana': 0.88, 'California': 0.98, 'Massachusetts': 1.03, 
'West Virginia': 0.96, 'South Carolina': 0.98, 'New Hampshire': 1.01, 
'Wisconsin': 0.94, 'Vermont': 1.01, 'Georgia': 0.96, 'North Dakota': 0.92, 
'Pennsylvania': 1.01, 'Florida': 1.04, 'Alaska': 0.92, 'Kentucky': 0.97, 
'Hawaii': 0.87, 'Nebraska': 0.98, 'Missouri': 0.96, 'Ohio': 1.02, 
'Alabama': 0.98, 'New York': 0.95, 'South Dakota': 0.92, 'Colorado': 0.96, 
'New Jersey': 1.07, 'Washington': 0.92, 'North Carolina': 0.94, 
'District of Columbia': 1, 'Nevada': 1.02, 'Maine': 0.95, 'Rhode Island': 1.01,
'Maryland': 1
}

# choose a color for each state based on spending
colors={}
stateNames=[]
cmap = plt.cm.RdYlBu # use 'Red Yellow Blue' colormap
vmin = min(stateSpending.itervalues()) # min spending value
vmax = max(stateSpending.itervalues()) # max spending value

# iterate over map shape dictionary skipping DC and PR    
for shapeDict in m.states_info:
    stateName = shapeDict['NAME']
    if stateName not in ['District of Columbia','Puerto Rico']: 
        stateSpendingValue = stateSpending[stateName]
        # calling colormap with value between 0 and 1 returns
        # rgba value.  red = high, blue = low
        colors[stateName] = cmap(1-((stateSpendingValue-vmin)/(vmax-vmin)))[:3]
    stateNames.append(stateName)
    
# get current axes instance
ax = plt.gca()

# cycle through state names, color each one.
for nshape, seg in enumerate(m.states):
    # skip DC and Puerto Rico.
    if stateNames[nshape] not in ['District of Columbia','Puerto Rico']:
        color = rgb2hex(colors[stateNames[nshape]]) 
        poly = Polygon(seg, facecolor = color , edgecolor = color)
        ax.add_patch(poly)
        
# draw meridians and parallels.
m.drawparallels(np.arange(25,65,20),labels=[1,0,0,0])
m.drawmeridians(np.arange(-120,-40,20),labels=[0,0,0,1])

plt.title('Relative Medicare Hospital Spending per Patient by State - 2013')

# adding a legend as patches
patchList = []
vDiff = vmax - vmin
avgUSSpending = 11195

for num in range(0,8):
    patch = mpatches.Patch(facecolor = cmap((vmax - (vmin + vDiff * num / 7)) / vDiff), 
            label = str(locale.currency(round((vmin + vDiff * num / 7) * avgUSSpending , 0), 
            grouping = True))[:-3], 
            edgecolor = 'black')    
    patchList.append(patch)

plt.legend(handles=patchList, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


plt.show()
pylab.savefig('StateSpending.png')