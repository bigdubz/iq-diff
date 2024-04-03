import os
import json
import difflib

def count_differences(file1, file2):
    """Count the number of differences between two text files."""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        f1n: list = [line.replace("//", "") for line in f1.readlines()]
        f2n: list = [line.replace("//", "") for line in f2.readlines()]
        diff = difflib.ndiff(f1n, f2n)
        return sum(1 for line in diff if line.startswith('+') or line.startswith('-'))

# Define the path to the Files folder
folder_path = 'Files'

# Get a list of all files in the folder
file_list = os.listdir(folder_path)

# Create an empty list to store the matching pairs
matching_pairs = []

# Create a set to store processed pairs to avoid repetitions
processed_pairs = set()

# Compare every file with every file
for first_file in file_list:
    for file in file_list:
        # Skip if the files are the same or if the pair is already processed
        if first_file == file or (first_file, file) in processed_pairs:
            continue
        
        # Count the number of differences between the two files
        differences = count_differences(os.path.join(folder_path, first_file), os.path.join(folder_path, file))
        
        # Set the threshold for maximum allowable differences
        threshold = 10  # Adjust this threshold as needed
        
        # If the number of differences is within the threshold, add the pair to matching_pairs list
        if differences <= threshold:
            matching_pairs.append((first_file, file, {"differences": differences}))
            # Add the pair and its reverse to processed_pairs set
            processed_pairs.add((first_file, file))
            processed_pairs.add((file, first_file))

# Convert the matching_pairs list to a JSON string
json_data = json.dumps(matching_pairs)

# Write the JSON string to a file
with open('matching_pairs.json', 'w') as file:
    file.write(json_data)

# List the suspected cheaters from the json file
# {x,y, differences: z} # x and y are suspected of cheating with 4 differences

# Open the JSON file and load the data
with open('matching_pairs.json', 'r') as file:
    data = json.load(file)
    # Loop through the data and print the suspected cheaters
    for pair in data:
        print(f"{pair[0]} and {pair[1]} are suspected of cheating with {pair[2]['differences']} differences.")
