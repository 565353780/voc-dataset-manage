#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method.image_format_switcher import switchImageFormat
from Method.label_cutter import LabelCutter
from Method.label_merger import LabelMerger
from Method.yolo_builder import YOLOBuilder

def demo():
    # Param
    source_folder_path = "/home/chli/yolo/test/1/"
    target_folder_path = "/home/chli/yolo/test/1_output/"

    source_format = ".jpg"
    target_format = ".png"

    cut_by_label_list = ["container"]
    cut_save_label_list = ["drop"]

    merge_save_label_list = ["drop"]
    merge_row_image_num = 2
    merge_col_image_num = 5
    is_row_merge_first = True
    merge_image_num = 9
    merge_image_time = 1

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

if __name__ == "__main__":
    demo()

