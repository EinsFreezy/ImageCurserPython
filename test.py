import os
import glob
import random
from PIL import Image
from itertools import product
import datetime
import time


def delFolder(path):
    folder_path = path

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


def tile(filename, dir_in, dir_out, d):
    start = time.time()

    split_filename = filename.split(".")
    filetyp = split_filename[-1]

    name, ext = os.path.splitext(filename)
    img = Image.open(os.path.join(dir_in, filename))
    w, h = img.size

    grid = product(range(0, h - h % d, d), range(0, w - w % d, d))
    for i, j in grid:
        box = (j, i, j + d, i + d)
        out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
        img.crop(box).save(out)

    # Get a list of all PNG files in the folder
    png_files = glob.glob(dir_out + '/*.png')

    # Calculate the number of columns and rows based on the file names
    column_nums = set()
    row_nums = set()
    for file in png_files:
        # Extract the column and row numbers from the file name
        filename = file.split('/')[-1]
        print(filename)
        name, column_num, row_num = filename.split('_')[:3]
        column_nums.add(int(str(column_num)))
        row_nums.add(int(str(row_num).replace("." + filetyp, "")))

    print(column_nums)
    print(row_nums)

    num_cols = max(column_nums) // d + 1
    num_rows = max(row_nums) // d + 1

    # Calculate the dimensions of the final image
    image_width = num_cols * d
    image_height = num_rows * d

    print(f'Number of columns: {num_cols}')
    print(f'Number of rows: {num_rows}')
    print(f'Image width: {image_width}')
    print(f'Image height: {image_height}')

    # Print the total number of files found
    print(f'Total number of files: {len(png_files)}')

    # Check for missing files
    missing_files = []
    for png_file in png_files:
        if not os.path.isfile(png_file):
            missing_files.append(png_file)

    # Print any missing files
    if len(missing_files) > 0:
        print(f'Missing files: {missing_files}')

    # Choose a random file and remove it from the list
    random_files = []
    while len(png_files) > 0:
        random_file = random.choice(png_files)
        png_files.remove(random_file)
        random_files.append(random_file)
        random.shuffle(png_files)

    # Create a new blank image for the final collage
    num_images = len(random_files)
    collage_width = 64 * num_cols
    collage_height = 64 * num_rows

    image_width = int(collage_width / num_cols)
    image_height = int(collage_height / num_rows)
    collage_image = Image.new('RGBA', (collage_width, collage_height), (255, 255, 255, 255))

    # Loop through the random files and paste them onto the collage image
    for i, png_file in enumerate(random_files):
        x_pos = (i % num_cols) * image_width
        y_pos = (i // num_cols) * image_height
        image = Image.open(png_file)
        image = image.resize((image_width, image_height))
        collage_image.paste(image, (x_pos, y_pos))

    # Save the final collage image
    collage_image.save(dir_out + '/collage.png')

    end = time.time() - start
    print(end)


delFolder('./img_out')
tile('olafscholz01.jpg', './img', './img_out', 1)
