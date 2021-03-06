import pandas as pd

def mdLongformat():

    # read the original CSV file with uncleaned data and put it into a pandas dataframe
    df = pd.read_csv('marriageanddivorce.csv', na_values='null')

    # put the names of the columns into a list to be used with melt
    columnList = df.columns.tolist()

    # Use melt to change the table from wide to long format.
    df_melted = pd.melt(df, id_vars=['State'], value_vars=columnList[1:32], var_name='Year', value_name='Rate')

    # Since year and type (marriage and divorce) are in the same column at this point, this splits them into 2 columns.
    df_melted[['Year', 'Type']] = df_melted['Year'].str.split(' ', expand=True)

    # List used to set the desired order of column titles for later reindexing.
    columnTitles = ['State', 'Year', 'Type', 'Rate']

    # Reindex uses the list of column titles (above) as the order of the columns of the table.
    df_melted = df_melted.reindex(columns=columnTitles)

    # Sorts the values by state, year, and type. Order of sorting is determined by the ascending boolean.
    df_melted = df_melted.sort_values(['State', 'Year', 'Type'], ascending=[True, True, False])

    # Unstack divorce and marriage types into 2 columns
    df_long = df_melted.pivot_table(index=['State', 'Year'], columns='Type', values='Rate', dropna=False)

    # Takes the df_final dataframe and exports it to a CSV file.
    df_long.to_csv('mdLong_nulls.csv', index=True)


def mdImpute():

    df = pd.read_csv('mdLong_nulls.csv', na_values='null', header=0, index_col='State')

    # Fill null values for every state where we decided to use a backward fill
    df.loc['Colorado', 'Divorce'] = df.loc['Colorado', 'Divorce'].fillna(method='bfill')
    df.loc['Oklahoma', 'Marriage'] = df.loc['Oklahoma', 'Marriage'].fillna(method='bfill')

    # Fill null values for every state where we decided to use a forward fill
    df.loc['California', 'Divorce'] = df.loc['California', 'Divorce'].fillna(method='ffill')
    df.loc['Minnesota', 'Divorce'] = df.loc['Minnesota', 'Divorce'].fillna(method='ffill')
    df.loc['Louisiana', 'Marriage'] = df.loc['Louisiana', 'Marriage'].fillna(method='ffill')

    # Full null values for every state where we decided to use mean fill
    df.loc['Georgia', 'Divorce'] = df.loc['Georgia', 'Divorce'].fillna(df.loc['Georgia', 'Divorce'].mean())
    df.loc['Hawaii', 'Divorce'] = df.loc['Hawaii', 'Divorce'].fillna(df.loc['Hawaii', 'Divorce'].mean())
    df.loc['Louisiana', 'Divorce'] = df.loc['Louisiana', 'Divorce'].fillna(df.loc['Louisiana', 'Divorce'].mean())
    df.loc['Oklahoma', 'Divorce'] = df.loc['Oklahoma', 'Divorce'].fillna(df.loc['Oklahoma', 'Divorce'].mean())

    # Fill the rest with the mean from every year (at this point, it should just be Indiana divorce that's missing.
    df = df.fillna(df.groupby(['Year']).transform('mean'))

    # Round all the values in the table to one decimal place (as in the original table)
    df = df.round(decimals=1)

    # Export the filled table to a new CSV file
    df.to_csv('mdrates_filled.csv')

    # make sure the table lengths stay the same after null value imputation
    print('Table lengths equal?')
    if len(pd.read_csv('mdrates_filled.csv')) == len(pd.read_csv('mdLong_nulls.csv')):
        print('Yes')

mdLongformat()
mdImpute()