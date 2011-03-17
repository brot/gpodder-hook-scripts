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
# This hook scripts removes coverart from all downloaded ogg files.
# The reason for this script is that my media player (MEIZU SL6) 
# couldn't handle ogg files with included coverart

import os
import gpodder
from gpodder.liblogger import log

try:
    from mutagen.oggvorbis import OggVorbis 
except:
    log( '(remove ogg cover hook) Could not find mutagen')


class gPodderHooks(object):
    def __init__(self):
        log('Remove ogg cover extension is initializing.')

    def on_episode_downloaded(self, episode):
        filename = episode.local_filename(create=False, check_only=True)
        if filename is None:
            return

        (basename, extension) = os.path.splitext(filename)
        if episode.file_type() == 'audio' and extension.lower().endswith('ogg'):
            log(u'trying to remove cover from %s' % filename)
            found = False

            try:
                ogg = OggVorbis(filename)
                for key in ogg.keys():
                    if key.startswith('cover'):
                        found = True
                        ogg[key]=''
                
                if found:
                    log(u'removed cover from the ogg file successfully')
                    ogg.save()
                else:
                    log(u'there was no cover to remove in the ogg file')
            except:
                None
