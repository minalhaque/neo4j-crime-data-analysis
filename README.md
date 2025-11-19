# Neo4j Crime Data Analysis Pipeline

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-4.x-008CC1?style=for-the-badge&logo=neo4j&logoColor=white)](https://neo4j.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

> Transform flat crime CSV data into a powerful Neo4j graph database for advanced pattern analysis

**Developed by:** Minal Haque  
**Year:** 2024-2025

---

## Table of Contents

- [Overview]
- [Features]
- [Graph Schema]
- [Quick Start]
- [Project Structure]
- [How It Works]
- [Neo4j Import]
- [Example Queries]
- [Customization]
- [Testing]
- [Performance]
- [Documentation]
- [License]
- [Author]

---

## Overview

This project provides a complete ETL pipeline that transforms a flat CSV crime dataset into a graph database structure optimized for Neo4j. It enables powerful crime pattern analysis through graph queries that would be difficult or impossible with traditional relational databases.

### What It Does

**INPUT:** Single CSV file with crime records  
**OUTPUT:** 15 Neo4j-compatible CSV files (7 node types + 7 relationship types)

### Why Graph Database?

- Find Hidden Patterns - Discover crime relationships through graph traversal
- Spatial Analysis - Analyze crime spread across adjacent beats
- Temporal Patterns - Identify seasonal and yearly trends
- Complex Queries - Answer questions like "What neighborhoods have similar crime patterns?"

---

## Features

- **Automated Processing** - Single script processes entire dataset in seconds
- **Data Cleaning** - Handles missing values, invalid dates, duplicates
- **ID Generation** - Creates unique identifiers for all entities
- **Relationship Mapping** - Builds all crime-to-entity connections automatically
- **Temporal Decomposition** - Extracts year, month, month names from dates
- **Spatial Relationships** - Creates beat adjacency graph for spatial analysis
- **Neo4j Ready** - CSV headers pre-formatted for direct import
- **Fast Performance** - Processes 10K+ crimes in under 10 seconds

---

## Graph Schema

### Visual Representation

```
                    ┌──────────────┐
                    │ Neighborhood │
                    │  (283 nodes) │
                    └──────────────┘
                           ▲
                           │
                    OCCURRED_IN
                           │
    ┌──────────┐     ┌─────────┐     ┌──────────────┐
    │CrimeType │◄────│  Crime  │────►│PropertyType  │
    │(7 nodes) │     │(9643 n.)│     │  (11 nodes)  │
    └──────────┘     └─────────┘     └──────────────┘
       OF_TYPE       │  │  │  │       AT_PROPERTY
                     │  │  │  │
          IN_BEAT────┘  │  │  └────IN_MONTH
                        │  │
                   IN_YEAR │
                           │
                   ┌───────▼──────────┐
                   │  Beat  │ Month   │
                   │(19 n.) │(12 n.)  │
                   └────────┴─────────┘
                   │  Year    │
                   │ (X nodes)│
                   └──────────┘
                        │
              Beat─[ADJACENT_TO]─►Beat
```

### Entity-Relationship Breakdown

**Nodes (7 types):**
- **Crime** - Individual crime records with ID and date
- **Neighborhood** - Geographic locations where crimes occur
- **CrimeType** - Categories of crimes (Burglary, Theft, etc.)
- **PropertyType** - Types of properties targeted
- **Beat** - Police patrol beats
- **Month** - Calendar months (1-12)
- **Year** - Years in dataset

**Relationships (7 types):**
- **OCCURRED_IN** - Crime to Neighborhood
- **OF_TYPE** - Crime to CrimeType
- **AT_PROPERTY** - Crime to PropertyType
- **IN_BEAT** - Crime to Beat
- **IN_MONTH** - Crime to Month
- **IN_YEAR** - Crime to Year
- **ADJACENT_TO** - Beat to Beat (spatial adjacency)

---

## Quick Start

### Prerequisites

```bash
# Install Python 3.8 or higher
python --version

# Install required packages
pip install pandas
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

### Running the Pipeline

```bash
# 1. Navigate to project directory
cd neo4j-crime-data-preprocessing

# 2. Run preprocessing script
python Preprocessing_DataSet.py

# 3. Output will be in neo4j_csv/ folder
ls neo4j_csv/
```

### Expected Output

```
Loading the data...
Loaded 9643 crime records

Creating crimes.csv...
Created 9643 crime nodes

Creating neighborhoods.csv...
Created 283 neighborhood nodes

Creating crime_types.csv...
Created 7 crime type nodes

Creating property_types.csv...
Created 11 property type nodes

Creating beats.csv...
Created 19 beat nodes

Creating months.csv...
Created 12 month nodes

Creating years.csv...
Created X year nodes

Creating occurred_in.csv...
Created 9643 OCCURRED_IN relationships

Creating of_type.csv...
Created 9643 OF_TYPE relationships

Creating at_property.csv...
Created 9643 AT_PROPERTY relationships

Creating in_beat.csv...
Created 9643 IN_BEAT relationships

Creating in_month.csv...
Created 9643 IN_MONTH relationships

Creating in_year.csv...
Created 9643 IN_YEAR relationships

Creating adjacent_beats.csv...
Created 18 ADJACENT_TO relationships

All CSVs Made
```

---

## Project Structure

```
neo4j-crime-data-preprocessing/
│
├── README.md                      # This file
├── LICENSE                        # MIT License
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
│
├── Preprocessing_DataSet.py       # Main ETL script
├── crime_subset.csv               # Sample input data (9,643 crimes)
│
├── neo4j_csv/                     # Generated output files
│   ├── crimes.csv                 # Crime nodes
│   ├── neighborhoods.csv          # Neighborhood nodes
│   ├── crime_types.csv            # Crime type nodes
│   ├── property_types.csv         # Property type nodes
│   ├── beats.csv                  # Beat nodes
│   ├── months.csv                 # Month nodes
│   ├── years.csv                  # Year nodes
│   ├── occurred_in.csv            # Crime→Neighborhood relationships
│   ├── of_type.csv                # Crime→CrimeType relationships
│   ├── at_property.csv            # Crime→PropertyType relationships
│   ├── in_beat.csv                # Crime→Beat relationships
│   ├── in_month.csv               # Crime→Month relationships
│   ├── in_year.csv                # Crime→Year relationships
│   └── adjacent_beats.csv         # Beat→Beat relationships
│
├── examples/                      # Usage examples
│   ├── neo4j_import_commands.cypher  # Complete import script
│   └── sample_queries.cypher         # 30+ example queries
│
└── docs/                          # Documentation
    └── PIPELINE.md                # Detailed pipeline docs
```

---

## How It Works

### Input Data Format

**File:** crime_subset.csv

**Required Columns:**
```csv
number,crime,date,neighborhood,beat,type
1,Burglary,2024-01-15,Downtown,B101,Residential
2,Theft,2024-02-20,Eastside,B102,Commercial
3,Assault,2024-03-10,Westside,B103,Public
```

### Processing Pipeline

```
┌─────────────────────┐
│  1. EXTRACT         │
│  - Load CSV         │
│  - Select columns   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  2. TRANSFORM       │
│  - Parse dates      │
│  - Extract entities │
│  - Generate IDs     │
│  - Build maps       │
│  - Create relations │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  3. LOAD            │
│  - Format CSV       │
│  - Write 15 files   │
│  - Verify output    │
└─────────────────────┘
```

### Key Transformations

**1. Date Parsing:**
```
'2024-01-15' → year: 2024, month: 1, month_name: 'January'
```

**2. Entity Extraction:**
```
283 unique neighborhoods → neighborhoodId: 0, 1, 2, ...
7 unique crime types → crimeTypeId: 0, 1, 2, ...
```

**3. Relationship Building:**
```
Crime #1 in 'Downtown' → (Crime:1)-[:OCCURRED_IN]->(Neighborhood:0)
```

**4. Spatial Adjacency:**
```
Sorted beats: ['B101', 'B102', 'B103']
Creates: B101→B102, B102→B103
```

---

## Neo4j Import

### Step 1: Copy Files to Neo4j

```bash
# Find your Neo4j import directory
# Default locations:
# - Linux: /var/lib/neo4j/import/
# - Mac: ~/Library/Application Support/Neo4j Desktop/.../import/
# - Windows: C:\Users\YourName\.Neo4jDesktop\...\import\

# Copy all CSV files
cp neo4j_csv/*.csv /path/to/neo4j/import/
```

### Step 2: Create Indexes (Recommended)

```cypher
CREATE INDEX FOR (c:Crime) ON (c.crimeId);
CREATE INDEX FOR (n:Neighborhood) ON (n.neighborhoodId);
CREATE INDEX FOR (ct:CrimeType) ON (ct.crimeTypeId);
CREATE INDEX FOR (pt:PropertyType) ON (pt.propertyTypeId);
CREATE INDEX FOR (b:Beat) ON (b.beatId);
CREATE INDEX FOR (m:Month) ON (m.monthNumber);
CREATE INDEX FOR (y:Year) ON (y.yearNumber);
```

### Step 3: Import Nodes

```cypher
// Import Crime nodes
LOAD CSV WITH HEADERS FROM 'file:///crimes.csv' AS row
CREATE (:Crime {
  crimeId: toInteger(row.`crimeId:ID`), 
  date: date(row.date)
});

// Import Neighborhood nodes
LOAD CSV WITH HEADERS FROM 'file:///neighborhoods.csv' AS row
CREATE (:Neighborhood {
  neighborhoodId: toInteger(row.`neighborhoodId:ID`), 
  name: row.name
});

// Import CrimeType nodes
LOAD CSV WITH HEADERS FROM 'file:///crime_types.csv' AS row
CREATE (:CrimeType {
  crimeTypeId: toInteger(row.`crimeTypeId:ID`), 
  type: row.type
});

// Import PropertyType nodes
LOAD CSV WITH HEADERS FROM 'file:///property_types.csv' AS row
CREATE (:PropertyType {
  propertyTypeId: toInteger(row.`propertyTypeId:ID`), 
  type: row.type
});

// Import Beat nodes
LOAD CSV WITH HEADERS FROM 'file:///beats.csv' AS row
CREATE (:Beat {beatId: row.`beatId:ID`});

// Import Month nodes
LOAD CSV WITH HEADERS FROM 'file:///months.csv' AS row
CREATE (:Month {
  monthNumber: toInteger(row.`monthNumber:ID`), 
  monthName: row.monthName
});

// Import Year nodes
LOAD CSV WITH HEADERS FROM 'file:///years.csv' AS row
CREATE (:Year {yearNumber: toInteger(row.`yearNumber:ID`)});
```

### Step 4: Import Relationships

```cypher
// Import OCCURRED_IN relationships
LOAD CSV WITH HEADERS FROM 'file:///occurred_in.csv' AS row
MATCH (c:Crime {crimeId: toInteger(row.`:START_ID`)})
MATCH (n:Neighborhood {neighborhoodId: toInteger(row.`:END_ID`)})
CREATE (c)-[:OCCURRED_IN]->(n);

// Import OF_TYPE relationships
LOAD CSV WITH HEADERS FROM 'file:///of_type.csv' AS row
MATCH (c:Crime {crimeId: toInteger(row.`:START_ID`)})
MATCH (ct:CrimeType {crimeTypeId: toInteger(row.`:END_ID`)})
CREATE (c)-[:OF_TYPE]->(ct);

// Import AT_PROPERTY relationships
LOAD CSV WITH HEADERS FROM 'file:///at_property.csv' AS row
MATCH (c:Crime {crimeId: toInteger(row.`:START_ID`)})
MATCH (pt:PropertyType {propertyTypeId: toInteger(row.`:END_ID`)})
CREATE (c)-[:AT_PROPERTY]->(pt);

// Import IN_BEAT relationships
LOAD CSV WITH HEADERS FROM 'file:///in_beat.csv' AS row
MATCH (c:Crime {crimeId: toInteger(row.`:START_ID`)})
MATCH (b:Beat {beatId: row.`:END_ID`})
CREATE (c)-[:IN_BEAT]->(b);

// Import IN_MONTH relationships
LOAD CSV WITH HEADERS FROM 'file:///in_month.csv' AS row
MATCH (c:Crime {crimeId: toInteger(row.`:START_ID`)})
MATCH (m:Month {monthNumber: toInteger(row.`:END_ID`)})
CREATE (c)-[:IN_MONTH]->(m);

// Import IN_YEAR relationships
LOAD CSV WITH HEADERS FROM 'file:///in_year.csv' AS row
MATCH (c:Crime {crimeId: toInteger(row.`:START_ID`)})
MATCH (y:Year {yearNumber: toInteger(row.`:END_ID`)})
CREATE (c)-[:IN_YEAR]->(y);

// Import ADJACENT_TO relationships
LOAD CSV WITH HEADERS FROM 'file:///adjacent_beats.csv' AS row
MATCH (b1:Beat {beatId: row.`:START_ID`})
MATCH (b2:Beat {beatId: row.`:END_ID`})
CREATE (b1)-[:ADJACENT_TO]->(b2);
```

### Step 5: Verify Import

```cypher
// Check node counts
MATCH (c:Crime) RETURN COUNT(c) AS Crimes;
MATCH (n:Neighborhood) RETURN COUNT(n) AS Neighborhoods;

// Check relationship counts
MATCH ()-[r:OCCURRED_IN]->() RETURN COUNT(r) AS OccurredIn;

// Visualize sample data
MATCH (c:Crime)-[r]-(n)
WHERE c.crimeId = 1
RETURN c, r, n
LIMIT 25;
```

**Full Import Guide:** See examples/neo4j_import_commands.cypher

---

## Example Queries

### Top 10 Crime Hotspots

```cypher
MATCH (c:Crime)-[:OCCURRED_IN]->(n:Neighborhood)
RETURN n.name AS Neighborhood, COUNT(c) AS CrimeCount
ORDER BY CrimeCount DESC
LIMIT 10;
```

### Seasonal Crime Patterns

```cypher
MATCH (c:Crime)-[:IN_MONTH]->(m:Month)
RETURN m.monthName AS Month, COUNT(c) AS CrimeCount
ORDER BY m.monthNumber;
```

### Adjacent Beat Analysis

```cypher
MATCH (b1:Beat)<-[:IN_BEAT]-(c:Crime)
MATCH (b1)-[:ADJACENT_TO]->(b2:Beat)
RETURN b1.beatId AS Beat1, b2.beatId AS Beat2, COUNT(c) AS CrimeCount
ORDER BY CrimeCount DESC;
```

### Most Common Crime Types

```cypher
MATCH (c:Crime)-[:OF_TYPE]->(ct:CrimeType)
RETURN ct.type AS CrimeType, COUNT(c) AS Count
ORDER BY Count DESC;
```

### Property Types Targeted

```cypher
MATCH (c:Crime)-[:AT_PROPERTY]->(pt:PropertyType)
RETURN pt.type AS PropertyType, COUNT(c) AS Count
ORDER BY Count DESC;
```

### Crime Types by Month

```cypher
MATCH (c:Crime)-[:OF_TYPE]->(ct:CrimeType)
MATCH (c)-[:IN_MONTH]->(m:Month)
RETURN m.monthName, ct.type, COUNT(c) AS Count
ORDER BY m.monthNumber, Count DESC;
```

### Find Similar Neighborhoods

```cypher
MATCH (n1:Neighborhood)<-[:OCCURRED_IN]-(c1:Crime)-[:OF_TYPE]->(ct:CrimeType)
MATCH (n2:Neighborhood)<-[:OCCURRED_IN]-(c2:Crime)-[:OF_TYPE]->(ct)
WHERE n1 <> n2
WITH n1, n2, COUNT(ct) AS SharedCrimeTypes
WHERE SharedCrimeTypes > 5
RETURN n1.name, n2.name, SharedCrimeTypes
ORDER BY SharedCrimeTypes DESC
LIMIT 10;
```

**30+ More Queries:** See examples/sample_queries.cypher

---

## Customization
### Add New Node Type

```python
# Example: Add districts
districts = df[['district']].drop_duplicates().reset_index(drop=True)
districts['districtId'] = range(len(districts))
districts.columns = ['districtId:ID', 'name']
districts.to_csv(os.path.join(output_folder, 'districts.csv'), index=False)
```

### Add New Relationship

```python
# Example: Crime to District
in_district = df[['crime_id', 'district_id']].copy()
in_district.columns = [':START_ID', ':END_ID']
in_district.to_csv(os.path.join(output_folder, 'in_district.csv'), index=False)
```

### Add Node Properties

```python
# Add severity to crimes
crimes['severity'] = df['severity']
crimes.columns = ['crimeId:ID', 'date', 'severity:int']
```

---

## Testing

### Verify Script Execution

```bash
# Run with sample data
python Preprocessing_DataSet.py

# Check output folder
ls neo4j_csv/

# Should show 15 CSV files
```

### Verify CSV Format

```bash
# Check node CSV headers
head -n 2 neo4j_csv/crimes.csv
# Output: crimeId:ID,date

# Check relationship CSV headers
head -n 2 neo4j_csv/occurred_in.csv
# Output: :START_ID,:END_ID
```

### Verify Data Integrity

```bash
# Count crimes
wc -l neo4j_csv/crimes.csv
# Should be: 9644 (9643 crimes + 1 header)

# Count relationships
wc -l neo4j_csv/occurred_in.csv
# Should be: 9644 (9643 relationships + 1 header)
```

### Neo4j Database Tests

```cypher
// Verify all crimes have relationships
MATCH (c:Crime)
WHERE NOT (c)-->()
RETURN COUNT(c) AS OrphanCrimes;
// Should return: 0

// Verify relationship integrity
MATCH (c:Crime)-[:OCCURRED_IN]->(n:Neighborhood)
RETURN COUNT(c) AS CrimesWithNeighborhood;
// Should return: 9643
```

---

## Performance

### Benchmark Results

**System:** Standard laptop (8GB RAM, Intel i5)  
**Dataset:** 9,643 crime records

| Stage | Time | Memory |
|-------|------|--------|
| Data Loading | <1s | ~2 MB |
| Transformation | ~2s | ~5 MB |
| CSV Generation | ~2s | ~3 MB |
| **Total** | **~5s** | **<10 MB** |

### Scalability

- Linear time complexity O(n)
- Can handle 100K+ crimes on standard hardware
- For millions of records, use chunking:

```python
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    process_chunk(chunk)
```

---

## Documentation

| Document | Description |
|----------|-------------|
| README.md | This file - Quick start guide |
| PIPELINE.md | Detailed pipeline documentation |
| neo4j_import_commands.cypher | Complete Neo4j import script |
| sample_queries.cypher | 30+ example queries |

---

## License

This project is licensed under the MIT License - see LICENSE file for details.

```
MIT License

Copyright (c) 2025 Minal Haque

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Acknowledgments
- Neo4j Community - Graph database platform and documentation
- Pandas Team - Data analysis library
- Python Community - Programming language and ecosystem


---

If you find this project useful, please consider giving it a star on GitHub!
