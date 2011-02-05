#!/usr/bin/python
# -*- coding: utf-8 -*-
####
# 01/2011 Bernd Schlapsi <brot@gmx.info>
#
# This script is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
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
# * python-mutagen (Mutagen is a Python module to handle audio metadata)
#
# This hook script adds episode title and podcast title to the audio file
# The episode title is written into the title tag
# The podcast title is written into the album tag

import datetime
import os
import gpodder
from gpodder.liblogger import log

try:
    from mutagen import File 
    mutagen_installed = True
except:
    log( '(tagging hook) Could not find mutagen')
    mutagen_installed = False


## settings
strip_album_from_title = True
genre_tag = u'Podcast'


class gPodderHooks(object):
    def __init__(self):
        log('tagging extension is initializing.')

    def on_episode_downloaded(self, episode):
        log(u'tagging.on_episode_downloaded(%s/%s)' % (episode.channel.title, episode.title))


        # exit if mutagen is not installed
        if not mutagen_installed:
            return

        # read filename (incl. file path) from gPodder database
        filename = episode.local_filename(create=False, check_only=True)
        if filename is None:
            return

        # open file with mutagen
        audio = File(filename, easy=True)
        if audio is None:
            return

        # read title+album from gPodder database
        album = episode.channel.title
        title = episode.title
        if (strip_album_from_title and title and album and title.startswith(album)):
            title = title[len(album):].lstrip()

        # convert pubDate to string
        try:
            pubDate =  datetime.datetime.fromtimestamp(episode.pubDate).strftime('%Y-%m-%d %H:%M')
        except:
            pubDate = None

        # write title+album information into audio files
        if audio.tags is None:
            audio.add_tags()

        if album is not None:
            audio.tags['album'] = album
        if title is not None:
            audio.tags['title'] = title
        if genre_tag is not None:
            audio.tags['genre'] = genre_tag
        if pubDate is not None:
            audio.tags['date'] = pubDate

        audio.save()

