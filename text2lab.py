import mytextgrid
import os

use_converter = False # [True/False] If you want to use a phonetic convertion, set it to True
low_number = True # [True/False] If you want to remove numbers and transform the text to lowercase, set it to True

# Open, read and store info for convertion
converter_file = open('converter.txt', 'r')
converter_text = converter_file.read()
converter = dict(map(str.strip, line.split(',')) for line in converter_text.split('\n') if line.strip())

# Function to lowercase and remove nunbers
def lowercase_and_remove_numbers(text):
    text = text.lower()
    text = ''.join(c for c in text if not c.isdigit())
    return text

# Function to convert TextGrid to lab file
def textgrid_to_lab(textgrid_file):
    tg = mytextgrid.read_from_file(textgrid_file)
    lab_lines = []
    for tier in tg:
        if tier.name =='phones' and tier.is_interval():
            for interval in tier:
                time_start = int(float(interval.xmin)*10000000)
                time_end = int(float(interval.xmax)*10000000)
                label = interval.text
                if label == '':
                    label = 'pau'
                if low_number:
                    # lowercase and remove numbers
                    label = lowercase_and_remove_numbers(label)
                if use_converter:
                    # Convert phoneme to another, if exists
                    for phoneme, replacement in converter.items():
                        label = label.replace(phoneme, replacement)
                lab_lines.append(f"{time_start} {time_end} {label}")
    return lab_lines

# Get all TextGrid files in subfolders
for subdir, dirs, files in os.walk("./"):
    for file in files:
        if file.endswith(".TextGrid"):
            textgrid_file = os.path.join(subdir, file)
            lab_lines = textgrid_to_lab(textgrid_file)
            # Write lab lines to a space separated lab file
            lab_file = textgrid_file.replace(".TextGrid", ".lab")
            with open(lab_file, 'w') as f:
                for lab_line in lab_lines:
                    f.write("%s\n" % lab_line)
            print(f"Converted {textgrid_file} to {lab_file}")