#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET
from random import randint
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
        xml_file_path = self.source_image_folder_path + xml_file_basename + ".xml"
        if os.path.exists(xml_file_path):
            tree = ET.parse(xml_file_path)
            self.root_list.append(tree.getroot())
        else:
            self.root_list.append(None)

        image_file_path = self.source_image_folder_path + xml_file_basename + image_format
        if not os.path.exists(image_file_path):
            print("[ERROR][LabelMerger::loadXML]")
            print("\t image_file not exist in source_image_folder_path!")
            return False

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
            return []

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
            return []

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

    def getRowFirstImagePositionList(self):
        row_first_image_position_list = []

        image_col_num = int(len(self.image_list) / self.merge_row_image_num)

        last_col_image_num = len(self.image_list) % self.merge_row_image_num
        if last_col_image_num > 0:
            image_col_num += 1

        image_used_width = 0

        for image_col_idx in range(image_col_num):
            current_image_start_idx = image_col_idx * self.merge_row_image_num

            image_used_height = 0

            current_max_image_width = 0
            for i in range(self.merge_row_image_num):
                current_image_idx = current_image_start_idx + i

                if current_image_idx >= len(self.image_list):
                    return row_first_image_position_list

                current_image_shape = self.image_list[current_image_idx].shape

                row_first_image_position_list.append(
                    [image_used_width, image_used_height,
                     image_used_width + current_image_shape[1],
                     image_used_height + current_image_shape[0]])

                image_used_height += current_image_shape[0]

                current_max_image_width = max(
                    current_max_image_width,
                    current_image_shape[1])
            image_used_width += current_max_image_width

        return row_first_image_position_list

    def getColFirstImagePositionList(self):
        col_first_image_position_list = []

        image_row_num = int(len(self.image_list) / self.merge_col_image_num)

        last_row_image_num = len(self.image_list) % self.merge_col_image_num
        if last_row_image_num > 0:
            image_row_num += 1

        image_used_height = 0

        for image_row_idx in range(image_row_num):
            current_image_start_idx = image_row_idx * self.merge_col_image_num

            image_used_width = 0

            current_max_image_height = 0
            for i in range(self.merge_col_image_num):
                current_image_idx = current_image_start_idx + i

                if current_image_idx >= len(self.image_list):
                    return col_first_image_position_list

                current_image_shape = self.image_list[current_image_idx].shape

                col_first_image_position_list.append(
                    [image_used_width, image_used_height,
                     image_used_width + current_image_shape[1],
                     image_used_height + current_image_shape[0]])

                image_used_width += current_image_shape[1]

                current_max_image_height = max(
                    current_max_image_height,
                    current_image_shape[0])
            image_used_height += current_max_image_height

        return col_first_image_position_list

    def getImagePositionList(self):
        if self.merge_row_image_num is None:
            print("[ERROR][LabelMerger::getImagePositionList]")
            print("\t merge_row_image_num is None!")
            return None
        if self.merge_col_image_num is None:
            print("[ERROR][LabelMerger::getImagePositionList]")
            print("\t merge_col_image_num is None!")
            return None
        if self.is_row_merge_first is None:
            print("[ERROR][LabelMerger::getImagePositionList]")
            print("\t is_row_merge_first is None!")
            return None
        if len(self.image_list) == 0:
            print("[WARN][LabelMerger::getImagePositionList]")
            print("\t image_list is empty!")
            return []

        if self.is_row_merge_first:
            return self.getRowFirstImagePositionList()
        return self.getColFirstImagePositionList()

    def mergeImage(self, merge_image_basename, xml_file_basename_list, image_format):
        '''
        Input :
            merge_image_basename : str e.g. "0"
            xml_file_basename_list : [xml_file_basename_1, ...]
            image_format : str e.g. ".png"
        '''
        if len(xml_file_basename_list) == 0:
            print("[ERROR][LabelMerger::mergeImage]")
            print("\t xml_file_basename_list is empty!")
            return False

        if self.merge_save_label_list is None:
            print("[ERROR][LabelMerger::mergeImage]")
            print("\t merge_save_label_list is None!")
            return False
        if self.merge_row_image_num is None:
            print("[ERROR][LabelMerger::mergeImage]")
            print("\t merge_row_image_num is None!")
            return False
        if self.merge_col_image_num is None:
            print("[ERROR][LabelMerger::mergeImage]")
            print("\t merge_col_image_num is None!")
            return False
        if self.is_row_merge_first is None:
            print("[ERROR][LabelMerger::mergeImage]")
            print("\t is_row_merge_first is None!")
            return False

        if not self.clearImage():
            print("[ERROR][LabelMerger::mergeImage]")
            print("\t clearImage failed!")
            return False

        for xml_file_basename in xml_file_basename_list:
            if not self.loadXML(xml_file_basename, image_format):
                print("[ERROR][LabelMerger::mergeImage]")
                print("\t loadXML failed!")
                return False

        image_position_list = self.getImagePositionList()

        if image_position_list is None:
            print("[ERROR][LabelMerger::mergeImage]")
            print("\t getImagePositionList failed!")
            return False

        merge_image_width = 0
        merge_image_height = 0
        merge_image_depth = 3
        for image_position in image_position_list:
            merge_image_width = max(merge_image_width, image_position[2])
            merge_image_height = max(merge_image_height, image_position[3])

        merge_image = np.zeros(
            (merge_image_height, merge_image_width, merge_image_depth),
            dtype=np.uint8)

        merge_object_list = []

        for image_idx in range(len(self.image_list)):
            current_image = self.image_list[image_idx]
            current_image_position = image_position_list[image_idx]

            merge_image[
                current_image_position[1]:current_image_position[3],
                current_image_position[0]:current_image_position[2],
                :] = current_image[:, :, :]

            current_object_list = self.getObjectListWithLabel(image_idx,
                                                              self.merge_save_label_list)

            #  print("image ", image_idx, "have ", len(current_object_list), "objects.")

            for current_object in current_object_list:
                current_merge_object = current_object
                current_merge_object.bbox = current_object.getMovedBBox(current_image_position[0],
                                                                   current_image_position[1])
                merge_object_list.append(current_merge_object)

        merge_image_basepath = self.merge_image_save_path + merge_image_basename

        cv2.imwrite(merge_image_basepath + image_format, merge_image)

        if len(merge_object_list) == 0:
            return True

        xml_builder = XMLBuilder()
        xml_builder.initXML()
        xml_builder.setImageFilePath(merge_image_basepath + image_format)
        xml_builder.setImageSize(merge_image_width, merge_image_height, merge_image_depth)
        for merge_object in merge_object_list:
            xml_builder.addObject(merge_object)

        xml_builder.saveXML(merge_image_basepath + ".xml")
        return True

    def mergeAllImage(self, merge_image_num, merge_image_time, image_format):
        if merge_image_num < 1:
            print("[ERROR][LabelMerger::mergeAllImage]")
            print("\t merge_image_num not valid!")
            return False
        if merge_image_time < 1:
            print("[WARN][LabelMerger::mergeAllImage]")
            print("\t merge_image_time not valid!")
            return True

        merge_image_filename_list = os.listdir(self.source_image_folder_path)
        merge_image_xml_filename_list = []

        #  print("[INFO][LabelMerger::mergeAllImage]")
        #  print("start choose source image...")
        #  for merge_image_filename in tqdm(merge_image_filename_list):
        for merge_image_filename in merge_image_filename_list:
            if merge_image_filename[-4:] != image_format:
                continue
            merge_image_xml_filename_list.append(merge_image_filename)

        if len(merge_image_xml_filename_list) == 0:
            return True

        print("[INFO][LabelMerger::mergeAllImage]")
        print("start merge source image...")
        for i in tqdm(range(merge_image_time)):
            xml_file_basename_list = []
            for _ in range(merge_image_num):
                random_image_idx = randint(0, len(merge_image_xml_filename_list) - 1)
                xml_file_basename_list.append(
                    merge_image_xml_filename_list[random_image_idx][:-4])
            if not self.mergeImage(str(i), xml_file_basename_list, image_format):
                continue
        return True

def demo():
    source_image_folder_path = "/home/chli/yolo/test/1_output/cut/"
    merge_image_save_path = "/home/chli/yolo/test/1_output/merge/"
    merge_save_label_list = ["drop"]
    merge_row_image_num = 2
    merge_col_image_num = 5
    is_row_merge_first = True
    merge_image_num = 9
    merge_image_time = 1
    image_format = ".png"

    label_merger = LabelMerger()
    label_merger.setMergeInfo(source_image_folder_path,
                              merge_image_save_path,
                              merge_save_label_list,
                              merge_row_image_num,
                              merge_col_image_num,
                              is_row_merge_first)
    label_merger.mergeAllImage(merge_image_num,
                               merge_image_time,
                               image_format)
    return True

if __name__ == "__main__":
    demo()

