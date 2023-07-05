import os
import random
import shutil

# Directory containing the digits folder
base_dir = "sorted_by_num"

# Directory for train and test folders
train_dir = os.path.join("sorted_training", "train")
test_dir = os.path.join("sorted_training", "test")

# Create the train and test directories if they don't exist
if not os.path.exists(train_dir):
    os.makedirs(train_dir)

if not os.path.exists(test_dir):
    os.makedirs(test_dir)

# List subfolders in the digits directory
subfolders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

# Iterate over each subfolder
for subfolder in subfolders:
    # Create the corresponding subfolder in the train and test directories
    train_subfolder = os.path.join(train_dir, subfolder)
    test_subfolder = os.path.join(test_dir, subfolder)

    if not os.path.exists(train_subfolder):
        os.makedirs(train_subfolder)

    if not os.path.exists(test_subfolder):
        os.makedirs(test_subfolder)

    # List all files in the subfolder
    files = os.listdir(os.path.join(base_dir, subfolder))

    # Calculate the number of files for test (25% of total)
    num_test_files = int(len(files) * 0.25)

    # Randomly select files for the test folder
    test_files = random.sample(files, num_test_files)

    # Copy the selected files to the test subfolder
    for test_file in test_files:
        src_path = os.path.join(base_dir, subfolder, test_file)
        dst_path = os.path.join(test_subfolder, test_file)
        shutil.copy(src_path, dst_path)

    # Copy the remaining files to the train subfolder
    for file in files:
        src_path = os.path.join(base_dir, subfolder, file)
        dst_path = os.path.join(train_subfolder, file)
        if file not in test_files:  # Skip the files already copied to the test folder
            shutil.copy(src_path, dst_path)
