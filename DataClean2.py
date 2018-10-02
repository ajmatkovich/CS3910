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

    # Incomplete section
'''
def medincomeClean():

    # dataframe for current dollars table
    df1 = pd.read_excel("h08.xls", skiprows=4, skip_footer=56, header=[0,1])

    # dataframe for 2017 dollars table
    df2 = pd.read_excel("h08.xls", skiprows=59, skip_footer=1, header=[0,1])

    # flatten df1 column headers and format them correctly
    #df1.columns = pd.Index([str(e[0]) + ' ' + str(e[1]) for e in df1.columns.tolist()])  # flatten
    #df1.columns = df1.columns.str.replace('\(.*\)', '') # get rid of the things in parentheses
    #df1.columns = df1.columns.str.replace('  ', ' ') # get rid of the double spaces
    #df1.columns = df1.columns.str.replace('\n', ' ') # get rid of the newline characters and replace with spaces


    df1.columns = df1.columns.rename(names=['Year', 'Type'], level=None, inplace=False)
    df1.index = df1.index.rename('State', inplace=False)



    # flatten df2 column headers and format them correctly
    df2.columns = pd.Index([str(e[0]) + ' ' + str(e[1]) for e in df2.columns.tolist()]) #flatten
    df2.columns = df2.columns.str.replace('\(.*\)', '')  # get rid of the things in parentheses
    df2.columns = df2.columns.str.replace('  ', ' ')  # get rid of the double spaces
    df2.columns = df2.columns.str.replace('\n', ' ')  # get rid of the newline characters and replace with spaces

    print(df1.head())
    #df2.to_csv('test2.csv')
'''
#medincomeClean()
crimesClean()
mardivClean()