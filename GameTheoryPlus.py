import numpy as np
import pandas as pd
from sympy import solve,Eq,symbols
# Create a table
rows_list = []  
row_input = None
table=pd.DataFrame()
dominant_table =pd.DataFrame()
while row_input != "":
    row_input = input("Enter the row, to end press enter: ")
    if row_input != "":
        row = [int(item) for item in row_input.split(",")]
        rows_list.append(row)
table = pd.concat([pd.DataFrame([r]) for r in rows_list], ignore_index=True)
table.columns = ['Y' + str(i) for i in range(1, table.shape[1] + 1)]
table.index = ['X' + str(i) for i in range(1, table.shape[0] + 1)]
print()
print ('The original table is: ')
print(table)

# Define the function for dominance
def dominance(table):
    
    # find the dominant row, then delete the dominated row
    if table.shape[0]>2:
        min_values=table.min(axis=1)
        top_two_max=min_values.nlargest(2)
        dominant_table=table.loc[top_two_max.index]
        dominant_table=dominant_table.sort_index()
    # find the dominant column, then delete the dominated column
    if table.shape[1]>2:
        max_values=table.max(axis=0)
        top_two_min=max_values.nsmallest(2)
        dominant_table=dominant_table.loc[:,top_two_min.index]
        dominant_table=dominant_table.sort_index(axis=1)
    print('The dominant table is:')
    print(dominant_table)
    return dominant_table
    
# define the function for saddle point
def saddle_point(table):
    # find the max value of each row, then minimax
    min_row = table.min(axis=1)
    X_minimax = min_row.max(axis=0)
    print("The X_minimax is: ", X_minimax)
    # find the min value of each column,then maximin
    max_column = table.max(axis=0)
    Y_maximin = max_column.min(axis=0)
    print("The Y_maximin is: ", Y_maximin)
    # find the saddle point
    if X_minimax == Y_maximin:
        print("The saddle point is: ", X_minimax)
        return True
    else:
        print("There is no saddle point.")
        return False

# define the function for mixed strategy
def mixed_strategy(table):
    X_Q,Y_P = symbols('X_Q Y_P')
    eq1 =Eq(Y_P*table.iloc[0,0]+(1-Y_P)*table.iloc[0,1],Y_P*table.iloc[1,0]+(1-Y_P)*table.iloc[1,1])
    eq2 =Eq(X_Q*table.iloc[0,0]+(1-X_Q)*table.iloc[1,0],X_Q*table.iloc[0,1]+(1-X_Q)*table.iloc[1,1])
    solutions = solve((eq1,eq2),(X_Q,Y_P))
    value_X_Q =solutions[X_Q]
    value_Y_P =solutions[Y_P]
    table_value_Y_P = value_Y_P*table.iloc[0,0]+(1-value_Y_P)*table.iloc[0,1]
    table_value_X_Q = value_X_Q*table.iloc[0,0]+(1-value_X_Q)*table.iloc[1,0]
    print('The value of Y_P is: ',value_Y_P)
    print('The value of X_Q is: ',value_X_Q)
    print('The table value using Y_P is: ',table_value_Y_P)
    print('The table value using X_Q is: ',table_value_X_Q)

if table.shape[0]!=2 or table.shape[1]!=2:
    table = dominance(table)

if saddle_point(table) == False:
    mixed_strategy(table)