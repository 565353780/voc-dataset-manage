#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method.label_cutter import LabelCutter

def demo():
    source_image_folder_path = "/home/chli/yolo/test/1_png/"
    cut_image_save_path = "/home/chli/yolo/test/2/"
    cut_by_label_list = ["container"]
    cut_save_label_list = ["drop"]
    image_format = ".png"

    label_cutter = LabelCutter()
    label_cutter.setCutInfo(source_image_folder_path,
                         cut_image_save_path,
                         cut_by_label_list,
                         cut_save_label_list)
    label_cutter.cutAllImage(image_format)
    return True

if __name__ == "__main__":
    demo()

