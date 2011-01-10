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
        log('Remove ogg cover extension is initializing.')

    def on_episode_save(self, episode):
        self.on_episode_downloaded(episode)

    def on_episode_downloaded(self, episode):
        log(u'on_episode_downloaded(%s/%s)' % (episode.channel.title, episode.title))

        filename = episode.local_filename(create=False, check_only=True)
        if filename is None:
            return

        save_filename = sanitize_filename(episode.title)
        path, fn = os.path.split(filename)
        basename, extension = os.path.splitext(fn)
        new_filename = os.path.join(path, "%s%s" % (save_filename, extension))

        ## check if file exists before renaming
        #os.rename(filename, new_filename)

        ## update filename in the sqlite-db (table: episodes, column: filename (without path, only filename))
