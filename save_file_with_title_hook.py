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
#

import os
import gpodder
from gpodder.util import sanitize_filename 
from gpodder.liblogger import log


class gPodderHooks(object):
    def __init__(self):
        log('save episode title to file extension is initializing.')

    def on_episode_downloaded(self, episode):
        log(u'on_episode_downloaded(%s/%s)' % (episode.channel.title, episode.title))

        filename = episode.local_filename(create=False, check_only=True)
        if filename is None:
            return

        save_title = sanitize_filename(episode.title)
        (path, fn) = os.path.split(filename)
        basename, extension = os.path.splitext(fn)
        new_filename = "%s%s" % (save_title, extension)
        new_file= os.path.join(path, new_filename)

        ## check if file exists before renaming
        os.rename(filename, new_file)
        log(u'---------------------------: %s' % episode.filename)
        log(u'---------------------------: %s' % new_filename)
        log(u'---------------------------: %s' % new_file)

        ## update filename in the sqlite-db (table: episodes, column: filename (without path, only filename))
        episode.filename = new_filename
        episode.save()
        episode.db.commit()

        log(u'---------------------------: %s' % episode.local_filename(create=False, check_only=True))

        ## wird aber mit alten Namen auf den MediaPlayer gespielt :-(
