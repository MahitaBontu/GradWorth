import pandas as pd
import json
import requests

def fetch_college_scorecard_data():
    api_key = '8slewlULAuRoJfkehoQgJbN5gTJBDeYgb3NoDBJN'
    # College Scorecard API endpoint
    base_url = "https://api.data.gov/ed/collegescorecard/v1/schools"
    
    # Parameters for the API request
    params = {
        "api_key": api_key,
        "per_page": 100,
        "school.degrees_awarded.predominant": "3,4",  # 3=Bachelor's, 4=Graduate
        "fields": "school.name,school.city,school.state,school.school_url,"
                 "school.ownership,latest.earnings.5_yrs_after_entry.median,"
                 "latest.aid.median_debt.completers.overall,"
                 "latest.cost.tuition.in_state,latest.cost.tuition.out_of_state,"
                 "latest.admissions.admission_rate.overall"
    }
    
    all_data = []
    page = 0
    
    while True:
        params['page'] = page
        response = requests.get(base_url, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            break
            
        data = response.json()
        if not data['results']:
            break
            
        all_data.extend(data['results'])
        page += 1
        print(f"Fetched page {page}, total schools: {len(all_data)}")
    
    return pd.json_normalize(all_data)

def create_institution_json():
    # Fetch data from College Scorecard API
    df = fetch_college_scorecard_data()
    
    # Fetch data from the API
    df = fetch_college_scorecard_data(api_key)

    # Rename columns for consistency
    df = df.rename(columns={
        'school.name': 'school',
        'school.city': 'city',
        'school.state': 'state',
        'school.school_url': 'website',
        'school.ownership': 'control',
        'latest.earnings.5_yrs_after_entry.median': 'earnings',
        'latest.aid.median_debt.completers.overall': 'debt',
        'latest.cost.tuition.in_state': 'tuition_in_state',
        'latest.cost.tuition.out_of_state': 'tuition_out_state',
        'latest.admissions.admission_rate.overall': 'admission_rate'
    })
    
    # Clean and process the data
    df = df.dropna(subset=['school', 'state'])
    
    # Map control values to readable format
    control_map = {1: 'Public', 2: 'Private Non-Profit', 3: 'Private For-Profit'}
    df['type'] = df['control'].map(control_map)
    
    # Calculate estimated total cost (using in-state tuition as default)
    df['cost'] = df['tuition_in_state'].fillna(0) * 4  # Assuming 4 years
    
    # Convert to records
    institutions = df.to_dict(orient='records')
    
    # Sort by school name
    institutions.sort(key=lambda x: x['school'] if x['school'] else '')

    # Write to JSON file
    with open('roi_institution_data.json', 'w') as f:
        json.dump(institutions, f)
    
    print(f"Successfully wrote data for {len(institutions)} institutions to roi_institution_data.json")

if __name__ == "__main__":
    create_institution_json()
