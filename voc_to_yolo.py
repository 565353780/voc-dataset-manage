#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method.yolo_builder import YOLOBuilder

def demo():
    classes = ["container", "drop", "zbar"]
    xml_folder_path = "/home/chli/yolo/test/1_png/"
    save_folder_path = "/home/chli/yolo/test/1_png_yolo/"
    image_format = ".png"

    yolo_builder = YOLOBuilder()
    yolo_builder.setVOCInfo(classes, xml_folder_path, save_folder_path)
    yolo_builder.transLabel(image_format)
    return True

if __name__ == "__main__":
    demo()

