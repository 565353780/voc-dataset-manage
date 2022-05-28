#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
from shutil import copyfile
from tqdm import tqdm

class YOLOBuilder(object):
    def __init__(self):
        self.classes = []
        self.xml_folder_path = None
        self.save_folder_path = None
        return

    def setVOCInfo(self, classes, xml_folder_path, save_folder_path):
        self.classes = classes
        self.xml_folder_path = xml_folder_path
        self.save_folder_path = save_folder_path
        return True

    def convert(self, size, box):
        dw = 1./size[0]
        dh = 1./size[1]
        x = (box[0] + box[1])/2.0
        y = (box[2] + box[3])/2.0
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x*dw
        w = w*dw
        y = y*dh
        h = h*dh
        return (x,y,w,h)

    def convertAnnotation(self, xml_file_basename):
        tree = None
        xml_file_path = self.xml_folder_path + xml_file_basename + ".xml"

        if not os.path.exists(xml_file_path):
            return True

        with open(xml_file_path, "r") as in_file:
            tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        with open(self.xml_folder_path + xml_file_basename + ".txt", 'w') as out_file:
            for obj in root.iter('object'):
                difficult = obj.find('difficult').text
                cls = obj.find('name').text
                if cls not in self.classes or int(difficult) == 1:
                    continue
                cls_id = self.classes.index(cls)
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text),
                     float(xmlbox.find('xmax').text),
                     float(xmlbox.find('ymin').text),
                     float(xmlbox.find('ymax').text))
                bb = self.convert((w,h), b)
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        return True

    def transLabel(self, image_format):
        if not os.path.exists(self.xml_folder_path):
            print("[ERROR][YOLOBuilder::transLabel]")
            print("\t xml_folder_path not exist!")
            return False

        if os.path.exists(self.save_folder_path):
            save_folder_filename_list = os.listdir(self.save_folder_path)
            if len(save_folder_filename_list) > 0:
                print("[ERROR][YOLOBuilder::transLabel]")
                print("\t save_folder_path already exist and not empty!")
                return False
        else:
            os.makedirs(self.save_folder_path)

        xml_folder_filename_list = os.listdir(self.xml_folder_path)
        xml_file_basename_list = []
        for xml_folder_filename in xml_folder_filename_list:
            xml_folder_filename_split_list = xml_folder_filename.split(".")
            if "." + xml_folder_filename_split_list[1] != image_format:
                continue
            xml_file_basename_list.append(xml_folder_filename_split_list[0])

        #  print("[INFO][YOLOBuilder::transLabel]")
        #  print("\t start convert annotations...")
        with open(self.save_folder_path + "train.txt", "w") as list_file:
            #  for image_file_basename in tqdm(xml_file_basename_list):
            for image_file_basename in xml_file_basename_list:
                list_file.write(self.xml_folder_path + image_file_basename + image_format + "\n")
                self.convertAnnotation(image_file_basename)
        return True

def demo():
    classes = ["container", "drop", "zbar"]
    xml_folder_path = "/home/chli/yolo/test/1_output/merge/"
    save_folder_path = "/home/chli/yolo/test/1_output/yolo/"
    image_format = ".png"

    yolo_builder = YOLOBuilder()
    yolo_builder.setVOCInfo(classes, xml_folder_path, save_folder_path)
    yolo_builder.transLabel(image_format)
    return True

if __name__ == "__main__":
    demo()

