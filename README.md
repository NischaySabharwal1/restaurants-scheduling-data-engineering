# restaurants-scheduling-data-engineering

File Structure: 

1. restaurants-opening-hour.xlsx - Given format of the data for Microsoft Excel.
2. create_tables.py: Reads 'restaurants-opening-hour.xlsx' and outputs the restaurants.csv and schedule.csv data files
3. main.py: Uses the restaurants.csv and schedule.csv files to extract the open restaurants based on the day and time given by the user
4. test_inputs.py: Consists of 4 test cases used for verifying the working of the extraction algorithm
5. Restaurants-schedule-extraction.ipynb: The Jupyter notebook file with the steps used for creating the algorithm
6. 'restaurants.csv': Dimension table for restaurants file created from create_tables.py
7. 'schedule.csv': Fact table consisting of restaurant schedules created from create_tables.py