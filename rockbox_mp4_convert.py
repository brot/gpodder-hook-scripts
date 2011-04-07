#!/usr/bin/python
# -*- coding: utf-8 -*-
# Requirements: apt-get install python-kaa-metadata  ffmpeg python-dbus
# To use, copy it as a Python script into ~/.config/gpodder/hooks/rockbox_mp4_convert.py
# See the module "gpodder.hooks" for a description of when each hook
# gets called and what the parameters of each hook are.
#Based on Rename files after download based on the episode title
#And patch in Bug https://bugs.gpodder.org/show_bug.cgi?id=1263
# Copyright (c) 2011-04-06 Guy Sheffer <guysoft at gmail.com>
# Copyright (c) 2011-04-04 Thomas Perl <thp.io>
# Licensed under the same terms as gPodder itself

DEFAULT_DEVICE_WIDTH = 224.0 #make sure to include the .0, this is a float
DEFAULT_DEVICE_HEIGHT = 176.0
ROCKBOX_EXTENTION = "mpg"
EXTENTIONS_TO_CONVERT = ['.mp4',"." + ROCKBOX_EXTENTION] 
FFMPEG_OPTIONS = '-vcodec mpeg2video -b 500k -ab 192k -ac 2 -ar 44100 -acodec libmp3lame'

from gpodder import util
import os
import os.path

import kaa.metadata
#import subprocess
import time

import dbus #For onscreen messages

#create a session 
bus = dbus.SessionBus()

#Get the required notification service
notify_service = bus.get_object('org.freedesktop.Notifications', \
        '/org/freedesktop/Notifications')

#interface for a message
notify_interface = dbus.Interface(notify_service, \
        'org.freedesktop.Notifications')
def message(title,message):
    '''
    Send a notify message via Dbus
    '''
    notify_interface.Notify("test-notify", 0, '', title, \
        message, [], {}, -1)

def convertMP4(from_file, to_file):
    '''
    Convert MP4 file to rockbox mpg file
    '''
    time.sleep(4)
    
    #input_command = self.decoder_command % input_filename
    #output_command = self.encoder_command % output_filename
    
    if not os.path.isfile(to_file):
        
        print "Converting:" + from_file
        info = kaa.metadata.parse(from_file)
        
        deviceWidth = DEFAULT_DEVICE_WIDTH
        deviceHeight = DEFAULT_DEVICE_HEIGHT
        width = info.video[0].width
        height = info.video[0].height
        
        try:
            if height != None:
                
                destWidth = DEFAULT_DEVICE_WIDTH
                destHeight = DEFAULT_DEVICE_HEIGHT
                
                widthRatio = destWidth/width
                heightRatio = deviceHeight/height
                
                destWidth = deviceWidth
                destHeight = widthRatio*height
                
                if destHeight > deviceHeight:
                    destHeight = deviceHeight
                    destWidth = heightRatio*width
                message('Running conversion script',"Converting  "+ from_file)
                
                convert_command = 'ffmpeg -y -i "' + from_file +'" -s ' + str(int(destWidth))+ 'x' +  str(int(destHeight)) + ' ' + FFMPEG_OPTIONS + ' "' + to_file + '"'
                
                #process = subprocess.Popen(convert_command, stdout=subprocess.PIPE, shell=True)
                os.system(convert_command)
            else:
                raise
        except:
            message('Conversion error',"Could not locate file for Conversion:  "+ from_file)
    return
            
print "RockBox mp4 converter hook loaded"
class gPodderHooks(object):
    def on_episode_downloaded(self, episode):
        
        try:            
            current_filename = episode.local_filename(False)
            
            dirname = os.path.dirname(current_filename)
            filename = os.path.basename(current_filename)
            basename, ext = os.path.splitext(filename)
            
            #print ext + " "+ str(EXTENTIONS_TO_CONVERT)
        except:
            print "Exception!"
            
        if  ext in EXTENTIONS_TO_CONVERT:
            print "Converting"
            #new_filename = util.sanitize_encoding(episode.title) + ext
            
            new_filename = (current_filename[:- len(ext)]) +  "." + ROCKBOX_EXTENTION
            new_filebasename = basename + "." + ROCKBOX_EXTENTION
            
            if filename.endswith(ROCKBOX_EXTENTION):
                tmpFilename= current_filename + ".tmp"
                os.rename(current_filename , tmpFilename)
                current_filename = tmpFilename
                dirname = os.path.dirname(current_filename)
                filename = os.path.basename(current_filename)
                basename, ext = os.path.splitext(filename)
                            
            
                
            print 'Renaming:', filename, '->', new_filename
    
            destination_filename = os.path.join(dirname, new_filename)
            
            convertMP4(current_filename, destination_filename)
            
            #os.rename(current_filename, destination_filename)
            
            episode.filename = os.path.basename(destination_filename)
            episode.save()
            os.remove(current_filename)
            print "done converting!"
        else:
            print "Not converting"

