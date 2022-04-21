#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

from Method.image_object import ImageObject

class XMLBuilder(object):
    def __init__(self):
        self.root = None
        return

    def initXML(self):
        self.root = None
        self.root = ET.Element("annotation")

        folder = ET.SubElement(self.root, "folder")
        folder.text = "test"

        source = ET.SubElement(self.root, "source")
        database = ET.SubElement(source, "database")
        database.text = "Unknown"

        segmented = ET.SubElement(self.root, "segmented")
        segmented.text = "0"
        return True

    def setImageFilePath(self, image_file_path):
        image_file_path_split_list = image_file_path.split("/")
        image_file_name = image_file_path_split_list[-1]

        filename = ET.SubElement(self.root, "filename")
        filename.text = image_file_name

        path = ET.SubElement(self.root, "path")
        path.text = image_file_path
        return True

    def setImageSize(self, image_width, image_height, image_depth):
        size = ET.SubElement(self.root, "size")
        width = ET.SubElement(size, "width")
        width.text = str(image_width)
        height = ET.SubElement(size, "height")
        height.text = str(image_height)
        depth = ET.SubElement(size, "depth")
        depth.text = str(image_depth)
        return True

    def addObject(self, obj):
        new_object = ET.SubElement(self.root, "object")

        name = ET.SubElement(new_object, "name")
        name.text = obj.name

        pose = ET.SubElement(new_object, "pose")
        pose.text = "Unspecified"

        truncated = ET.SubElement(new_object, "truncated")
        truncated.text = "0"

        difficult = ET.SubElement(new_object, "difficult")
        difficult.text = "0"

        bndbox = ET.SubElement(new_object, "bndbox")

        xmin = ET.SubElement(bndbox, "xmin")
        xmin.text = str(obj.bbox[0])

        ymin = ET.SubElement(bndbox, "ymin")
        ymin.text = str(obj.bbox[1])

        xmax = ET.SubElement(bndbox, "xmax")
        xmax.text = str(obj.bbox[2])

        ymax = ET.SubElement(bndbox, "ymax")
        ymax.text = str(obj.bbox[3])
        return True

    def prettyXml(self, element, indent="\t", newline="\n", level=0):
        if element:
            if element.text == None or element.text.isspace():
                element.text = newline + indent * (level + 1)
            else:
                element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
        temp = list(element)
        for subelement in temp:
            if temp.index(subelement) < (len(temp) - 1):
                subelement.tail = newline + indent * (level + 1)
            else:
                subelement.tail = newline + indent * level
            self.prettyXml(subelement, indent, newline, level = level + 1)
        return True

    def saveXML(self, xml_file_path):
        self.prettyXml(self.root)

        tree = ET.ElementTree(self.root)
        tree.write(xml_file_path, encoding="utf-8")
        return True

def demo():
    image_file_path = "/home/chli/yolo/test/1/0_0.jpg"
    image_width = 1920
    image_height = 1080
    image_depth = 3
    save_xml_file_path = "/home/chli/yolo/test/1/0_0.xml"

    xml_builder = XMLBuilder()
    xml_builder.initXML()
    xml_builder.setImageFilePath(image_file_path)
    xml_builder.setImageSize(image_width, image_height, image_depth)

    image_object = ImageObject("target", 10, 10, 100, 100)
    xml_builder.addObject(image_object)

    xml_builder.saveXML(save_xml_file_path)
    return True

if __name__ == "__main__":
    demo()

