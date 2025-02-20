import numpy as np
import pandas as pd
payoff_table=pd.DataFrame()

# Take input of probabilities
probabilities_input = input("Enter the probabilities of the events, separated by commas: ")
# Convert the comma-separated string into a list of floats
probabilities_list = [float(x) for x in probabilities_input.split(',')]
# Convert the list into a numpy array
probabilities = np.array(probabilities_list)
# Add the probabilities to the payoff table
payoff_table['Probabilities'] = probabilities

# Take input of alternatives
number_of_alternatives = int(input("Enter the number of alternatives: "))
for i in range(number_of_alternatives):
    # Take input of payoffs
    payoffs_input = input("Enter the payoffs for alternative " + str(i+1) + ", separated by commas: ")
    # Convert the comma-separated string into a list of floats
    payoffs_list = [float(x) for x in payoffs_input.split(',')]
    # Convert the list into a numpy array
    payoffs = np.array(payoffs_list)
    # Add the payoffs to the payoff table
    payoff_table['Alternative ' + str(i+1)] = payoffs
    
payoff_table=payoff_table.transpose()

# Calculate the expected value of each alternative
alternative_list=[]
for i in range(number_of_alternatives):
    alternative_list.append('Alternative '+str(i+1))
payoff_table['EV']=0.0
for i in alternative_list:
    ev=(payoff_table.loc['Probabilities']*payoff_table.loc[i]).sum()
    payoff_table.loc[i,'EV']=ev


# For profit, enter 'p' and for cost, enter 'c'
profit_or_cost = input("Enter 'p' for profit and 'c' for cost: ")
if profit_or_cost == 'p':
    payoff_table.loc['Probabilities','EV']=np.nan
    EMV=payoff_table['EV'].max()
    alternative_with_max_EMV = payoff_table['EV'].idxmax()
    print(f"The maximum EMV is {EMV} for {alternative_with_max_EMV}.")
    # Initialize an empty list to store the 'with PI' values
    with_pi_values = []

    # Iterate over the columns (excluding the 'EV' column)
    for col in payoff_table.columns[:-1]:
        # Extract the probabilities value
        probability = payoff_table.at['Probabilities', col]
    
        # Extract the max value from alternatives for the current column
        max_value = payoff_table.loc[alternative_list, col].max()
    
        # Compute 'with PI' value for the current column
        with_pi_value = max_value * probability
        with_pi_values.append(with_pi_value)

    # Compute the 'EV' value for 'with PI' row
    ev_with_pi = sum(with_pi_values)

    # Append the 'EV' value to the 'with PI' values list
    with_pi_values.append(ev_with_pi)

    # Add the computed 'with PI' values as a new row to the DataFrame
    payoff_table.loc['with PI'] = with_pi_values

    EVwPI=payoff_table.loc['with PI','EV']
    print("The EMV with PI is " + str(EVwPI) + ".")
    print('The EVPI is ' + str(EVwPI - EMV) + '.')
    print(payoff_table)

elif profit_or_cost == 'c':
    payoff_table.loc['Probabilities','EV']=np.nan
    EMV=payoff_table['EV'].min()
    alternative_with_max_EMV = payoff_table['EV'].idxmin()
    print(f"The minimum EMV is {EMV} for {alternative_with_max_EMV}.")
    # Initialize an empty list to store the 'with PI' values
    with_pi_values = []

    # Iterate over the columns (excluding the 'EV' column)
    for col in payoff_table.columns[:-1]:
        # Extract the probabilities value
        probability = payoff_table.at['Probabilities', col]
    
        # Extract the max value from alternatives for the current column
        max_value = payoff_table.loc[alternative_list, col].min()
    
        # Compute 'with PI' value for the current column
        with_pi_value = max_value * probability
        with_pi_values.append(with_pi_value)

    # Compute the 'EV' value for 'with PI' row
    ev_with_pi = sum(with_pi_values)

    # Append the 'EV' value to the 'with PI' values list
    with_pi_values.append(ev_with_pi)

    # Add the computed 'with PI' values as a new row to the DataFrame
    payoff_table.loc['with PI'] = with_pi_values

    EVwPI=payoff_table.loc['with PI','EV']
    print("The EMV with PI is " + str(EVwPI) + ".")
    print('The EVPI is ' + str(EMV - EVwPI) + '.')
    print(payoff_table)
