# Sales Analytics System

A complete Python-based sales analytics application that:
- Reads and cleans raw sales data
- Validates and optionally filters transactions
- Performs detailed sales analysis
- Enriches sales data using an external API
- Generates comprehensive text reports
---


## Prerequisites

- Python 3.8 or higher
- Internet connection (for API integration)

---

## Setup Instructions

### 1. Clone the Repository
git clone <your-github-repository-url>
cd sales-analytics-system

### 2. (Recommended) Create a Virtual Environment
python -m venv venv

Activate it:

macOS / Linux:
source venv/bin/activate

Windows:
venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

---

## Input Data

Ensure the following file exists before running the program:

data/sales_data.txt

---

## How to Run the Program

From the project root directory, run:

python main.py

---

## Program Execution Flow

1. Displays a welcome banner
2. Reads sales data with encoding handling
3. Parses and cleans transactions
4. Displays available filter options
5. Optional user filtering
6. Validates transactions
7. Performs all analytics
8. Fetches product data from DummyJSON API
9. Enriches sales data
10. Saves enriched data
11. Generates comprehensive report
12. Displays success messages

---

## Output Files

data/enriched_sales_data.txt  
output/sales_report.txt

---

## Error Handling

- Encoding issues handled
- API failures handled gracefully
- User input validated
- Program does not crash

