import pandas as pd 
import os 

output_folder = (r"C:\Users\User\OneDrive - Murdoch University\Desktop\ASSIGN2_203\neo4j_csv")
os.makedirs(output_folder, exist_ok=True) # This makes a folder to store all the csvs files 

print("Loading the data...")
df = pd.read_csv(r"C:\Users\User\OneDrive - Murdoch University\Desktop\ASSIGN2_203\crime_subset.csv")

df = df[['number', 'crime', 'date', 'neighborhood', 'beat', 'type']] # Selects only the needed columns for the quieries 

df = df.rename(columns={
    'number': "crime_id", # Renaming columns for clarity
    'crime': 'crime_type',
    'type': 'property_type'
})

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['month_name'] = df['date'].dt.month_name()


print(f"Loaded {len(df)} crime records")
print("\nFirst few rows:")
print(df.head())

# Creating the seperate CSV files 
# Crimes CSV 
print("\nCreating crimes.csv...")
crimes = df[['crime_id', 'date']].copy()
crimes.columns = ['crimeId:ID', 'date']
crimes.to_csv(os.path.join(output_folder,'crimes.csv'), index=False)
print(f"Created {len(crimes)} crime nodes")

# Neighborhoods 
print("\nCreating neighborhoods.csv...")
neighborhoods = df[['neighborhood']].drop_duplicates().reset_index(drop=True)
neighborhoods['neighborhoodId'] = range(len(neighborhoods))
neighborhoods = neighborhoods[['neighborhoodId', 'neighborhood']]
neighborhoods.columns = ['neighborhoodId:ID', 'name']
neighborhoods.to_csv(os.path.join(output_folder,'neighborhoods.csv'), index=False)
print(f"Created {len(neighborhoods)} neighborhood nodes")

# Crime Types 
print("\nCreating crime_types.csv...")
crime_types = df[['crime_type']].drop_duplicates().reset_index(drop=True)
crime_types['crimeTypeId'] = range(len(crime_types))
crime_types = crime_types[['crimeTypeId', 'crime_type']]
crime_types.columns = ['crimeTypeId:ID', 'type']
crime_types.to_csv(os.path.join(output_folder,'crime_types.csv'), index=False)
print(f"Created {len(crime_types)} crime type nodes")

# Property Type 
print("\nCreating property_types.csv...")
property_types = df[['property_type']].drop_duplicates().reset_index(drop=True)
property_types['propertyTypeId'] = range(len(property_types))
property_types = property_types[['propertyTypeId', 'property_type']]
property_types.columns = ['propertyTypeId:ID', 'type']
property_types.to_csv(os.path.join(output_folder,'property_types.csv'), index=False)
print(f"Created {len(property_types)} property type nodes")

# Beats 
print("\nCreating beats.csv...")
beats = df[['beat']].drop_duplicates().reset_index(drop=True)
beats.columns = ['beatId:ID']
beats.to_csv(os.path.join(output_folder,'beats.csv'), index=False)
print(f"Created {len(beats)} beat nodes")

# Months
print("\nCreating months.csv...")
months = df[['month', 'month_name']].drop_duplicates().sort_values('month').reset_index(drop=True)
months.columns = ['monthNumber:ID', 'monthName']
months.to_csv(os.path.join(output_folder,'months.csv') , index=False)
print(f"Created {len(months)} month nodes")

# Years
print("\nCreating years.csv...")
years = df[['year']].drop_duplicates().sort_values('year').reset_index(drop=True)
years.columns = ['yearNumber:ID']
years.to_csv(os.path.join(output_folder,'years.csv'), index=False)
print(f"Created {len(years)} year nodes")

# Mapping Dictionaries 
print("\nCreating ID mappings...")
neighborhood_map = dict(zip(neighborhoods['name'], neighborhoods['neighborhoodId:ID']))
crime_type_map = dict(zip(crime_types['type'], crime_types['crimeTypeId:ID']))
property_type_map = dict(zip(property_types['type'], property_types['propertyTypeId:ID']))

# OCCURRED_IN relationship (Crime -> Neighborhood)
print("\nCreating occurred_in.csv...")
occurred_in = df[['crime_id', 'neighborhood']].copy()
occurred_in['neighborhood_id'] = occurred_in['neighborhood'].map(neighborhood_map)
occurred_in = occurred_in[['crime_id', 'neighborhood_id']]
occurred_in.columns = [':START_ID', ':END_ID']
occurred_in.to_csv(os.path.join(output_folder,'occurred_in.csv'), index=False)
print(f"Created {len(occurred_in)} OCCURRED_IN relationships")

# OF_TYPE relationship (Crime -> CrimeType)
print("\nCreating of_type.csv...")
of_type = df[['crime_id', 'crime_type']].copy()
of_type['crime_type_id'] = of_type['crime_type'].map(crime_type_map)
of_type = of_type[['crime_id', 'crime_type_id']]
of_type.columns = [':START_ID', ':END_ID']
of_type.to_csv(os.path.join(output_folder,'of_type.csv'), index=False)
print(f"Created {len(of_type)} OF_TYPE relationships")

# AT_PROPERTY relationship (Crime -> PropertyType)
print("\nCreating at_property.csv...")
at_property = df[['crime_id', 'property_type']].copy()
at_property['property_type_id'] = at_property['property_type'].map(property_type_map)
at_property = at_property[['crime_id', 'property_type_id']]
at_property.columns = [':START_ID', ':END_ID']
at_property.to_csv(os.path.join(output_folder,'at_property.csv'), index=False)
print(f"Created {len(at_property)} AT_PROPERTY relationships")

# IN_BEAT relationship (Crime - > Beat)
print("\nCreating in_beat.csv...")
in_beat = df[['crime_id', 'beat']].copy()
in_beat.columns = [':START_ID', ':END_ID']
in_beat.to_csv(os.path.join(output_folder,'in_beat.csv'), index=False)
print(f"Created {len(in_beat)} IN_BEAT relationships")

# IN_MONTH relationship (Crime -> Month)
print("\nCreating in_month.csv...")
in_month = df[['crime_id', 'month']].copy()
in_month.columns = [':START_ID', ':END_ID']
in_month.to_csv(os.path.join(output_folder,'in_month.csv'), index=False)
print(f"Created {len(in_month)} IN_MONTH relationships")

# IN_YEAR relationship (Crime -> Year)
print("\nCreating in_year.csv...")
in_year = df[['crime_id', 'year']].copy()
in_year.columns = [':START_ID', ':END_ID']
in_year.to_csv(os.path.join(output_folder,'in_year.csv'), index=False)
print(f"Created {len(in_year)} IN_YEAR relationships")


# For Adjacent Beats 
print("\nCreating adjacent_beats.csv...")

# Get all unique beats and sort them
all_beats = sorted(df['beat'].dropna().astype(str).unique())
beat_map = {beat: i+1 for i, beat in enumerate(all_beats)}
print(f"Beats in data: {all_beats}")

# Create pairs: each beat is adjacent to the next one in the sorted list
adjacent_pairs = []
for i in range(len(all_beats) - 1):
    adjacent_pairs.append((all_beats[i], all_beats[i + 1]))

# Save to CSV
adjacent_df = pd.DataFrame(adjacent_pairs, columns=[':START_ID', ':END_ID'])
adjacent_df.to_csv(os.path.join(output_folder,'adjacent_beats.csv'), index=False)
print(f"Created {len(adjacent_df)} ADJACENT_TO relationships")

print("\n All CSVs Made")
print(f"\n in 'neo4j_csv' folder")

output_folder = (r"C:\Users\User\OneDrive - Murdoch University\Desktop\ASSIGN2_203\neo4j_csv")
print(os.listdir(output_folder))
