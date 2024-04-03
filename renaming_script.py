import os
import re

folder_path = "Files"

# Open all main .c files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".c"):
        file_path = os.path.join(folder_path, file_name)

        # Open the files and read the comments
        with open(file_path, 'r') as file:

            # Create an array with all comments
            comments_with_digits = []
            for line in file:
                if "//" in line:
                    comment_text = line.split("//")[1].strip()

                    # Search for 8-digit numbers with digits between 0-9
                    matches = re.findall(r'\b\d{8}\b', comment_text)
                    comments_with_digits.extend(matches)

            # Make a secondary check to sanitize the array "comments with digits" and remove duplicates as well as
            # invalid numbers
            comments_with_digits = list(set(comments_with_digits))

            # Make sure all the numbers start with 20
            comments_with_digits = [comment for comment in comments_with_digits if comment.startswith("20")]

            # If there is still more than one number in the array, create a popup that tells the user to check that
            # there is only one student id in the file
            if len(comments_with_digits) > 1:
                print(f"Check file: {file_name} for multiple student IDs")
                continue  # Skip renaming if there are multiple IDs

        # If there's a single ID, proceed to rename the file
        if comments_with_digits:
            for comment in comments_with_digits:
                new_file_name = f"main_{comment}.c"
                new_file_path = os.path.join(folder_path, new_file_name)
                os.rename(file_path, new_file_path)
