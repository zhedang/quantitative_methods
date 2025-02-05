import pandas as pd
import numpy as np
# create dataframes for the under uncertainty analysis
payoff_table=pd.DataFrame()

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
print()


# Calculate for the Optimistic, Pessimistic, Equally Likely, and Minimax Regret Criteria

# Optimistic
max_vals = payoff_table.max(axis=1)
max_max_vals = max_vals.max()
print("The optimistic criteria: "+str(max_max_vals))
payoff_table_optimistic = payoff_table.copy()
payoff_table_optimistic['max_in_rows']=payoff_table_optimistic.max(axis=1)
print(payoff_table_optimistic)
print()

# Pessimistic
min_vals = payoff_table.min(axis=1)
max_min_vals = min_vals.max()
print("The pessimistic criteria: "+str(max_min_vals))
payoff_table_pessimistic = payoff_table.copy()
payoff_table_pessimistic['min_in_rows']=payoff_table_pessimistic.min(axis=1)
print(payoff_table_pessimistic)
print()

# Equally Likely
equally_likely_vals = payoff_table.sum(axis=1) * (1/len(payoff_table.columns))
max_equally_likely_vals = equally_likely_vals.max()
print("The equally likely criteria: "+str(max_equally_likely_vals))
payoff_table_equally_likely = payoff_table.copy()
payoff_table_equally_likely['equally_likely_vals']=equally_likely_vals
print(payoff_table_equally_likely)
print()

# Minimax Regret
# Using the 'max()' function along axis=0 (column-wise) to get the maximum value of each column
max_values = payoff_table.max(axis=0)
# Subtracting each cell in the column from the corresponding maximum value
regret_table = max_values - payoff_table
# Get a new column for the maximum regret value for each row
regret_table['max_in_rows']=regret_table.max(axis=1)
# Get Minmax Regret value
minmax_regret = regret_table['max_in_rows'].min()
print("The minimax regret criteria: "+str(minmax_regret))
print(regret_table)
print()

# Criterion of Realism (Hurwicz)
# if Criterion of Realism (Hurwicz) is needed, ask the user to input alpha, or ress 'enter' to skip
alpha = input("Enter alpha for the Criterion of Realism (Hurwicz), or press 'enter' to skip: ")
if alpha == '':
    pass
else:
    alpha = float(alpha)
    hurwicz_vals = (alpha * payoff_table.max(axis=1)) + ((1-alpha) * payoff_table.min(axis=1))
    max_hurwicz_vals = hurwicz_vals.max()
    print("The Criterion of Realism (Hurwicz) criteria: "+str(max_hurwicz_vals))
    payoff_table_hurwicz = payoff_table.copy()
    payoff_table_hurwicz['hurwicz_vals']=hurwicz_vals
    print(payoff_table_hurwicz)