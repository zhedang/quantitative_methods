import pandas as pd
import re

def parse_expression(expression):
    # Split the expression into terms using '+' as the separator, considering '-'
    terms = re.split(r'(?<!^)(?=[+-])', expression)

    coeffs = []
    for term in terms:
        term = term.strip()  # Remove leading/trailing whitespaces
        if term:
            # Match the coefficient and variable
            match = re.match(r'([+-]?)(\d*\.?\d*)([a-zA-Z]*)', term)
            sign, coeff, var = match.groups()
            # Convert the coefficient to float; if it's empty, set to 1, and consider the sign
            coeff = float(coeff) if coeff else 1
            coeff = -coeff if sign == '-' else coeff  # Apply sign if necessary
            coeffs.append((coeff, var))
    return coeffs

def parse_constraint(constraint):
    coeffs = parse_expression(constraint.split('=')[0])
    rhs = float(re.search(r'([<>]?=)\s*(-?\d+)', constraint).group(2))
    constraint_type = re.search(r'([<>]?=)', constraint).group(1)
    return coeffs, rhs, constraint_type

def parse_objective(objective):
    coeffs = parse_expression(objective)
    return coeffs
    
def get_simplex_tableau_from_input():
    # Requesting the objective function input
    print("Please enter the objective function (e.g., '5x+6y' or '5x-6y'):")
    objective_input = input().strip()

    # Parsing the objective function using the parse_objective function defined earlier
    obj_coeffs = parse_objective(objective_input)

    # Requesting constraint inputs
    constraints_input = []
    print("Please enter the constraints (e.g., '2x+3y<=1000'), one per line. Press enter without typing anything else to finish:")
    while True:
        constraint_input = input().strip()
        if not constraint_input:
            break
        constraints_input.append(constraint_input)

    # Parsing the constraints using the parse_constraint function defined earlier
    parsed_constraints = [parse_constraint(constraint) for constraint in constraints_input]

    # construct the simplex tableau
    simplex=pd.DataFrame()
    # establish the 'z' columen
    simplex['z'] = None

    # establishing the variable columns
    obj_vars = [var for _, var in obj_coeffs]
    for var in obj_vars:
        simplex[var]=None
    # establish the Slack and Artificial columns
    # calculate the number of slack and artificial variables
    num_slack = 0
    num_artificial = 0
    for constraint in constraints_input:
        coeffs, _, constraint_type = parse_constraint(constraint)
        if constraint_type == '<=':
            num_slack += 1
        elif constraint_type == '=':
            num_artificial += 1
        elif constraint_type == '>=':
            num_slack += 1
            num_artificial += 1
    # add the slack and artificial columns
    for i in range(num_slack):
        simplex[f'S{i+1}']=None
    for i in range(num_artificial):
        simplex[f'A{i+1}']=None
    # estalbish the RHS column
    simplex['RHS']=None
    # Construct rows
    # add the z row
    simplex.loc['z'] = pd.Series(dtype='float')
    # add the constraint rows
    S_count = 0
    A_count = 0
    for constraint in constraints_input:
        _, _, constraint_type = parse_constraint(constraint)
        if constraint_type == '<=':
            S_count += 1
            simplex.loc[f'S{S_count}']=pd.Series(dtype='float')
        elif constraint_type == '=':
            A_count += 1
            simplex.loc[f'A{A_count}']=pd.Series(dtype='float')
        elif constraint_type == '>=':
            A_count += 1
            S_count += 1
            simplex.loc[f'A{A_count}']=pd.Series(dtype='float')
    # update z row values
    simplex.loc['z', 'z'] = 1
    for coeff, var in obj_coeffs:
        simplex.loc['z', var] = -coeff
    for i in range(num_artificial):
        if max_min == "min":
            simplex.loc['z', f'A{i+1}'] = simplex.iloc[0,1]*20
        else:
            simplex.loc['z', f'A{i+1}'] = simplex.iloc[0,1]*-20
    # update constraint rows
    row_index=1
    slack_pool = [f'S{i}' for i in range(1, num_slack + 1)]
    artificial_pool = [f'A{i}' for i in range(1, num_artificial + 1)]
    for constraint in constraints_input:
        coeffs, rhs, constraint_type = parse_constraint(constraint)
        simplex.iloc[row_index, -1] = rhs
        index_name=simplex.index[row_index]
        for coeff, var in coeffs:
            simplex.loc[index_name, var] = coeff

        if constraint_type == '<=':
            simplex.loc[index_name, slack_pool.pop(0)] = 1
        elif constraint_type == '=':
            simplex.loc[index_name, artificial_pool.pop(0)] = 1
        elif constraint_type == '>=':
            simplex.loc[index_name, slack_pool.pop(0)] = -1
            simplex.loc[index_name, artificial_pool.pop(0)] = 1
        
        row_index += 1
    simplex.fillna(0, inplace=True)
    
    
    if 'A1' in simplex.columns:
        print('The initial simplex tableau is:')
        print(simplex)
        print()
        if max_min == "min":
            M=simplex.iloc[0,1]*-20
        else:
            M=simplex.iloc[0,1]*20
        for i in range(1, num_artificial+1):               
                simplex.loc['z']=simplex.loc['z']+simplex.loc[f'A{i}']*M              
    return simplex

def pivoting_max(df):
    #find the pivot column
    pivot_col = df.loc['z'].idxmin()
    print("Pivot column is: ", pivot_col)
    #find the pivot row
    ratios = df.loc[df.index != 'z', 'RHS'] / df[pivot_col]
    positive_ratios = ratios[ratios >= 0]
    pivot_row = positive_ratios.idxmin()
    print("Pivot row is:", pivot_row)
    #find the pivot element
    pivot_element = df.loc[pivot_row, pivot_col]
    print("Pivot element is:", pivot_element)
    #pivot the pivot row
    df.loc[pivot_row] = df.loc[pivot_row] / pivot_element    
    # update the simplex tableau
    for row in df.index:
        if row != pivot_row:
            df.loc[row] = df.loc[row] - df.loc[row, pivot_col] * df.loc[pivot_row]
    # update the pivot_row
    df = df.rename(index={pivot_row: pivot_col})
    print()
    print('The updated simplex tableau is:\n', df)
    return df

def pivoting_min(df):
    #find the pivot column
    pivot_col = df.loc['z'].drop(['z','RHS']).idxmax()
    print("Pivot column is: ", pivot_col)
    #find the pivot row
    pivot_row = (df.loc[df.index != 'z', 'RHS'] / df[pivot_col])
    pivot_row = pivot_row[pivot_row>0].idxmin()
    print("Pivot row is:", pivot_row)
    #find the pivot element
    pivot_element = df.loc[pivot_row, pivot_col]
    print("Pivot element is:", pivot_element)
    #pivot the pivot row
    df.loc[pivot_row] = df.loc[pivot_row] / pivot_element
    # update the simplex tableau
    for row in df.index:
        if row != pivot_row:
            df.loc[row] = df.loc[row] - df.loc[row, pivot_col] * df.loc[pivot_row]
    # update the pivot_row
    df = df.rename(index={pivot_row: pivot_col})
    print()
    print('The updated simplex tableau is:\n', df)
    return df

# Ask the user if they want to do max or min
print("maximize or minimize? pls enter max or min")
max_min = input()

simplex=get_simplex_tableau_from_input()
print('The basic simplex tableau is:\n', simplex)


if max_min == "max":
    while simplex.loc['z'].min() < 0:
        simplex=pivoting_max(simplex)
    print()
elif max_min == "min":
    while simplex.loc['z'].drop(['z','RHS']).max() > 0:
        simplex=pivoting_min(simplex)
    print()

