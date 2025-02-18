# MIT License

# Copyright (c) 2021 Minas Giannekas
# Modified by Newyorker on 2025/2/18

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import argparse
import os
import re
from collections import Counter
from pathlib import Path

from PIL import Image


def split_image(image_path, rows, cols, should_square, should_cleanup,should_reverse,should_quiet=False, output_dir=None):
    im = Image.open(image_path)
    im_width, im_height = im.size
    row_width = int(im_width / cols)
    row_height = int(im_height / rows)
    name, ext = os.path.splitext(image_path)
    name = os.path.basename(name)
    if output_dir != None:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    else:
        output_dir = "./"
    if should_square:
        min_dimension = min(im_width, im_height)
        max_dimension = max(im_width, im_height)
        if not should_quiet:
            print("Resizing image to a square...")
            print("Determining background color...")
        bg_color = determine_bg_color(im)
        if not should_quiet:
            print("Background color is... " + str(bg_color))
        im_r = Image.new("RGBA" if ext == "png" else "RGB",
                         (max_dimension, max_dimension), bg_color)
        offset = int((max_dimension - min_dimension) / 2)
        if im_width > im_height:
            im_r.paste(im, (0, offset))
        else:
            im_r.paste(im, (offset, 0))
        if not should_quiet:
            print("Exporting resized image...")
        outp_path = name + "_squared" + ext
        outp_path = os.path.join(output_dir, outp_path)
        im_r.save(outp_path)
        im = im_r
        row_width = int(max_dimension / cols)
        row_height = int(max_dimension / rows)
    n = 0
    for i in range(0, rows):
        for j in range(0, cols):
            box = (j * row_width, i * row_height, j * row_width +
                   row_width, i * row_height + row_height)
            outp = im.crop(box)
            if should_reverse:
                outp_path = name + "_" + str(1-n) + ext
            else:
                outp_path = name + "_" + str(n) + ext
            outp_path = os.path.join(output_dir, outp_path)
            if not should_quiet:
                print("Exporting image tile: " + outp_path)
            outp.save(outp_path)
            n += 1
    if should_cleanup:
        if not should_quiet:
            print("Cleaning up: " + image_path)
        os.remove(image_path)


def reverse_split(paths_to_merge, rows, cols, image_path, should_cleanup, should_quiet=False):
    if len(paths_to_merge) == 0:
        print("No images to merge!")
        return
    for index, path in enumerate(paths_to_merge):
        path_number = int(path.split("_")[-1].split(".")[0])
        if path_number != index:
            print("Warning: Image " + path +
                  " has a number that does not match its index!")
            print("Please rename it first to match the rest of the images.")
            return
    images_to_merge = [Image.open(p) for p in paths_to_merge]
    image1 = images_to_merge[0]
    new_width = image1.size[0] * cols
    new_height = image1.size[1] * rows
    print(paths_to_merge)
    new_image = Image.new(image1.mode, (new_width, new_height))
    if not should_quiet:
        print("Merging image tiles with the following layout:", end=" ")
    for i in range(0, rows):
        print("\n")
        for j in range(0, cols):
            print(paths_to_merge[i * cols + j], end=" ")
    print("\n")
    for i in range(0, rows):
        for j in range(0, cols):
            image = images_to_merge[i * cols + j]
            new_image.paste(image, (j * image.size[0], i * image.size[1]))
    if not should_quiet:
        print("Saving merged image: " + image_path)
    new_image.save(image_path)
    if should_cleanup:
        for p in paths_to_merge:
            if not should_quiet:
                print("Cleaning up: " + p)
            os.remove(p)


def determine_bg_color(im):
    im_width, im_height = im.size
    rgb_im = im.convert('RGBA')
    all_colors = []
    areas = [[(0, 0), (im_width, im_height / 10)],
             [(0, 0), (im_width / 10, im_height)],
             [(im_width * 9 / 10, 0), (im_width, im_height)],
             [(0, im_height * 9 / 10), (im_width, im_height)]]
    for area in areas:
        start = area[0]
        end = area[1]
        for x in range(int(start[0]), int(end[0])):
            for y in range(int(start[1]), int(end[1])):
                pix = rgb_im.getpixel((x, y))
                all_colors.append(pix)
    return Counter(all_colors).most_common(1)[0][0]

def split_dir(dir_path:Path,rows, cols, should_square:bool, should_cleanup:bool,should_reverse:bool,should_quiet:bool =False, output_dir=None):
    for file in dir_path.iterdir():
        if file.suffix in [".jpg","jpeg",".png"]:
            split_image(file, rows, cols,
                        should_square, should_cleanup, should_reverse, should_quiet, output_dir)



def main():
    parser = argparse.ArgumentParser(
        description="Split an image into rows and columns.")
    parser.add_argument("image_path", nargs=1,
                        help="The path to the image or directory with images to process.")
    parser.add_argument("rows", type=int, default=2, nargs='?',
                        help="How many rows to split the image into (horizontal split).")
    parser.add_argument("cols", type=int, default=2, nargs='?',
                        help="How many columns to split the image into (vertical split).")
    parser.add_argument("-s", "--square", action="store_true",
                        help="If the image should be resized into a square before splitting.")
    parser.add_argument("-m", "--merge", action="store_true",
                        help="Reverse the splitting process, i.e. merge multiple tiles of an image into one.")
    parser.add_argument("--cleanup", action="store_true",
                        help="After splitting or merging, delete the original image/images.")
    parser.add_argument("--load-large-images", action="store_true",
                        help="Ignore the PIL decompression bomb protection and load all large files.")
    parser.add_argument("-o","--output-dir", type=str,
                        help="Set the output directory for image tiles (e.g. 'outp/images'). Defaults to current working directory.")
    parser.add_argument("--quiet", action="store_true",
                        help="Run without printing any messages.")
    parser.add_argument("-r","--reverse", action="store_true",
                        help="Reverse the name order when splitting image")

    args = parser.parse_args()
    if args.load_large_images:
        Image.MAX_IMAGE_PIXELS = None
    image_path = args.image_path[0]
    if not os.path.exists(image_path):
        print("Error: Image path does not exist!")
        return
    if os.path.isdir(image_path):
        if args.merge:
            print("Error: Cannot reverse split a directory of images!")
            return
        if not args.quiet:
            print("Splitting all images in directory: " + image_path)
        
        split_dir(Path(image_path),args.rows, args.cols,
                        args.square, args.cleanup,args.reverse, args.quiet, args.output_dir)
    else:
        if args.merge:
            if not args.quiet:
                print(
                    "Reverse mode selected! Will try to merge multiple tiles of an image into one.\n")
            start_name, ext = os.path.splitext(image_path)
            # Find all files that start with the same name as the image,
            # followed by "_" and a number, and with the same file extension.
            expr = re.compile(r"^" + start_name + "_\d+" + ext + "$")
            paths_to_merge = sorted([f for f in os.listdir(
                os.getcwd()) if re.match(expr, f)], key=lambda x: int(x.split("_")[-1].split(".")[0]))
            reverse_split(paths_to_merge, args.rows,
                          args.cols, image_path, args.cleanup, args.quiet)
        else:
            split_image(image_path, args.rows, args.cols,
                        args.square, args.cleanup, args.quiet, args.output_dir)
    if not args.quiet:
        print("Done!")


if __name__ == "__main__":
    main()
