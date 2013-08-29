datasprite
==========

OpenGL-based log-file visualizer

Created in a Toronto Python Meetup Hack Night, this 
script views the time-of-day vs. transferred file size
for a sample apache log file.

    ftp://ita.ee.lbl.gov/traces/epa-http.txt.Z'
    
Which must be unzipped into 'epa-http.txt'

Installation
---------------

    virtualenv --system-site-packages -p python2.7 datasprite-env
    source datasprite-env/bin/activate
    pip install -r datasprite/requirements.txt 

Install FontTools manually:

    http://downloads.sourceforge.net/project/fonttools/2.3/fonttools-2.3.tar.gz?r=&ts=1377749010

The script using PyOpenGL and OpenGLContext to 
do the rendering of the data-set, and currently just 
renders a sliding window of data as the script
parses the log-file with a per-line delay.
