import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

months = 'Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec'.split()
data_path = os.path.join(os.getcwd(), 'data')


def run_regression(df, x_col, y_col):
    # create a regressor object for the columns specified of the dataframe that is passed to it
    X = df[x_col].values.reshape(-1, 1)  # values converts it into a numpy array
    Y = df[y_col].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X, Y)  # perform linear regression
    return linear_regressor
    

def predict(regressor, value, many=None):
    # make predictions for the regressor that was passed
    if not many:
        return regressor.predict(np.array([value]).reshape(1,-1))[0][0]
    else:
        return regressor.predict(value)



def read_time_series(f_path, cols, col):
    # read a csv from a filepath with columns as specified
    # Returns a dataframe with the values row = year, columns = month, cells = values
    # Retruns a dataframe with a regression of the entire frame, not including seasnoality 
    # Returns a regressor and its r squared for the whole frame
    data = pd.read_csv(f_path, header=0, names=cols)
    data = data[data[col] > 0].groupby(['year', 'month']).mean().reset_index() 

    full_regressor = run_regression(data, 'decimal', col) #get the regressor before the dataframe is pivoted
    full_regression = data[['year', 'month', 'decimal', col]].copy()
    full_regression['Best_fit'] = predict(full_regressor, np.array(full_regression['decimal']).reshape(-1,1), many=True) #get the predictions for the full frame
    full_regression_r2 = r2_score(data[col],  full_regression['Best_fit'])
    full_regression = full_regression.pivot('year', 'month', 'Best_fit') # pivot to match the data
    
    data = data.pivot(index='year', columns='month', values=col) # use only the values in "col" years are rows and months are columns

    return data, full_regression, full_regressor.coef_[0][0], full_regression_r2 


def get_monthly_regressors(df, title, full_regression, full_r2):
    # returns a dataframe with the predicted values for each month

    # remove all years that don't have recorded data
    monthly_regressors = [run_regression(df[i+1].dropna().reset_index(), 'year', i+1) for i in range(len(df.columns))]

    # get the slope of the line for each month, aka average increase
    monthly_rates = [[months[i] ,r.coef_[0][0]] for i,r in enumerate(monthly_regressors)]


    # make predictions with each regression for each month  
    preds = pd.DataFrame().reindex_like(df)
    r_2 = []
    for i, regressor in enumerate(monthly_regressors):
        preds[i+1] = (predict(regressor, np.array(df.index).reshape(-1, 1), many=True))
        # run the r_2 analysis for all years that have data in the predictions and in the recorded data
        r_2.append([months[i], r2_score(df[i+1].dropna(), preds[i+1][preds.index.isin(df[i+1].dropna().index)])])

    # BEGIN OUTPUT
    print('='*70)
    print('Analysis for: {}'.format(title))
    print('-'*70)
    print('Monthly Increase Rates')
    for m in monthly_rates:
        print(m)
    print('-'*70)
    print('Monthly R Squared')
    for m in r_2:
        print(m)
    print('-'*70)
    print('Average increase for monthly preds', sum(map(lambda x : x[1], monthly_rates) ) /len(monthly_rates))
    print('Average R Squared for monthly preds', sum(map(lambda x : x[1], r_2) ) /len(r_2))
    print('-'*70)
    print('Average increase without monthly trends', full_regression)
    print('R squared without monthly trends', full_r2)


    return preds


def run(cols:list, fname:str, col:str, title:str, historical_years=range(2000,2021,5)):
    print('Starting: {}'.format(fname.split('\\')[-1].split('.')[0]))
    # create an output folder for the results
    save_path = os.path.join(os.getcwd(), fname.split('\\')[-1].split('.')[0]+'_outputs') 

    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    # write print statements to a text file
    orig_stdout = sys.stdout
    f = open(os.path.join(save_path, 'stats.txt'), 'w')
    sys.stdout = f

    # get the data in the correct format along with the full regressions
    data, full_reg, full_regressor, full_r2 = read_time_series(fname, cols, col)
    fname = fname.split('\\')[-1].split('.')[0]
    # write stats to a text file and get the predictions in a dataframe
    preds = get_monthly_regressors(data, title, full_regressor, full_r2)

    # remove the trends from the data
    trend_removed = data - preds



    
    # write the data for 2020, if 2020 shows a reduction from the trend covid has reduced the impact
    print('-'*70)
    print('2020 recorded data')
    for i, line in enumerate(data.loc[2020]):
        print([months[i], line])
    print('-'*70)
    print('2020 predicted data')
    for i, line in enumerate(preds.loc[2020]):
        print([months[i], line])
    print('-'*70)
    print('2020 trend removed')
    for i, line in enumerate(trend_removed.loc[2020]):
        print([months[i], line])

    print('-'*70)
    print('Standard Dev of data')
    for i in range(12):
        print([months[i], data[i+1].std()])

    print('-'*70)
    print('Average of data')
    for i in range(12):
        print([months[i], data[i+1].mean()])
    print('-'*70)
    print('Standard Dev of data after trend removed')
    for i in range(12):
        print([months[i], trend_removed[i+1].std()])
    
    print('-'*70)
    print('Average of data after trend removed')
    for i in range(12):
        print([months[i], trend_removed[i+1].mean()])
    print('='*70)

    plt.rcParams["figure.figsize"] = (18.5, 10.5)
    fig, ax = plt.subplots(nrows=2,ncols=6, sharex=True, sharey=True)
    for i, ax in enumerate(ax.ravel()):
        trend_removed[i+1].hist(ax=ax)
        ax.set_title(months[i]) 
    plt.savefig(os.path.join(save_path, 'Monthly Histograms Trend Removed.png'))

    # Trends for each month
    fig, ax = plt.subplots(nrows=2,ncols=6, sharex=True, sharey=True)
    for i, ax in enumerate(ax.ravel()):
        cur_pred = preds[i+1].reset_index()
        cur = data[i+1].reset_index()
        cur_pred.plot(x='year', y=i+1, ax=ax, label=months[i] + ' predicted')
        cur.plot(x='year', y=i+1, ax=ax, label=months[i])
        ax.set_ylabel('PPM')
        ax.grid()
    plt.savefig(os.path.join(save_path, 'Monthly Regressions.png'))

    # show what the data looks like for each month, what the trends look like (regression), and what it looks like when the trend is removed
    fig, ax = plt.subplots(ncols=3)
    for year in data.index:
        data.loc[year].plot(ax=ax[0])
        preds.loc[year].plot(ax=ax[1])
        trend_removed.loc[year].plot(ax=ax[2])
    ax[0].set_title('Monthly Mean {}(ppm) by Year'.format(title.split()[0]))
    ax[1].set_title('Trends of Monthly Mean {}(ppm) by Year'.format(title.split()[0]))
    ax[2].set_title('Monthly Mean {}(ppm) Trend Removal'.format(title.split()[0]))
    for ax in ax.ravel():
        ax.set_ylabel('PPM')
        ax.grid()
    plt.savefig(os.path.join(save_path, 'Total Trends.png'))

    plt.rcParams["figure.figsize"] = (7, 5)
    # Trend Removed
    fig, ax = plt.subplots()
    # plot the standard deviations 1 - 2
    labeled = False
    for i in range(1,3):
        if not labeled:
            (trend_removed.std(axis=0)*i).plot(ax=ax, linestyle='--', color='darkgrey',  label='Monthly STD')
            labeled = True
        else:
            (trend_removed.std(axis=0)*i).plot(ax=ax, linestyle='--', color='darkgrey',  label='_nolegend_')
        (trend_removed.std(axis=0)*i).apply(lambda x : -x) .plot(ax=ax, linestyle='--', color='darkgrey', label='_nolegend_')    

    # Show the last 20 years of data with the trend removed 
    for year in historical_years:
        trend_removed.loc[year].plot(ax=ax, label=year)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    
    ax.set_title('Detrended {}'.format(title))
    
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylabel('PPM')
    plt.grid()
    plt.savefig(os.path.join(save_path, 'Trend Removed.png'))


    # show the entire time series with the trends, 
    fig, ax = plt.subplots()
    preds.stack().plot(ax=ax, label='Monthly Regressions')
    data.stack().plot(ax=ax, label='Recorded Data')
    full_reg.stack().plot(ax=ax, label='Full Regression')
    plt.legend()
    plt.grid()
    plt.ylabel('PPM')
    plt.savefig(os.path.join(save_path, 'Monthly vs Full Regression.png'))

    sys.stdout = orig_stdout
    f.close()

    data.to_csv(os.path.join(save_path, fname+'_data.csv'))
    preds.to_csv(os.path.join(save_path, fname+'_trend_data.csv'))
    trend_removed.to_csv(os.path.join(save_path, fname+'_trend_removed.csv'))
    print('Finished: {}'.format(fname))

# METHANE GLOBAL DATA
cols = 'year month decimal average average_unc trend trend_unc'.split()
fname = os.path.join(data_path, 'ch4_mm_gl.csv')
col = 'average'
run(cols, fname, col, 'CH4 Global Data')

# CO2 LOCAL DATA
cols = 'year month day decimal co2_ppm num_days previous_year ten_previous since_1800'.split()
fname = os.path.join(data_path, 'co2_weekly_mlo.csv')
col = 'co2_ppm'
run(cols, fname, col, 'CO2 Mauna Loa Data')

# CO2 GLOBAL DATA
cols= 'year month decimal average average_unc trend trend_unc'.split()
fname = os.path.join(data_path, 'sf6_mm_gl.csv')
col = 'average'
run(cols, fname, col, 'SF6 Global Data')

# N20 GLOBAL DATA
# MUST SPECIFY DATES FROM 2005 - 2020 
cols= 'year month decimal average average_unc trend trend_unc'.split()
fname = os.path.join(data_path, 'n2o_mm_gl.csv')
col = 'average'
run(cols, fname, col, 'N2O Data', historical_years=range(2005, 2020, 5))

# CO2 GLOBAL DATA
cols= 'year month decimal average trend'.split()
fname = os.path.join(data_path, 'co2_mm_gl.csv')
col = 'average'
run(cols, fname, col, 'CO2 Global Data')