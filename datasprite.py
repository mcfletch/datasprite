#! /usr/bin/env python
'''PointSet object test (draw line of coloured dots)
'''
import re
import math
import threading
import time
import Queue
from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()
from OpenGLContext.arrays import *
from math import pi

from OpenGLContext.scenegraph.basenodes import *
from OpenGLContext.scenegraph import boundingvolume
from OpenGLContext.events.timer import Timer

class TestContext( BaseContext ):
    initialPosition = (0,0,10) # set initial camera position, tutorial does the re-positioning
    def OnInit( self ):
        """Load the image on initial load of the application"""
        print """Should see a sine wave fading from green to red"""
        self.log_queue = Queue.Queue( maxsize=600 )
        self.coordinate = Coordinate(
            point = [(0,0,0)]*600,
        )
        boundingvolume.cacheVolume(
            self.coordinate,
            boundingvolume.UnboundedVolume(),
        )
            
        self.fontstyle = FontStyle(
            family='SANS', format = 'bitmap',
            justify = 'BEGIN',
        )
        self.color = Color(
            color = [1.0,0.0,0.0],
        )
        self.data_slider = Transform(
            translation=(0,0,0),
            scale = (1/1800.,1,1,),
            children = [
                Shape(
                    appearance = Appearance(
                        texture = ImageTexture( url='_particle.png' ),
                        material = Material(
                            diffuseColor = [1,0,0],
                        )
                    ),
                    geometry = PointSet(
                        coord = self.coordinate,
                        minSize = 10.0,
                        maxSize = 10.0,
                    ),
                ),
            ],
        )
        self.axes = Transform(
            children = [
                Transform( 
                    translation = (.25,coord,0),
                    children = [
                        Shape( geometry = Text(
                            string = [label],
                            fontStyle = self.fontstyle,
                        ))
                    ],
                )
                for (coord,label) in [
                    (0,'0B'),
                    (3,'1KB'),
                    (6,'1MB'),
                    (9,'1GB'),
                ]
            ]
        )
        self.transform = Transform(
            translation = (.5,-2,0),
            children = [
                self.data_slider,
                self.axes,
            ]
        )
        self.sg = sceneGraph(
            children = [
                self.transform,
            ],
        )
        self.time = Timer( duration = .1, repeating = 1 )
        self.time.addEventHandler( "cycle", self.OnTimerFraction )
        self.time.register (self)
        self.time.start ()
        thread = threading.Thread( target = log_reader, args=('epa-http.txt',self.log_queue))
        thread.setDaemon(True)
        thread.start()
        
    def OnTimerFraction( self, evt ):
        new = []
        try:
            for i in range(len(self.coordinate.point)):
                new.append( self.log_queue.get( False ) )
        except Queue.Empty:
            pass 
        if not new:
            return
        # TODO: new might be bigger than our buffer, stop that
        to_retain = len(self.coordinate.point)-len(new)
        if to_retain:
            self.coordinate.point[:to_retain] = self.coordinate.point[-to_retain:]
        self.coordinate.point[-len(new):] = new
        # trigger new-bounding-box calculation
        boundingvolume.volumeFromCoordinate( self.coordinate )
        self.coordinate.point = self.coordinate.point
        self.data_slider.translation = -new[-1][0]*self.data_slider.scale[0],0,0
        
        self.triggerRedraw()
    
def log_reader( filename, queue ):
    """On event from the timer, generate new geometry"""
    for record in _log_reader_gen( filename ):
        queue.put( record, True )
        time.sleep( .005 )
def _log_reader_gen( filename ):
    date_finder = re.compile( r'[[]\d{2}:(?P<hour>\d{2})[:](?P<minute>\d{2})[:](?P<second>\d{2})[]].*?(?P<size>[-0-9]+)$' )
    def as_size( x ):
        if x == '-':
            return 0
        x =float(x)
        if x:
            x = math.log10(x)
        return x
    for line in open(filename):
        match = date_finder.search( line )
        if match:
            yield (
                float(match.group('hour')) * 3600 + float(match.group('minute')) * 60 + float( match.group('second')),
                as_size(match.group('size')),
                0.0,
            )
        else:
            raise ValueError( line )

def test_log_reader():
    points = list(log_reader( 'epa-http.txt' ))
    assert len(points) == 47748, len(points)

if __name__ == "__main__":
    # needs the data-file from 'ftp://ita.ee.lbl.gov/traces/epa-http.txt.Z' unzipped into 'epa-http.txt'
    TestContext.ContextMainLoop()
