import os
import difflib


# Set the threshold for maximum allowable differences
THRESHOLD = 10  # Adjust this threshold as needed


def count_differences(file1, file2):
    """Count the number of differences between two text files."""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        f1n: list = strip_characters(f1.readlines())
        f2n: list = strip_characters(f2.readlines())
        diff = difflib.ndiff(f1n, f2n)
        return sum(1 for line in diff if line.startswith('+') or line.startswith('-'))


# Remove characters that don't matter and are counted in differences (blank lines, whitespace, \n's, and comments).
def strip_characters(file_lines: list[str]) -> list[str]:
    first_copy: list = file_lines.copy()
    stripped_lines: list = []
    for line in first_copy:
        line: str
        if line == "\n":
            continue

        stripped_lines.append(
            (line
             .replace(" ", "")
             .replace("//", "")
             .replace("\n", ""))
        )

    return stripped_lines


# Define the path to the Files folder
folder_path = "Files"

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

        # If the number of differences is within the threshold, add the pair to matching_pairs list
        if differences <= THRESHOLD+2:
            matching_pairs.append([first_file, file, differences-2])
            # Add the pair and its reverse to processed_pairs set
            processed_pairs.add((first_file, file))
            processed_pairs.add((file, first_file))

# Loop through the data and print the suspected cheaters
# [x, y, z], x and y are suspected of cheating with z differences
for pair in matching_pairs:
    print(f"{pair[0]} and {pair[1]} are suspected of cheating with {pair[2]} differences in thier code.")
