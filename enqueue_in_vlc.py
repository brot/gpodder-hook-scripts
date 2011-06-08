# -*- coding: utf-8 -*-
# Hook script to add a context menu item for enqueueing episodes in a player
# Requirements: gPodder 3.x (or "tres" branch newer than 2011-06-08)
# (c) 2011-06-08 Thomas Perl <thp.io/about>
# Released under the same license terms as gPodder itself.

import gpodder
import subprocess

class gPodderHooks(object):
    def _enqueue_episodes(self, episodes):
        filenames = [episode.get_playback_url() for episode in episodes]
        cmd = ['vlc', '--started-from-file', '--playlist-enqueue'] + filenames
        subprocess.Popen(cmd)

    def on_episodes_context_menu(self, episodes):
        return [('Enqueue in VLC', self._enqueue_episodes)]

