import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', header=0)
df["date"] = pd.to_datetime(df["date"])
df=df.set_index('date')
# Clean data
df = df[(df['value']>=(df['value'].quantile(0.025)))&
        (df['value']<=(df['value'].quantile(0.975)))
        ]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots()
    sns.lineplot(df, legend=False)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
  

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
        
    df_bar = df.copy()

    df_bar['Years'] = [d.year for d in df_bar.index.date]
    df_bar['Months'] = [d.strftime('%b') for d in df_bar.index.date]
    #df_bar['Years'] = pd.to_datetime(df_bar['Years'], format='%Y')

    df_bar=pd.DataFrame(df_bar.groupby(['Years','Months'],sort=False)['value'].mean().round().astype(int))
    df_bar=df_bar.rename(columns={'value':'m_views'})
    df_bar=df_bar.reset_index()
    df_bar=df_bar.fillna(0) 
    # Draw bar plot
    fig,axes = plt.subplots(1,1)
    sns.barplot(df_bar, x='Years', y='m_views',hue='Months', palette='bright',orient='v')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Mean Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig,axes = plt.subplots()
    #df_box1=pd.DataFrame(df_box.groupby(['year'],sort=False)['value'].mean().round().astype(int))
    sns.boxplot(df_box, x='year', y='value', palette='bright')
    axes[0].set_xlabel('Years')
    axes[0].set_ylabel('Views')
    axes[0].set_title('Year-wise boxplot (trend)')

    
    #df_box2=pd.DataFrame(df_box.groupby(['month'],sort=False)['value'].mean().round().astype(int))
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(df_box, x='month', y='value', palette='bright', order=month_order, ax=axes[1])
    axes[1].set_xlabel('Months')
    axes[1].set_ylabel('Views')
    axes[1].set_title('Month-wise boxplot (trend)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
