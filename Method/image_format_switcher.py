#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
from shutil import copyfile
from tqdm import tqdm

def switchImageFormat(source_image_folder_path, source_format, target_image_folder_path, target_format):
    if not os.path.exists(source_image_folder_path):
        print("[ERROR][switch_image_format::switchImageFormat]")
        print("\t source_image_folder_path not exist!")
        return False

    if os.path.exists(target_image_folder_path):
        target_image_folder_file_list = os.listdir(target_image_folder_path)

        if len(target_image_folder_file_list) > 0:
            print("[ERROR][switch_image_format::switchImageFormat]")
            print("\t target_image_folder_path already exist and not empty!")
            return False
    else:
        os.makedirs(target_image_folder_path)

    source_file_name_list = os.listdir(source_image_folder_path)

    source_image_file_basename_list = []

    for source_file_name in source_file_name_list:
        source_file_name_split_list = source_file_name.split(".")
        source_file_basename = source_file_name_split_list[0]
        if "." + source_file_name_split_list[1] != source_format:
            continue
        source_image_file_basename_list.append(source_file_basename)

    print("[INFO][switch_image_format::switchImageFormat]")
    print("\t start switch image format...")
    for source_image_file_basename in tqdm(source_image_file_basename_list):
        source_image_file_path = source_image_folder_path + source_image_file_basename + source_format
        target_image_file_path = target_image_folder_path + source_image_file_basename + target_format

        image = cv2.imread(source_image_file_path)
        cv2.imwrite(target_image_file_path, image)

        source_xml_file_path = source_image_folder_path + source_image_file_basename + ".xml"
        if os.path.exists(source_xml_file_path):
            target_xml_file_path = target_image_folder_path + source_image_file_basename + ".xml"
            copyfile(source_xml_file_path, target_xml_file_path)
    return True

def demo():
    source_image_folder_path = "/home/chli/yolo/test/1/"
    source_format = ".jpg"
    target_image_folder_path = "/home/chli/yolo/test/1_png/"
    target_format = ".png"

    switchImageFormat(source_image_folder_path,
                      source_format,
                      target_image_folder_path,
                      target_format)
    return True

if __name__ == "__main__":
    demo()

