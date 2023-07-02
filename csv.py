import csv
import os

# where the original annotation files are
annotations_path = "./annotations"
# where the converted annotation files will be stored
output_path = "./converted_annotations"

# this list is used to store the frame-level labels for each frame
frames = []

# iterate over all annotation files
for filename in os.listdir(annotations_path):
    if filename.endswith(".txt"):
        with open(os.path.join(annotations_path, filename), 'r') as file:
            reader = csv.reader(file)

            # clear the frame list for each new file
            frames.clear()

            for row in reader:
                start, end, label = map(int, row)
                # we calculate the number of frames based on 24 fps
                start_frame = start * 4
                end_frame = end * 4
                # we add the label to the frame list for the range of frames specified
                frames[start_frame:end_frame] = [label] * (end_frame - start_frame)

        # write the frame-level labels to a new file
        with open(os.path.join(output_path, filename.replace(".txt", ".csv")), 'w', newline='') as file:
            writer = csv.writer(file)
            for label in frames:
                writer.writerow([label])
