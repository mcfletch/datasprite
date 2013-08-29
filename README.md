datasprite
==========

OpenGL-based log-file visualizer

Created in a Toronto Python Meetup Hack Night, this script views the 
time-of-day vs. transferred file size for a sample apache log file.

    ftp://ita.ee.lbl.gov/traces/epa-http.txt.Z
    
Which must be uncompressed into 'epa-http.txt', on a Linux machine:

    $ wget ftp://ita.ee.lbl.gov/traces/epa-http.txt.Z
    $ uncompress epa-http.txt.Z

Installation
---------------

    virtualenv --system-site-packages -p python2.7 datasprite-env
    source datasprite-env/bin/activate
    pip install -r datasprite/requirements.txt 

Install FontTools manually (doesn't currently work with pip):

    $ wget -o fonttools-2.3.tar.gz http://downloads.sourceforge.net/project/fonttools/2.3/fonttools-2.3.tar.gz?r=&ts=1377749010
    $ tar -zxvf fonttools-2.3.tar.gz
    $ cd fonttools-2.3
    $ python setup.py install

The script uses PyOpenGL and OpenGLContext to do the rendering of the data-set, 
and currently just renders a sliding window of data as the script parses the 
log-file with a per-line delay.
