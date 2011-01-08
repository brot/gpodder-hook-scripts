# Summary

This repository contains gPodder hook scripts which I use for myself. Please feel free to fork or use this repository for your own purpose.

## gPodder hooks infrastructure (recommended way)

### What are hooks in gPodder?

Hooks are python scripts in ~/.config/gpodder/hooks. Each script must define a class named "gPodderHooks", otherwise it will be ignored.

### How to configure

You could copy or link the scripts in this repository to ~/.config/gpodder/hooks/ and everything should work fine.


# Hooks list

## tfh_shownotes_hook

"Tin Foil Hat Show" is a podcast produced by CafeNinja.
http://cafeninja.blogspot.com/search/label/tinfoilhat

There is one special thing in this show. The show notes are hide in the FRONT_COVER image which is included in the mp3 file. This is the only place where you can find the show notes. So you have to run a few commands until you are able to read the notes.

This is the reason why I created some hooks to get this show notes automatically after I downloaded an episode with gPodder (http://gpodder.org/)

This github repository includes two options to configure your gPodder installation with this feature.

### Requirements

- python-eyed3

  Homepage: http://eyed3.nicfit.net/

  eyeD3 is a Python module and program for processing ID3 tags

- steghide

  Homepage: http://steghide.sourceforge.net/

  Steghide is a steganography program that is able to hide data in various kinds of image- and audio-files. 


## rm_ogg_coover_hook

This hook scripts removes coverart from all downloaded ogg files.
The reason for this script is that my media player (MEIZU SL6) could not handle ogg files with included coverart. 

### Requirements

- python-mutagen

  Homepage: http://code.google.com/p/mutagen/

  Mutagen is a Python module to handle audio metadata.

## bittorrent

Automatically open .torrent files with a BitTorrent client.

## mp3split

Split mp3 files in ranges of 10 minutes when the files are copied to the device.

### Requirements

- mp3splt binary on the path.

  Homepage: http://mp3splt.sourceforge.net/
