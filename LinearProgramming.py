import pandas as pd
import numpy as np
import pulp
# get user input
# get info about product1's consumables, profit/cost, split by comma
product1 = input("Enter product1's consumables, profit/cost,  split by comma: ")
product1 = product1.split(",")
product1 = [float(i) for i in product1]
# get info about product2'sconsumables, profit/cost, split by comma
product2 = input("Enter product2's consumables, profit/cost, split by comma: ")
product2 = product2.split(",")
product2 = [float(i) for i in product2]
# get info of consumables' maximum, split by comma
consumables = input("Enter consumables' limits, split by comma: ")
consumables = consumables.split(",")
consumable_requirement = [float(i) for i in consumables]
# get the lower bounds of product1 and product2
lower_bounds = [None]*2
# Get user input
user_input = input("Enter the lower bounds of product1 and product2, split by comma: ")
# Check if the user pressed enter (i.e., provided no input)
if user_input:
    user_values = user_input.split(",")
    # Update the lower_bounds list
    for i, value in enumerate(user_values):
        value = value.strip()  # Remove any leading/trailing whitespace
        if value:  # Check if the value is not empty
            lower_bounds[i] = float(value)  # Convert to float and update
# get the upper bounds of product1 and product2
upper_bounds = [None]*2
# Get user input
user_input = input("Enter the upper bounds of product1 and product2, split by comma: ")
# Check if the user pressed enter (i.e., provided no input)
if user_input:
    user_values = user_input.split(",")
    # Update the upper_bounds list
    for i, value in enumerate(user_values):
        value = value.strip()  # Remove any leading/trailing whitespace
        if value:  # Check if the value is not empty
            upper_bounds[i] = float(value)  # Convert to float and update

# create a dataframe to store the info
data = {
    'product1': product1,
    'product2': product2,
    'consumable_requirement': consumable_requirement
}
index = ['consumable'+str(i) for i in range(1,len(product1))]
index.append('profit/cost')
max_length=max(len(product1),len(product2),len(consumable_requirement))
consumable_requirement +=[np.nan]*(max_length-len(consumable_requirement))        
table = pd.DataFrame(data, index=index)
print(table)

# function for max_profit
def max_profit(table):
    model = pulp.LpProblem(name="example-problem", sense=pulp.LpMaximize)
    x1 = pulp.LpVariable(name="x1", lowBound=lower_bounds[0], upBound=upper_bounds[0])
    x2 = pulp.LpVariable(name="x2", lowBound=lower_bounds[1], upBound=upper_bounds[1])
    model += table.loc['profit/cost', 'product1']*x1 + table.loc['profit/cost', 'product2']*x2,'Total Profit'
    for i in range(1, table.shape[0]):
        constraint_label = f'constraint{i}'
        model += (table.loc[f'consumable{i}', 'product1'] * x1 + table.loc[f'consumable{i}', 'product2'] * x2) <= table.loc[f'consumable{i}', 'consumable_requirement'], constraint_label
    model.solve()
    print(f"x1 = {x1.varValue}")
    print(f"x2 = {x2.varValue}")
    print(f"Objective = {model.objective.value()}")

# function for min_cost
def min_cost(table):
    model = pulp.LpProblem(name="example-problem", sense=pulp.LpMinimize)
    x1 = pulp.LpVariable(name="x1", lowBound=lower_bounds[0], upBound=upper_bounds[0])
    x2 = pulp.LpVariable(name="x2", lowBound=lower_bounds[1], upBound=upper_bounds[1])
    model += table.loc['profit/cost', 'product1']*x1 + table.loc['profit/cost', 'product2']*x2,'Total Cost'
    for i in range(1, table.shape[0]):
        constraint_label = f'constraint{i}'
        model += (table.loc[f'consumable{i}', 'product1'] * x1 + table.loc[f'consumable{i}', 'product2'] * x2) >= table.loc[f'consumable{i}', 'consumable_requirement'], constraint_label
    model.solve()
    print(f"x1 = {x1.varValue}")
    print(f"x2 = {x2.varValue}")
    print(f"Objective = {model.objective.value()}")

# ask user to choose max_profit or min_cost
choice = input("Choose max_profit or min_cost(p or c): ")
if choice == 'p':
    max_profit(table)
elif choice == 'c':
    min_cost(table)
