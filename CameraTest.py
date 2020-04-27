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
import time
import os

def test():
    
    # get the camera information through the pyflycapture2
    print fc2.get_library_version()
    c = fc2.Context()
    print("number of camera is %d" %c.get_num_of_cameras())
#    print c.get_num_of_cameras()

    ## select the index zero camera
    num = 0
    c.connect(*c.get_camera_from_index(num))
    print("%d Camera is selected." %(num+1))
    print('')
    print("[Camera information]")
    print c.get_camera_info()
#    c.set_video_mode_and_frame_rate(fc2.VIDEOMODE_, fc2.FRAMERATE_15)
#    c.set_video_mode_and_frame_rate(FC_VIDEOMODE_1280x960Y16, FC_FRAMERATE_15)
    m, f = c.get_video_mode_and_frame_rate()
    print('')    
    print m, f
#    print c.get_video_mode_and_frame_rate_info(m, f)
    print("[Camera property Information]")
    print c.get_property_info(fc2.FRAME_RATE)
    print('')
    p = c.get_property(fc2.FRAME_RATE)
    print("[Camera Property]")
    print p
    print('')
    c.set_property(**p)
    c.start_capture()
	
    # video writer setting
    ## video save path
    if not os.path.exists("./saved_video") :
		os.makedirs("./saved_video")
    t = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    ## saved video parameter setting(15frames per sec, resolution(960, 600))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('./saved_video/'+ t + '.avi', fourcc, 15.0, (960, 600))
    
    # set time variable to get the frame rate
    te = 0

    # show and save the image
    while True :
	
	# get the image from the Gige Camera	
	im = fc2.Image()
	c.retrieve_buffer(im)
	a = np.array(im)
	## change the image channel to 3(BGR)
        b = cv2.cvtColor(a, cv2.COLOR_BAYER_BG2BGR)
        
	# get the frame rate
	ts = time.time()
        sec = ts - te
 	te = time.time()
        fps = 1/(sec)	
        ## write the frame rate on image
	cv2.putText(b, 'FPS : %.2f' %(fps), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)	
	# show the image
	cv2.imshow('x', b)
	# save the image
	out.write(b)
	
	# set the break point
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
