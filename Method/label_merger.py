#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import xml.etree.ElementTree as ET
from tqdm import tqdm

from Method.image_object import ImageObject
from Method.xml_builder import XMLBuilder

class LabelMerger(object):
    def __init__(self):
        self.source_image_folder_path = None
        self.merge_image_save_path = None
        self.merge_save_label_list = None
        self.merge_row_image_num = None
        self.merge_col_image_num = None
        self.is_row_merge_first = None

        self.root_list = []
        self.image_list = []
        return

    def setSourceImageFolderPath(self, source_image_folder_path):
        if not os.path.exists(source_image_folder_path):
            print("[ERROR][LabelMerger::setSourceImageFolderPath]")
            print("\t source_image_folder_path not exist!")
            return False
        self.source_image_folder_path = source_image_folder_path
        if self.source_image_folder_path[-1] != "/":
            self.source_image_folder_path += "/"
        return True

    def setMergeImageSavePath(self, merge_image_save_path):
        self.merge_image_save_path = merge_image_save_path
        if self.merge_image_save_path[-1] != "/":
            self.merge_image_save_path += "/"

        if not os.path.exists(self.merge_image_save_path):
            os.makedirs(self.merge_image_save_path)
        return True

    def setMergeInfo(self,
                     source_image_folder_path,
                     merge_image_save_path,
                     merge_save_label_list,
                     merge_row_image_num,
                     merge_col_image_num,
                     is_row_merge_first):
        '''
        Input :
            source_image_folder_path : str
            merge_image_save_path : str
            merge_save_label_list : [merge_save_label_1, merge_save_label_2, ...]
            merge_row_image_num : int
            merge_col_image_num : int
            is_row_merge_first : bool
        '''
        if not self.setSourceImageFolderPath(source_image_folder_path):
            print("[ERROR][LabelMerger::setMergeInfo]")
            print("\t setSourceImageFolderPath failed!")
            return False

        if not self.setMergeImageSavePath(merge_image_save_path):
            print("[ERROR][LabelMerger::setMergeInfo]")
            print("\t setMergeImageSavePath failed!")
            return False

        self.merge_save_label_list = merge_save_label_list
        self.merge_row_image_num = merge_row_image_num
        self.merge_col_image_num = merge_col_image_num
        self.is_row_merge_first = is_row_merge_first
        return True

    def clearImage(self):
        self.root_list = []
        self.image_list = []
        return True

    def loadXML(self, xml_file_basename, image_format):
        '''
        Input :
            xml_file_basename
            image_format
        '''
        self.xml_file_basename = xml_file_basename

        xml_file_path = self.source_image_folder_path + self.xml_file_basename + ".xml"
        if not os.path.exists(xml_file_path):
            print("[ERROR][LabelMerger::loadXML]")
            print("\t xml_file not exist in source_image_folder_path!")
            return False

        image_file_path = self.source_image_folder_path + self.xml_file_basename + image_format
        if not os.path.exists(image_file_path):
            print("[ERROR][LabelMerger::loadXML]")
            print("\t image_file not exist in source_image_folder_path!")
            return False

        tree = ET.parse(xml_file_path)
        self.root_list.append(tree.getroot())
        self.image_list.append(cv2.imread(image_file_path))
        return True

    def getObjectList(self, root_idx):
        '''
        Input :
            root_idx : int
        Return :
            [ImageObject(), ...]
        '''
        if root_idx >= len(self.root_list):
            print("[ERROR][LabelMerger::getObjectList]")
            print("\t root_idx out of range!")
            return None

        root = self.root_list[root_idx]

        if root is None:
            print("[ERROR][LabelMerger::getObjectList]")
            print("\t not load any xml file!")
            return None

        object_list = []

        for obj in root.iter('object'):
            name = obj.find('name').text
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)

            obj = ImageObject(name, xmin, ymin, xmax, ymax)
            object_list.append(obj)
        return object_list

    def getObjectListWithLabel(self, root_idx, label_list):
        '''
        Input :
            root_idx : int
            label_list : [label_1, label_2, ...]
        Return :
            [ImageObject(), ...]
        '''
        if root_idx >= len(self.root_list):
            print("[ERROR][LabelMerger::getObjectListWithLabel]")
            print("\t root_idx out of range!")
            return None

        root = self.root_list[root_idx]

        if root is None:
            print("[ERROR][LabelMerger::getObjectListWithLabel]")
            print("\t not load any xml file!")
            return None

        if label_list is None:
            print("[WARN][LabelMerger::getObjectListWithLabel]")
            print("\t label_list is empty!")
            return []

        object_list_with_label = []

        for obj in root.iter('object'):
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

    def mergeImage(self, )
