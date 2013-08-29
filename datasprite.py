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
from OpenGLContext.events.timer import Timer

class TestContext( BaseContext ):
    initialPosition = (0,0,3) # set initial camera position, tutorial does the re-positioning
    def OnInit( self ):
        """Load the image on initial load of the application"""
        print """Should see a sine wave fading from green to red"""
        self.log_queue = Queue.Queue( maxsize=600 )
        line = arange(0.0,1.0,.01)
        line2 = line[::-1]
        self.coordinate = Coordinate(
            point = [(0,0,0)]*600,
        )
        ymax = max(self.coordinate.point[:,1]) or 1
        self.color = Color(
            color = [1.0,0.0,0.0],
        )
        self.transform = Transform(
                    translation = (-.5,0,0),
                    scale = (1/3600.,1./5,0.0),
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
        self.transform.translation = (-new[0][0]/3600.) - .5,0,0
        self.triggerRedraw()
    
def log_reader( filename, queue ):
    """On event from the timer, generate new geometry"""
    for record in _log_reader_gen( filename ):
        queue.put( record, True )
        time.sleep( .01 )
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
    TestContext.ContextMainLoop()
