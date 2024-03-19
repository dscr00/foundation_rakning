#%%
import csv
import pandas as pd
df = pd.read_csv("PreferenceExtract-0235069829.csv") # change this to your own extract which can be found in your oriel
specialty_scoring = pd.read_csv('specialty scoring.csv') # I made this based on the specialties provided in the wessex system the csv is in this repo but may be different

df = df[['Programme Preference',	'Placement 1: Employer/Trust',	'Placement 1: Specialty',	'Placement 2: Specialty',	'Placement 3: Specialty',	'Placement 4: Specialty',	'Placement 5: Specialty',	'Placement 6: Specialty']]


# now make a dictionary with the scores I have assigned to each specialty

specialty_scoring_dict = specialty_scoring.set_index('specialty')['score'].to_dict()

# now dictionary for points related to location - used 'Placement 1: Employer/Trust' column

# Provide weightings for your own hospital preferences - currently made for Wessex

loc_dict = {'Hampshire Hospitals NHS Foundation Trust':50,
            'University Hospitals Dorset NHS Foundation Trust':50,
            'Portsmouth Hospitals University NHS Trust':50,
            'University Hospital Southampton NHS Foundation Trust':50,
            'UKFPO (Employing Trust TBC)':50,
            'Dorset County Hospital NHS Foundation Trust':50,
            'Salisbury NHS Foundation Trust':50,
            'Isle of Wight NHS Trust':50,
            'Hampshire and Isle of Wight Healthcare NHS Foundation Trust':50,
            'States of Jersey - Jersey General Hospital':50,
            'Dorset Healthcare University NHS Foundation Trust':50,
            'Avon And Wiltshire Mental Health Partnership NHS Trust':50
            }

# now for the importance of order for me mainly just having med first is a bonus - no multiplier though

# just change if you want to prioritise med/surg - psych also includes GP - this is based on the wessex csv in this repo

med_dict = {'medicine':20,
            'surgery':10,
            'psych':0}

# this is for the 'domain' column in my specialty scoring csv


# now putting everything together


def get_med_score(rotation, med_dict):
    for key, value in med_dict.items():
        if key in rotation.lower():
            return value
    return 0

def score_row(row):
    score = 0
    # Score for location - will be different if using another 
    score += loc_dict.get(row['Placement 1: Employer/Trust'], 0)

    # Score for first rotation medical specialty pro +20
    score += get_med_score(row['Placement 1: Specialty'], med_dict)

    # Score for specialties across all six rotations
    for col in row.index[2:]:  # Skip the first two columns as they're location and first rotation
        specialty = row[col]
        score += specialty_scoring_dict.get(specialty, 0)
    return score

df['Total Score'] = df.apply(score_row, axis=1)

#%%

df.to_csv('ranking_results.csv')
# %%
