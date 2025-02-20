import numpy as np
#input survey values
nums_of_surveys=int(input("Enter the number of survey: "))
survey_values = []
positive_prob_surveys = []
favprob_positive_surveys=[]
unfavprob_negative_surveys=[]

if nums_of_surveys!=0:
  for i in range(nums_of_surveys):
    survey_value = int(input(f"Enter the values of survey {i+1}: "))
    survey_values.append(survey_value)
    positive_prob_survey=float(input(f"Enter the positive probability of survey {i+1}: "))
    positive_prob_surveys.append(positive_prob_survey)
    favprob_positive_survey=float(input(f"Enter the favprob_positive of survey {i+1}: "))
    favprob_positive_surveys.append(favprob_positive_survey)
    unfavprob_negative_survey=float(input(f"Enter the unfavprob_negative of survey {i+1}: "))
    unfavprob_negative_surveys.append(unfavprob_negative_survey)
 
#input decision values   
nums_of_decisions=int(input("Enter the number of decisions: "))
decision_favvalues=[]
decision_unfavvalues=[]
for i in range(nums_of_decisions):
    decision_favvalue=int(input(f"Enter the favvalue of decision {i+1}: "))
    decision_favvalues.append(decision_favvalue)
    decision_unfavvalue=int(input(f"Enter the unfavvalue of decision {i+1}: "))
    decision_unfavvalues.append(decision_unfavvalue)
expected_fav_prob=float(input("Enter the expected fav_prob: "))
do_nothing=0
# Make survey values
survey_values_dict={}
for i in range(nums_of_surveys):
    survey_values_dict.update({f'survey{i+1}_positive': []})
    survey_values_dict.update({f'survey{i+1}_negative': []})
# Calculate survey values in positive and negative situations
for i in range(nums_of_surveys):
    for j in range(nums_of_decisions):
        # Positive situation: Subtracting survey value from the favored decision value
        positive_value = decision_favvalues[j] - survey_values[i]
        survey_values_dict[f'survey{i+1}_positive'].append(positive_value)
        
        # Negative situation: Subtracting survey value from the unfavored decision value
        negative_value = decision_unfavvalues[j] - survey_values[i]
        survey_values_dict[f'survey{i+1}_negative'].append(negative_value)
    
    
# Decsion 0: no survey
EMV=[]
for i in range(nums_of_decisions):
        EMV.append(decision_favvalues[i]*expected_fav_prob+decision_unfavvalues[i]*(1-expected_fav_prob))
EMV.append(do_nothing) 
decision_no_survey=max(EMV)  

# Decsions with surveys
decisions = {}
for i in range(nums_of_surveys):    
    # positive probability
    decisions.update({f'survey{i+1}_positive_decision{j+1}': [] for j in range(nums_of_decisions+1)})   
    for j in range(nums_of_decisions):
        # Retrieve positive and negative values from survey_values_dict
        pos_value = survey_values_dict[f'survey{i+1}_positive'][j]
        neg_value = survey_values_dict[f'survey{i+1}_negative'][j]
        
        decisions[f'survey{i+1}_positive_decision{j+1}'].append(
            pos_value*favprob_positive_surveys[i] + neg_value*(1-favprob_positive_surveys[i])
        )
    decisions[f'survey{i+1}_positive_decision{nums_of_decisions+1}']=[do_nothing-survey_values[i]]
    
    # negative probability
    decisions.update({f'survey{i+1}_negative_decision{j+1}': [] for j in range(nums_of_decisions+1)})
    for j in range(nums_of_decisions):
        # Retrieve positive and negative values from survey_values_dict
        pos_value = survey_values_dict[f'survey{i+1}_positive'][j]
        neg_value = survey_values_dict[f'survey{i+1}_negative'][j]
        
        decisions[f'survey{i+1}_negative_decision{j+1}'].append(
            pos_value*(1-unfavprob_negative_surveys[i]) + neg_value*unfavprob_negative_surveys[i]
        )
    decisions[f'survey{i+1}_negative_decision{nums_of_decisions+1}']=[do_nothing-survey_values[i]]


groupsize=nums_of_decisions+1   
best = {}

# Number of surveys based on the total number of decisions divided by twice the groupsize
num_of_surveys = len(decisions) // (2 * groupsize)

for i in range(1, num_of_surveys + 1):
    positive_values = [decisions[f'survey{i}_positive_decision{j}'][0] for j in range(1, groupsize + 1)]
    best[f'survey{i}_positive'] = max(positive_values)
    
    negative_values = [decisions[f'survey{i}_negative_decision{j}'][0] for j in range(1, groupsize + 1)]
    best[f'survey{i}_negative'] = max(negative_values)

# Calculate the best decision
best_decisions = {}

for i in range(len(positive_prob_surveys)):
    pos_value = best[f'survey{i+1}_positive']
    neg_value = best[f'survey{i+1}_negative']
    emv = pos_value * positive_prob_surveys[i] + neg_value * (1 - positive_prob_surveys[i])
    best_decisions[f'EMV_survey{i+1}'] = emv

best_decisions['EMV_no_survey'] = decision_no_survey
print(best_decisions)



