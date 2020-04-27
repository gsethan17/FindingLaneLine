#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#   pyflycapture2 - python bindings for libflycapture2_c
#   Copyright (C) 2012 Robert Jordens <robert@joerdens.org>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import flycapture2 as fc2
import numpy as np
import cv2
import datetime
import os

def test():
    print fc2.get_library_version()
    c = fc2.Context()
    print("number of camera is")
    print c.get_num_of_cameras()

    # select the index zero camera
    c.connect(*c.get_camera_from_index(0))
    print c.get_camera_info()
#    c.set_video_mode_and_frame_rate(fc2.VIDEOMODE_1280x960Y16, fc2.FRAMERATE_15)
    m, f = c.get_video_mode_and_frame_rate()
    print m, f
#    print c.get_video_mode_and_frame_rate_info(m, f)
    print c.get_property_info(fc2.FRAME_RATE)
    p = c.get_property(fc2.FRAME_RATE)
    print p
    c.set_property(**p)
    c.start_capture()
	
    # video writer
    if not os.path.exists("./saved_video") :
		os.makedirs("./saved_video")
    t = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter('./saved_video/'+ t + '.mp4', fourcc, 30.0, (640, 480))

    # show the image
    while 1 :
	
	
	im = fc2.Image()
	c.retrieve_buffer(im)
	a = np.array(im)
        b = cv2.cvtColor(a, cv2.COLOR_BAYER_BG2BGR)
	cv2.imshow('x', b)
	out.write(b)
	if cv2.waitKey(1) & 0xFF == ord('q') :
	    break

#    im = fc2.Image()
#    print [np.array(c.retrieve_buffer(im)).sum() for i in range(80)]
#    a = np.array(im)
    out.release()
    print a.shape, a.base
    c.stop_capture()
    c.disconnect()

if __name__ == "__main__":
    test()
