#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from Method.image_format_switcher import switchImageFormat
from Method.label_cutter import LabelCutter
from Method.label_merger import LabelMerger
from Method.yolo_builder import YOLOBuilder

def demo():
    # Param
    source_folder_path = "/home/chli/chLi/Download/DeepLearning/Dataset/WaterDrop/20220419_cap/rgb_data/1_1/"
    target_folder_path = "/home/chli/waterdrop_data/1_1/"

    source_format = ".png"
    target_format = ".png"

    cut_by_label_list = ["container"]
    cut_save_label_list = ["drop"]

    merge_save_label_list = ["drop"]
    merge_row_image_num = 4
    merge_col_image_num = 4
    is_row_merge_first = True
    merge_image_num = 16
    merge_image_time = 300 * 16

    classes = ["container", "drop", "zbar"]

    # Algorithm
    target_image_folder_path = \
        target_folder_path + target_format.split(".")[1] + "/"

    if source_format != target_format:
        switchImageFormat(source_folder_path,
                          source_format,
                          target_image_folder_path,
                          target_format)
    else:
        target_image_folder_path = source_folder_path

    label_cutter = LabelCutter()
    label_cutter.setCutInfo(target_image_folder_path,
                            target_folder_path + "cut/",
                            cut_by_label_list,
                            cut_save_label_list)
    label_cutter.cutAllImage(target_format)

    label_merger = LabelMerger()
    label_merger.setMergeInfo(target_folder_path + "cut/",
                              target_folder_path + "merge/",
                              merge_save_label_list,
                              merge_row_image_num,
                              merge_col_image_num,
                              is_row_merge_first)
    label_merger.mergeAllImage(merge_image_num,
                               merge_image_time,
                               target_format)
 
    yolo_builder = YOLOBuilder()
    yolo_builder.setVOCInfo(classes,
                            target_folder_path + "merge/",
                            target_folder_path + "yolo/")
    yolo_builder.transLabel(target_format)
    return True

def demo_multi():
    # Param
    source_folder_root = "/home/chli/chLi/Download/DeepLearning/Dataset/WaterDrop/20220419_cap/rgb_data/"
    source_folder_name_list = os.listdir(source_folder_root)
    target_folder_root = "/home/chli/waterdrop_data/"

    source_format = ".png"
    target_format = ".png"

    cut_by_label_list = ["container"]
    cut_save_label_list = ["drop"]

    merge_save_label_list = ["drop"]
    merge_row_image_num = 4
    merge_col_image_num = 4
    is_row_merge_first = True
    merge_image_num = 16
    merge_image_time = 300 * 16

    classes = ["container", "drop", "zbar"]

    # Algorithm
    all_folder_exist = True
    for source_folder_name in source_folder_name_list:
        source_folder_path = source_folder_root + source_folder_name + "/"
        if not os.path.exists(source_folder_path):
            all_folder_exist = False
            print("[ERROR][auto_cut_and_merge::demo_multi]")
            print("\t folder [" + source_folder_name + "] not exist!")

    if not all_folder_exist:
        return False

    for source_folder_name in source_folder_name_list:
        source_folder_path = source_folder_root + source_folder_name + "/"
        target_folder_path = target_folder_root + source_folder_name + "/"

        print("[INFO][auto_cut_and_merge::demo_multi]")
        print("\t start trans: " + source_folder_name + " ...")

        target_image_folder_path = \
            target_folder_path + target_format.split(".")[1] + "/"

        if source_format != target_format:
            switchImageFormat(source_folder_path,
                              source_format,
                              target_image_folder_path,
                              target_format)
        else:
            target_image_folder_path = source_folder_path

        label_cutter = LabelCutter()
        label_cutter.setCutInfo(target_image_folder_path,
                                target_folder_path + "cut/",
                                cut_by_label_list,
                                cut_save_label_list)
        label_cutter.cutAllImage(target_format)

        label_merger = LabelMerger()
        label_merger.setMergeInfo(target_folder_path + "cut/",
                                  target_folder_path + "merge/",
                                  merge_save_label_list,
                                  merge_row_image_num,
                                  merge_col_image_num,
                                  is_row_merge_first)
        label_merger.mergeAllImage(merge_image_num,
                                   merge_image_time,
                                   target_format)
     
        yolo_builder = YOLOBuilder()
        yolo_builder.setVOCInfo(classes,
                                target_folder_path + "merge/",
                                target_folder_path + "yolo/")
        yolo_builder.transLabel(target_format)

    merge_train_txt_path = target_folder_root + "train.txt"
    with open(merge_train_txt_path, "w") as f:
        for source_folder_name in source_folder_name_list:
            target_folder_path = target_folder_root + source_folder_name + "/"
            with open(target_folder_path + "yolo/train.txt", "r") as fr:
                for line in fr.readlines():
                    f.write(line)
    return True

if __name__ == "__main__":
    #  demo()
    demo_multi()

