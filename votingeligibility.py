import pandas as pd

# Super simple function to clean the voting eligibility data I obtained from https://data.world/carlvlewis/voter-regist
# ration-and-criminal-records-by-state-1980-2014/workspace/file?filename=voting-ineligibility-since-1980.csv
def votEl():

    # This dataset is already really clean, so all I will be doing is getting rid of the columns I am not interested in
    # for the sake of simplicity when working in Tableau.

    # Read the CSV file
    df = pd.read_csv('voting-ineligibility-since-1980.csv')

    # Drop the columns I don't need
    df = df.drop(['ICPSR_State_Code', 'Alphanumeric_State_Code', 'Turnout_Rates_VEP_Total_Ballots_Counted',
                  'Numerators_Total_Ballots_Counted', 'Non_citizen', 'Prison', 'Probation', 'Parole',
                  'Total_Ineligible_Felon', 'Percent Ineligible Because of Felony Charges',
                  'Percent of Turnout Potentially Swayed by Ineligibilty'], axis=1)

    # Create a new column with the total number of ineligible voters.
    df['Voting Ineligible Population'] = df['Voting Age Population'] - df['Voting Eligible Population']

    # Get rid of the total United States population values since they throw off the scale in Tableau
    df = df[df['State'] != 'United States']

    # Export cleaned data to new CSV
    df.to_csv('voteout.csv', index=False)

votEl()