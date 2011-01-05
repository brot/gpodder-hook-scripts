#!/usr/bin/python
# -*- coding: utf-8 -*-
####
# 10/2010 Bernd Schlapsi <brot@gmx.info>
#
# This script is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# gPodder is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Dependencies:
# * python-eyed3 (eyeD3 python library - http://eyed3.nicfit.net/)
# * steghide (steganography program - http://steghide.sourceforge.net/)
#
# you can find the instructions how to extract shownotes
# for the "Tin Foil Hat" podcast here:
# http://cafeninja.blogspot.com/2010/10/tin-foil-hat-show-episode-001.html

import gpodder
import os
import subprocess
import tempfile

from gpodder.liblogger import log

try:
    import eyeD3
except:
    log( '(tfh shownotes hook) Could not find eyeD3')


TFH_TITLE='Tin Foil Hat'

class gPodderHooks(object):
    def __init__(self):
        log('"Tin Foil Hat" shownote extractor extension is initializing.')

    def __extract_image(self, filename):
        """
        extract image from the podcast file
        """
        imagefile = None
        try:
            if eyeD3.isMp3File(filename):
                tag = eyeD3.Mp3AudioFile(filename).getTag()
                images = tag.getImages()
                if images:
                    tempdir = tempfile.gettempdir()
                    img = images[0]
                    imagefile = img.getDefaultFileName()
                    img.writeFile(path=tempdir, name=imagefile)
                    imagefile = "%s/%s" % (tempdir, imagefile)
                else:
                    log(u'No image found in %s' % filename)
        except:
            pass

        return imagefile

    def __extract_shownotes(self, imagefile):
        """
        extract shownotes from the FRONT_COVER.jpeg
        """
        shownotes = None
        password = 'tinfoilhat'
        shownotes_file = '/tmp/shownotes.txt'

        myprocess = subprocess.Popen(['steghide', 'extract', '-f', '-p', password,
            '-sf', imagefile, '-xf', shownotes_file],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = myprocess.communicate()

        os.remove(imagefile)

        if stderr.startswith('wrote extracted data to'):
            #read shownote file
            f = open(shownotes_file)
            shownotes = f.read()
            f.close()
        else:
            log(u'Error extracting shownotes from the image file %s' % imagefile)

        return shownotes

    #def on_episode_save(self, episode):
    #    log(u'on_episode_save(%s)' % episode.title)
    #    self.on_episode_downloaded(episode)

    def on_episode_downloaded(self, episode):
        log(u'on_episode_downloaded(%s/%s)' % (episode.channel.title, episode.title))

        if episode.channel.title == TFH_TITLE:
            filename = episode.local_filename(create=False, check_only=True)
            if filename is None:
                return
            
            imagefile = self.__extract_image(filename)
            if imagefile is None:
                return

            shownotes = self.__extract_shownotes(imagefile)
            if shownotes is None:
                return

            # save shownotes in the database
            if episode.description.find(shownotes) == -1:
                episode.description = "%s\n\n<pre>%s</pre>" % (episode.description, shownotes)
                episode.save()
