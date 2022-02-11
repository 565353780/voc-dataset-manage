#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import xml.etree.ElementTree as ET

class LabelCut(object):
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
            print("[ERROR][LabelCut::setSourceImageFolderPath]")
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
            print("[ERROR][LabelCut::setCutInfo]")
            print("\t setSourceImageFolderPath failed!")
            return False

        if not self.setCutImageSavePath(cut_image_save_path):
            print("[ERROR][LabelCut::setCutInfo]")
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
            print("[ERROR][LabelCut::loadXML]")
            print("\t xml_file not exist in source_image_folder_path!")
            return False

        image_file_path = self.source_image_folder_path + self.xml_file_basename + image_format
        if not os.path.exists(image_file_path):
            print("[ERROR][LabelCut::loadXML]")
            print("\t image_file not exist in source_image_folder_path!")
            return False

        tree = ET.parse(xml_file_path)
        self.root = tree.getroot()
        self.image = cv2.imread(image_file_path)
        return True

    def getSize(self):
        '''
        Return :
            [width, height]
        '''
        if self.root is None:
            print("[ERROR][LabelCut::getSize]")
            print("\t not load any xml file!")
            return None

        size = self.root.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)
        return [width, height]

    def getObjectList(self):
        '''
        Return :
            [[name, xmin, ymin, xmax, ymax], ...]
        '''
        if self.root is None:
            print("[ERROR][LabelCut::getObjectList]")
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
            object_list.append([name, xmin, ymin, xmax, ymax])
        return object_list

    def getObjectListWithLabel(self, label_list):
        '''
        Input :
            [label_1, label_2, ...]
        Return :
            [[name, xmin, ymin, xmax, ymax], ...]
        '''
        if self.root is None:
            print("[ERROR][LabelCut::getObjectListWithLabel]")
            print("\t not load any xml file!")
            return None

        if label_list is None:
            print("[WARN][LabelCut::getObjectListWithLabel]")
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
            object_list_with_label.append([name, xmin, ymin, xmax, ymax])
        return object_list_with_label

    def getObjectImage(self, object_bbox):
        '''
        Input :
            [xmin, ymin, xmax, ymax]
        Return :
            object_image
        '''
        if self.image is None:
            print("[ERROR][LabelCut::getObjectImage]")
            print("\t not load any xml file!")
            return None

        xmin, ymin, xmax, ymax = object_bbox

        object_image = self.image[ymin:ymax, xmin:xmax]
        return object_image

    def cutImage(self):
        if self.cut_by_label_list is None:
            print("[ERROR][LabelCut::cutImage]")
            print("\t cut_by_label_list is None!")
            return False
        if self.cut_save_label_list is None:
            print("[ERROR][LabelCut::cutImage]")
            print("\t cut_save_label_list is None!")
            return False

        cut_by_object_list = self.getObjectListWithLabel(self.cut_by_label_list)
        if cut_by_object_list is None:
            print("[ERROR][LabelCut::cutImage]")
            print("\t getObjectListWithLabel for cut_by_label_list failed!")
            return False

        cut_save_object_list = self.getObjectListWithLabel(self.cut_save_label_list)
        if cut_save_object_list is None:
            print("[ERROR][LabelCut::cutImage]")
            print("\t getObjectListWithLabel for cut_save_label_list failed!")
            return False
        return True

    def cutAllImage(self):
        return True

def demo():
    source_image_folder_path = "./1/"
    cut_image_save_path = "./2/"
    cut_by_label_list = ["Container"]
    cut_save_label_list = ["Drop"]

    label_cut = LabelCut()
    label_cut.setCutInfo(source_image_folder_path,
                         cut_image_save_path,
                         cut_by_label_list,
                         cut_save_label_list)
    label_cut.cutAllImage()
    return True

if __name__ == "__main__":
    demo()

