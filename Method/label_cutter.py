#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import xml.etree.ElementTree as ET
from tqdm import tqdm

from Method.image_object import ImageObject
from Method.xml_builder import XMLBuilder

class LabelCutter(object):
    def __init__(self):
        self.source_image_folder_path = None
        self.cut_image_save_path = None
        self.cut_by_label_list = None
        self.cut_save_label_list = None

        self.xml_file_basename = None
        self.root = None
        self.image = None
        return

    def setSourceImageFolderPath(self, source_image_folder_path):
        if not os.path.exists(source_image_folder_path):
            print("[ERROR][LabelCutter::setSourceImageFolderPath]")
            print("\t source_image_folder_path not exist!")
            return False
        self.source_image_folder_path = source_image_folder_path
        if self.source_image_folder_path[-1] != "/":
            self.source_image_folder_path += "/"
        return True

    def setCutImageSavePath(self, cut_image_save_path):
        self.cut_image_save_path = cut_image_save_path
        if self.cut_image_save_path[-1] != "/":
            self.cut_image_save_path += "/"

        if not os.path.exists(self.cut_image_save_path):
            os.makedirs(self.cut_image_save_path)
        return True

    def setCutInfo(self,
                   source_image_folder_path,
                   cut_image_save_path,
                   cut_by_label_list,
                   cut_save_label_list):
        '''
        Input :
            source_image_folder_path : str
            cut_image_save_path : str
            cut_by_label_list : [cut_by_label_1, cut_by_label_2, ...]
            cut_save_label_list : [cut_save_label_1, cut_save_label_2, ...]
        '''
        if not self.setSourceImageFolderPath(source_image_folder_path):
            print("[ERROR][LabelCutter::setCutInfo]")
            print("\t setSourceImageFolderPath failed!")
            return False

        if not self.setCutImageSavePath(cut_image_save_path):
            print("[ERROR][LabelCutter::setCutInfo]")
            print("\t setCutImageSavePath failed!")
            return False

        self.cut_by_label_list = cut_by_label_list
        self.cut_save_label_list = cut_save_label_list
        return True

    def loadXML(self, xml_file_basename, image_format):
        '''
        Input :
            xml_file_basename
            image_format
        '''
        self.xml_file_basename = xml_file_basename
        self.root = None

        xml_file_path = self.source_image_folder_path + self.xml_file_basename + ".xml"
        if not os.path.exists(xml_file_path):
            print("[ERROR][LabelCutter::loadXML]")
            print("\t xml_file not exist in source_image_folder_path!")
            return False

        image_file_path = self.source_image_folder_path + self.xml_file_basename + image_format
        if not os.path.exists(image_file_path):
            print("[ERROR][LabelCutter::loadXML]")
            print("\t image_file not exist in source_image_folder_path!")
            return False

        tree = ET.parse(xml_file_path)
        self.root = tree.getroot()
        self.image = cv2.imread(image_file_path)
        return True

    def getObjectList(self):
        '''
        Return :
            [ImageObject(), ...]
        '''
        if self.root is None:
            print("[ERROR][LabelCutter::getObjectList]")
            print("\t not load any xml file!")
            return None

        object_list = []

        for obj in self.root.iter('object'):
            name = obj.find('name').text
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)

            obj = ImageObject(name, xmin, ymin, xmax, ymax)
            object_list.append(obj)
        return object_list

    def getObjectListWithLabel(self, label_list):
        '''
        Input :
            label_list : [label_1, label_2, ...]
        Return :
            [ImageObject(), ...]
        '''
        if self.root is None:
            print("[ERROR][LabelCutter::getObjectListWithLabel]")
            print("\t not load any xml file!")
            return None

        if label_list is None:
            print("[WARN][LabelCutter::getObjectListWithLabel]")
            print("\t label_list is empty!")
            return []

        object_list_with_label = []

        for obj in self.root.iter('object'):
            name = obj.find('name').text
            if name not in label_list:
                continue

            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)

            obj = ImageObject(name, xmin, ymin, xmax, ymax)
            object_list_with_label.append(obj)
        return object_list_with_label

    def cutImage(self, xml_file_basename, image_format):
        '''
        Input :
            xml_file_basename
            image_format
        '''
        if self.cut_by_label_list is None:
            print("[ERROR][LabelCutter::cutImage]")
            print("\t cut_by_label_list is None!")
            return False
        if self.cut_save_label_list is None:
            print("[ERROR][LabelCutter::cutImage]")
            print("\t cut_save_label_list is None!")
            return False

        if not self.loadXML(xml_file_basename, image_format):
            print("[ERROR][LabelCutter::cutImage]")
            print("\t loadXML failed!")
            return False

        cut_by_object_list = self.getObjectListWithLabel(self.cut_by_label_list)
        if cut_by_object_list is None:
            print("[ERROR][LabelCutter::cutImage]")
            print("\t getObjectListWithLabel for cut_by_label_list failed!")
            return False

        cut_save_object_list = self.getObjectListWithLabel(self.cut_save_label_list)
        if cut_save_object_list is None:
            print("[ERROR][LabelCutter::cutImage]")
            print("\t getObjectListWithLabel for cut_save_label_list failed!")
            return False

        current_save_object_idx = 0

        for cut_by_object in cut_by_object_list:
            current_save_object_idx += 1

            child_object_list = []
            for cut_save_object in cut_save_object_list:
                child_object = cut_by_object.getChild(cut_save_object)
                if child_object is None:
                    continue
                child_object_list.append(child_object)

            current_cut_image_basename = \
                xml_file_basename + "_" + str(current_save_object_idx) + "_" + cut_by_object.name
            current_cut_image_basepath = self.cut_image_save_path + current_cut_image_basename

            current_cut_image_width = cut_by_object.bbox[2] - cut_by_object.bbox[0]
            current_cut_image_height = cut_by_object.bbox[3] - cut_by_object.bbox[1]
            current_cut_image_depth = 3

            current_cut_image = cut_by_object.getBBoxImage(self.image)
            cv2.imwrite(current_cut_image_basepath + image_format, current_cut_image)

            if len(child_object_list) == 0:
                continue

            xml_builder = XMLBuilder()
            xml_builder.initXML()
            xml_builder.setImageFilePath(current_cut_image_basepath + image_format)
            xml_builder.setImageSize(current_cut_image_width, current_cut_image_height, current_cut_image_depth)
            for child_object in child_object_list:
                xml_builder.addObject(child_object)

            xml_builder.saveXML(current_cut_image_basepath + ".xml")
        return True

    def cutAllImage(self, image_format):
        '''
        Input :
            image_format
        '''
        cut_image_filename_list = os.listdir(self.source_image_folder_path)
        cut_image_xml_filename_list = []

        print("[INFO][LabelCutter::cutAllImage]")
        print("start choose labeled image...")
        for cut_image_filename in tqdm(cut_image_filename_list):
            if cut_image_filename[-4:] != ".xml":
                continue
            if cut_image_filename[:-4] + image_format not in cut_image_filename_list:
                continue
            cut_image_xml_filename_list.append(cut_image_filename)

        print("[INFO][LabelCutter::cutAllImage]")
        print("start cut labeled image...")
        for cut_image_xml_filename in tqdm(cut_image_xml_filename_list):
            cut_image_xml_basename = cut_image_xml_filename[:-4]
            if not self.cutImage(cut_image_xml_basename, image_format):
                continue
        return True

def demo():
    source_image_folder_path = "/home/chli/yolo/test/1/"
    cut_image_save_path = "/home/chli/yolo/test/2/"
    cut_by_label_list = ["Container"]
    cut_save_label_list = ["Drop"]
    image_format = ".jpg"

    label_cutter = LabelCutter()
    label_cutter.setCutInfo(source_image_folder_path,
                         cut_image_save_path,
                         cut_by_label_list,
                         cut_save_label_list)
    label_cutter.cutAllImage(image_format)
    return True

if __name__ == "__main__":
    demo()

