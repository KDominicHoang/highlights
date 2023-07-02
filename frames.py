import os
import math
import concurrent.futures
import subprocess
from pathlib import Path

input_folder = Path('./input_videos')
output_folder = Path('./output')

def extract_frames(video_file):
    output_subfolder = output_folder / f'{video_file.stem}_frames'
    output_subfolder.mkdir(parents=True, exist_ok=True)

    # Get the duration of the video in seconds
    duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
                                              'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
                                              str(video_file)]).decode('utf-8').strip())
    # Calculate the number of frames to extract
    num_frames = math.ceil(duration * 4)  # Changed from 24 to 4

    # Generate ffmpeg commands
    commands = []
    for i in range(num_frames):
        output_file = output_subfolder / f'{i:06}.jpeg'
        commands.append(['ffmpeg', '-accurate_seek', '-ss', f'{i / 4.0}', '-i', str(video_file),  # Changed from 24.0 to 4.0
                         '-frames:v', '1', str(output_file)])

    # Use multiprocessing to execute the commands
    with concurrent.futures.ProcessPoolExecutor() as executor:
        list(executor.map(subprocess.run, commands))

# Collect video files and start processing
video_files = list(input_folder.glob('*.MOV')) + list(input_folder.glob('*.mov'))

with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(extract_frames, video_files)
