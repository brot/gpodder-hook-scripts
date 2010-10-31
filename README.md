Summary
=======

"Tin Foil Hat Show" is a podcast produced by CafeNinja.
http://cafeninja.blogspot.com/search/label/tinfoilhat

There is one special thing in this show. The show notes are hide in the FRONT_COVER image which is included in the mp3 file. This is the only place where you can find the show notes. So you have to run a few commands until you are able to read the notes.

This is the reason why I created some hooks to get this show notes automatically after I downloaded an episode with gPodder (http://gpodder.org/)

This github repository includes two options to configure your gPodder installation with this feature.

Requirements
------------

First you have to take care that all required programs and libraries are installed on your system

- python-eyed3

  Homepage: http://eyed3.nicfit.net/

  eyeD3 is a Python module and program for processing ID3 tags

- steghide

  Homepage: http://steghide.sourceforge.net/

  Steghide is a steganography program that is able to hide data in various kinds of image- and audio-files. 


gPodder hooks infrastructure (recommended way)
----------------------------------------------

### What are hooks in gPodder?

Hooks are python scripts in ~/.config/gpodder/hooks. Each script must define a class named "gPodderHooks", otherwise it will be ignored.

### How to configure

You could copy the script `tfh_shownotes_hook.py` to ~/.config/gpodder/hooks/ and everything should work fine.


gPodder post-download script hook
---------------------------------

### What is the post-download script hook in gPodder?

In the advanced configuration gui of gPodder you could define a script which is started after a download is finished

## How to configure

- Open the advanced configuration gui in gPodder
- Search for the "cmd_download_complete" variable
- Fill in the full path to the "tfh_shownotes_script.py" script 
