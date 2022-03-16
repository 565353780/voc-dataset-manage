#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method.label_merger import LabelMerger

if __name__ == "__main__":
    source_image_folder_path = "/home/chli/yolo/test/1/"
    merge_image_save_path = "/home/chli/yolo/test/3/"
    merge_save_label_list = ["dog"]
    merge_row_image_num = 2
    merge_col_image_num = 5
    is_row_merge_first = True
    merge_image_num = 9
    merge_image_time = 1
    image_format = ".jpg"

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
 
