# Extract the details from the ticket pdf and store them in a dictionary

# uncomment this following when running for the first time

# with open("get_stationcodes.py") as f:
#   exec(f.read())

with open("extract_text.py") as f:
  exec(f.read())

import re
import pandas as pd

station_codes_df = pd.read_csv('./station_codes.csv')

station_codes = station_codes_df['Stations'].tolist()

for _ in range(len(station_codes)):
  station_codes[_] = station_codes[_].upper()
  station_codes[_] = station_codes[_].replace("JUNCTION", "JN")
  station_codes[_] = station_codes[_].replace("JN", " ")
  station_codes[_] = station_codes[_].replace("   ", " ")

travel_classes = ['CHAIR CAR (CC)', 'CC', 'AC CHAIR CLASS (CC)', 'CHAIR CLASS (CC)', 'SECOND AC (2A)', 'THIRD AC (3A)', 'SLEEPER (SL)', 'GENERAL (G)']

# Replace 'path' with the path to the ticket pdf
pdf_path = 'path'

text = get_text(pdf_path)

def extract_info(text):
  name_age_gender_match = re.findall(r'([A-Za-z]+\.?\s([A-Za-z]+\.?\s)?[A-Za-z]+\.?\s*\d{2}\s+[M|F])', text)

  names = []
  genders = []
  ages = []

  for X in name_age_gender_match:
    x_text = X[0]
    filtered = [a for a in x_text.split(" ") if len(a)]
    name_list = filtered[:-2]
    name = " ".join([str(item) for item in name_list])

    names.append(name)

    filtered = filtered[::-1]

    gender = filtered[0]
    genders.append(gender)

    age = filtered[1]
    ages.append(age)

  status_match = []
  statuss = []

  status_match_type1 = re.findall(r'(\w+\s+\/\w+\/\d+\/\w+\s*\w+)', text)
  if status_match_type1:
    status_match = [a for a in list(status_match_type1) if len(a)]
    statuss.append(status_match)
  else:
    status_match_type2 = re.findall(r'(\w+\s*\/\w+\s*\/\w+\s*\/\d+)', text)
    if status_match_type2:
      status_match = [a for a in list(status_match_type2) if len(a)]
      statuss.append(status_match)
    else:
      status_match_type3 = re.findall(r'(\w+\s*\/\w+\s*\/\d+)', text)
      if status_match_type3:
        status_match = [a for a in list(status_match_type3) if len(a)]
        for _ in range(1, len(status_match), 2):
          statuss.append(status_match[_])

  pnr_match = re.findall(r'(\s+\d{10}\s+)', text)
  pnr = (pnr_match[0]).strip()
  pnr = list(pnr.split(" "))
  pnr = pnr[0]

  train_details_gr1_match = re.findall(r'(\s+\d{5}\s+\/\s+\w+\s+\w+)|(\s+\d{5}\s*\/\w+\s+\w+\s+\w+)|(\s+\d{5}\s+\w+\s+\w+\s+)', text)
  for X in train_details_gr1_match:
    x_text = X
    train_details = [a for a in list(x_text) if len(a)]
    train_details = train_details[0].strip()

  boarding_deboarding_match = re.findall(r'(\s+\w+\s+\w+\s+\(\w+\))|(\s+\w+\s+\(\w+\))', text)
  boarding_deboarding_match = [(x[0] + x[1]).strip() for x in boarding_deboarding_match if x[0] or x[1]]
  for _ in range(len(boarding_deboarding_match)):
    boarding_deboarding_match[_] = boarding_deboarding_match[_].upper()
    boarding_deboarding_match[_] = boarding_deboarding_match[_].replace("JN", " ")
    boarding_deboarding_match[_] = boarding_deboarding_match[_].replace("TO ", "")
    boarding_deboarding_match[_] = boarding_deboarding_match[_].replace("   ", " ")

  def common_elements(list1, list2):
    common = list(set(list1) & set(list2))
    return common
  
  match = common_elements(boarding_deboarding_match, station_codes)
  match2 = common_elements(boarding_deboarding_match, travel_classes)

  departure_arrival_match_type1 = re.findall(r'(\*\s+\d{1,2}\:\d{1,2}\s+)|(\:\s+\d{1,2}\:\d{1,2}\s+\w+\s+)', text)
  departure_arrival_match_type1 = [(x[0] + x[1]).strip() for x in departure_arrival_match_type1 if x[0] or x[1]]
  for _ in range(len(departure_arrival_match_type1)):
    departure_arrival_match_type1[_] = departure_arrival_match_type1[_].replace("* ", "")
    departure_arrival_match_type1[_] = departure_arrival_match_type1[_].replace(": ", "")

  departure_arrival_match_type2 = re.findall(r'(\s+\d{1,2}\:\d{1,2}\:\d{1,2}\s+\w{2}\s+)', text)
  if departure_arrival_match_type2:
    arrival_time = departure_arrival_match_type2[1].strip()
    departure_time = departure_arrival_match_type1[0]
  else:
    departure_time = departure_arrival_match_type1[0]
    arrival_time = departure_arrival_match_type1[1]

  details = {
    'name(s)': names,
    'age(s)': ages,
    'gender(s)': genders,
    'status(es)': statuss,
    'pnr': pnr,
    'train_no._and_name': train_details,
    'boarding_from_to': match,
    'class': match2,
    'departure': departure_time,
    'arrival':arrival_time
  }

  return details

details = extract_info(text)