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
#
#
# you can find the instructions how to extract shownotes
# for the "Tin Foil Hat" podcast here:
# http://cafeninja.blogspot.com/2010/10/tin-foil-hat-show-episode-001.html

import eyeD3
import re
import os
import sys
import subprocess

TFH_TITLE='Tin Foil Hat'

# I use gpodder from git and append the source path to sys.path
sys.path.append('/opt/gpodder/src/')


# extract image from the podcast file
def extract_image(filename):
    imagefile = None
    if eyeD3.isMp3File(filename):
        tag = eyeD3.Mp3AudioFile(filename).getTag()
        images = tag.getImages()
        if images:
            img = images[0]
            imagefile = img.getDefaultFileName()
            img.writeFile(path='/tmp', name=imagefile)
            imagefile = "/tmp/%s" % imagefile
    
    return imagefile


# extract shownotes from the FRONT_COVER.jpeg
def extract_shownotes(imagefile):
    shownotes = None 
    if imagefile:
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

    return shownotes


def write_to_database(shownotes, url):
    if shownotes:
        from gpodder import database_file
        from gpodder import dbsqlite

        # open database and a new cursor
        db = dbsqlite.Database(database_file)
        cur = db.cursor(lock=True)

        # read episode data
        cur.execute("SELECT id, description FROM EPISODES WHERE url = ?", (url, ) )
        (episode_id, desc) = cur.fetchone()
        cur.close()

        # update episode description with added shownotes if they don't exists
        if desc.find(shownotes) == -1:
            desc = "%s\n\n<pre>%s</pre>" % (desc, shownotes)
            cur.execute("UPDATE EPISODES SET description = ? WHERE id = ?", (desc, episode_id, ))
            db.commit()


def main():
    title = os.environ['GPODDER_CHANNEL_TITLE']
    filename = os.environ['GPODDER_EPISODE_FILENAME']
    url = os.environ['GPODDER_EPISODE_URL']

    if title == TFH_TITLE:
        imagefile = extract_image(filename)
        shownotes = extract_shownotes(imagefile)
        write_to_database(shownotes, url)

if __name__=="__main__":
    main()
