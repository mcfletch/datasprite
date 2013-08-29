datasprite
==========

OpenGL-based log-file visualizer

Created in a Toronto Python Meetup Hack Night, this 
script views the time-of-day vs. transferred file size
for a sample apache log file.

    ftp://ita.ee.lbl.gov/traces/epa-http.txt.Z'
    
Which must be unzipped into 'epa-http.txt'

The script using PyOpenGL and OpenGLContext to 
do the rendering of the data-set, and currently just 
renders a sliding window of data as the script
parses the log-file with a per-line delay.
