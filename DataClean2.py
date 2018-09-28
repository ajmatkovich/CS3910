import pandas as pd

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

def medincomeClean():


    df = pd.read_excel("h08.xls", header=[4,5])

    ind = pd.Index([str(e[0]) + ' ' + str(e[1]) for e in df.columns.tolist()])

    df.columns = ind

    df.columns = df.columns.str.replace('\(.*\)', '')

    df.columns = df.columns.str.replace('  ', ' ')

    df.columns = df.columns.str.replace('\n', ' ')

    #df_melted = pd.melt(df, id_vars='State', )

    currentdollar = df.iloc[4:56,:]
    seventeendollar = df.iloc[60:113,:]


    df.to_csv('test.csv')

medincomeClean()