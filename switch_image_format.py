#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Method.image_format_switcher import switchImageFormat

def demo():
    source_image_folder_path = "/home/chli/yolo/test/1/"
    source_format = ".jpg"
    target_image_folder_path = "/home/chli/yolo/test/1_output/png/"
    target_format = ".png"

    switchImageFormat(source_image_folder_path,
                      source_format,
                      target_image_folder_path,
                      target_format)
    return True

if __name__ == "__main__":
    demo()

