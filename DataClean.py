import pandas as pd

'''
A function which takes the marriage and divorce data (as input.csv), switches it from wide to long format, cleans and
structures it correctly, and exports it to a new file (output.csv). Code will run as the Python file is run.
'''
def dataClean():

    # read the original CSV file with uncleaned data and put it into a pandas dataframe
    df = pd.read_csv("input.csv")

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

    # Takes the df_melted dataframe and exports it to a CSV file.
    df_melted.to_csv('output.csv', index=False)


dataClean()