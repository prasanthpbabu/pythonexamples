import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker 
import matplotlib.animation as animation 
from IPython.display import HTML
from numpngw import AnimatedPNGWriter

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

def draw_barchart(year):
    
    #fig, ax = plt.subplots(figsize=(15, 8))
    ax = fig.add_subplot(111)
    dff = (df[df['Year'].eq(year)].sort_values(by='Counts', ascending=True).head(5)) 
    ax.clear()
    cmap = get_cmap(20)
    #group_lk = df.set_index('Acct_Type')['Year'].to_dict() 
    #dff = dff[::-1]
    ax.barh(dff['Acct_Type'], dff['Counts'], color=[cmap(i) for i in range(20)]) 
    dx = dff['Counts'].max() / 200
    #plt.show()
    for i, (Counts,Acct_Type) in enumerate(zip(dff['Counts'], dff['Acct_Type'])):
        ax.text(Counts-dx, i,   Acct_Type,  size=14, weight=600,  ha='right',va='bottom')  
        #ax.text(value-dx, i-.25, group_lk[name], size=10, color='#444444', ha='right', va='baseline') 
        ax.text(Counts-dx, i,     Counts,           size=14, ha='left',  va='center') 
        # Add year right middle portion of canvas 
    ax.text(1, 0.4, year, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800) 
    ax.text(0, 1.06, 'Account Type Counts', transform=ax.transAxes, size=12, color='#777777') 
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}')) 
    ax.xaxis.set_ticks_position('top') 
    ax.tick_params(axis='x', colors='#777777', labelsize=12) 
    ax.set_yticks([]) 
    ax.margins(0, 0.01) 
    ax.grid(which='major', axis='x', linestyle='-') 
    ax.set_axisbelow(True) 
    ax.text(0, 1.12, 'The most demanding TDA account types from 2000 to 2018', transform=ax.transAxes, size=20, weight=600, ha='left') 
    ax.text(1, 0, 'by @prasanth Panikkassery Babu; credit @Python', transform=ax.transAxes, ha='right',color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white')) 
    plt.box(False) 
    #plt.show()

New_Acct_By_year = 0
for chunk in (pd.read_csv('acct_data.csv',error_bad_lines=False,chunksize=100000)):
    chunk['acct_open_year'] = pd.DatetimeIndex(chunk['acct_open_ts']).year
    #print(chunk)
    New_Acct_By_year += chunk.groupby(['acct_open_year','bos_acct_type_cd']).size()
df  = pd.DataFrame(New_Acct_By_year)
df = df.reset_index()
df.columns = ['Year','Acct_Type','Counts']
df = df.fillna(0)
df.Year = df.Year.astype(int)
df.Counts = df.Counts.astype(int)
df = df[df['Counts']!=0]
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_yticks([]) 
#writer = AnimatedPNGWriter(fps=2)
animator = animation.FuncAnimation(fig,draw_barchart, frames=range(2000, 2019),repeat=True) 
#animator.save('Top_Acct_Types.png', dpi=50, writer=writer)
plt.show()  

