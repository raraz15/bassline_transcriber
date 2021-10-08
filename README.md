# bassline_transcription

This repository contains an automatic bassline transcriber system that was designed for our Senior Design Project ELEC491 at Koç University, Istanbul / Turkey.

It estimates the beat positions using madmom, detects a drop by our custom algorithm then takes this drop as a chorus section and extracts the bassline using demucs_extra.

The isolated bassline in the beat grid then transcribed using pYIN, confidence filtered. Finally it is adaptively quantized by our custom algorithm and converted to a midi file

where middle C is taken as C4.

How to Use:

1) Run create_directories.py from the project directory.

    It will create the json file that keeps the file structure and create some of the main directories.

2) Put your audio clips to data/audio_clips directory

3) Create a track_dicts.json file

    This file should hold the BPM, key informatin of the tracks.
    An example can be found in data/metadata/track_dicts.json
