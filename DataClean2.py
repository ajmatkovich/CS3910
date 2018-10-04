import pandas as pd

# Clean the violent crimes dataset
def crimesClean():

    # read the original CSV file with uncleaned data and put it into a pandas dataframe
    df = pd.read_csv("violentcrimes.csv")

    # put the names of the columns into a list to be used with melt
    columnList = df.columns.tolist()

    # Use melt to change the table from wide to long format.
    df_melted = pd.melt(df, id_vars=['Region', 'Division', 'State'], value_vars=columnList[3:(len(columnList)+1)],
                        var_name='Year', value_name='Crimes')
    # outputs the long format table to a new csv
    df_melted.to_csv('vcOut.csv', index=False)

# Clean the marriage and divorce dataset
def mardivClean():

    # read the original CSV file with uncleaned data and put it into a pandas dataframe
    df = pd.read_csv("marriageanddivorce.csv")

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

    # Drops rows of the table for which there is no rate data.
    df_melted = df_melted.dropna()

    # Unstack divorce and marriage types into 2 columns
    df_final = df_melted.pivot_table(index=['State', 'Year'], columns='Type', values='Rate')

    # Takes the df_final dataframe and exports it to a CSV file.
    df_final.to_csv('mdOut.csv', index=True)

    # Incomplete section

# Clean the median income dataset
def medincomeClean():

    # get dataframes from excel sheets
    df1 = pd.read_excel("h08.xls", skiprows=3, nrows=53, header=[0, 1, 2])
    df2 = pd.read_excel("h08.xls", skiprows=58, nrows=53, header=[0, 1, 2])

    # use stack to put tables in long format
    df1 = df1.stack([0, 1]).reset_index()
    df2 = df2.stack([0, 1]).reset_index()

    # Rename the columns so they properly reflect the values in them
    column_names = ['State', 'Dollar Type', 'Year', 'Dollars', 'std_dev']
    df1.columns = column_names
    df2.columns = column_names

    # Drop the Dollar Type column. It is not needed since each table will have its own output (one for current dollar
    # and one for 2017 dollar)
    df1 = df1.drop('Dollar Type', axis=1)
    df2 = df2.drop('Dollar Type', axis=1)

    # extract the year code to a different column
    df1['Year Code'] = df1['Year'].str.extract(r'\((.*?)\)')
    df2['Year Code'] = df2['Year'].str.extract(r'\((.*?)\)')

    # remove the year code from the Year column
    df1['Year'] = df1['Year'].astype(str).str[:4]
    df2['Year'] = df2['Year'].astype(str).str[:4]

    # export to csv
    df1.to_csv('curdollar.csv')
    df2.to_csv('17dollar.csv')

medincomeClean()
crimesClean()
mardivClean()