#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ImageObject(object):
    def __init__(self, name, xmin, ymin, xmax, ymax):
        self.name = name
        self.bbox = [xmin, ymin, xmax, ymax]
        return

    def getTransBBox(self, x_start, y_start):
        return [self.bbox[0] - x_start,
                self.bbox[1] - y_start,
                self.bbox[2] - x_start,
                self.bbox[3] - y_start]

    def haveThisChild(self, target_object):
        '''
        Input:
            ImageObject
        '''
        target_object_bbox = target_object.bbox
        if target_object_bbox[0] >= self.bbox[2] or \
                target_object_bbox[1] >= self.bbox[3] or \
                target_object_bbox[2] <= self.bbox[0] or \
                target_object_bbox[3] <= self.bbox[1]:
            return False
        return True

    def getChild(self, target_object):
        '''
        Input:
            target_object : ImageObject
        Return:
            child_object : ImageObject
            None if union is empty
        '''
        if not self.haveThisChild(target_object):
            return None

        trans_bbox = target_object.getTransBBox(self.bbox[0], self.bbox[1])
        valid_child_bbox = [max(0, trans_bbox[0]),
                            max(0, trans_bbox[1]),
                            min(self.bbox[2] - self.bbox[0], trans_bbox[2]),
                            min(self.bbox[3] - self.bbox[1], trans_bbox[3])]
        child_object = ImageObject(target_object.name,
                                   valid_child_bbox[0],
                                   valid_child_bbox[1],
                                   valid_child_bbox[2],
                                   valid_child_bbox[3])
        return child_object

    def getBBoxImage(self, image):
        bbox_image = image[self.bbox[1]:self.bbox[3], self.bbox[0]:self.bbox[2]]
        return bbox_image

    def outputInfo(self, info_level=0):
        line_start = "\t" * info_level
        print(line_start + "ImageObject:")
        print(line_start + "\t name = " + self.name)
        print(line_start + "\t bbox =", self.bbox)
        return True

