#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET

sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["container", "drop", "zbar"]

def convert(size, box):
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

def convert_annotation(xml_folder_path, xml_file_basename, save_folder_path):
    tree = None
    with open(xml_folder_path + xml_file_basename + ".xml", "r") as in_file:
        tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text),
             float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        with open(save_folder_path + "labels/" + xml_file_basename + ".xml", 'w') as out_file:
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    return True

def demo():
    xml_folder_path = "/home/chli/yolo/test/1_png/"
    save_folder_path = "/home/chli/yolo/test/1_png_yolo/"

    if not os.path.exists(xml_folder_path):
        print("[ERROR][voc_to_yolo::demo]")
        print("\t xml_folder_path not exist!")
        return False

    if os.path.exists(save_folder_path):
        save_folder_filename_list = os.listdir(save_folder_path)
        if len(save_folder_filename_list) > 0:
            print("[ERROR][voc_to_yolo::demo]")
            print("\t save_folder_path already exist and not empty!")
            return False
    else:
        os.makedirs(save_folder_path)
        os.makedirs(save_folder_path + "labels/")

    xml_folder_filename_list = os.listdir(xml_folder_path)
    image_filename_list = []
    for xml_folder_filename in xml_folder_filename_list:
        xml_folder_filename_split_list = xml_folder_filename.split(".")
        if xml_folder_filename

    image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
    for xml_file_basename in image_ids:
        list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg\n'%(wd, year, xml_file_basename))
        convert_annotation(year, xml_file_basename)

if __name__ == "__main__":
    demo()

