#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Method.label_cutter import LabelCutter

if __name__ == "__main__":
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

