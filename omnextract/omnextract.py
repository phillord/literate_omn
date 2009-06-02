#!/usr/bin/env python

import sys
import re

def main( argv ):
    
    document = Document( argv[ 1 ] )

    ## add the relevant macros
    OwlMacro( document )
    document.render()
    output = open( argv[ 2 ], "w" )
    output.write( document.get_output() )
    

## support classes
class Document:
    '''
    
    '''

    ## filename to start with
    ## list of macros
    ## list of environments to deal with.
    def __init__(self, filename):
        '''
        A document is created by supplying a filename
        '''
        self.enviroment_stack = {}
        self.filename = filename

        self.macrodict = {}
        InputMacro(self)

        self.environdict = {}
    
        ## two special macros which define an environment
        BeginEnvironmentMacro(self)
        EndEnvironmentMacro(self)
        self.output = ""
        

    def add_macro(self, macro):
        self.macrodict[ macro.get_macroname() ] = macro
        
    def has_macro(self, macroname):
        return macroname in self.macrodict
    
    def get_macro(self, macroname):
        return self.macrodict[ macroname ]

    def add_environment(self, environment):
        self.environdict[ environment.get_environname() ] = environment 

    def has_environment(self, environname):
        return environname in self.environdict
    
    def get_environment(self, environname):
        return self.environdict[ environname ]

    ## main method that starts it all off..
    def render(self):
        self.get_macro("input").render(self.filename, self.output)

    def render_file(self, filename):

        ## read the entire file contents
        finputcontent = open( filename ).read()
        ## search for macro
        ## this doesn't do optional arguments at the moment. 
        p = re.compile("\\\\(\w*)\\{([\w.]*)\\}")
        for m in p.finditer( finputcontent ):
            macroname = m.group( 1 )
            macroarg = m.group( 2 )
            if( self.has_macro(macroname) ):
                self.get_macro(macroname).render(macroarg,self.output)

    def get_output(self):
        return self.output
    
    def add_output(self,line):
        self.output = self.output + line
        
class Macro:
    def __init__(self, document, macroname):
        self.macroname = macroname
        self.document = document
        document.add_macro( self )
        
    def get_macroname(self):
        return self.macroname

    def render(self,argument,output):
        pass
    
    def get_document(self):
        return self.document

class Environment:
    def __init__(self, document, environname):
        self.environname = environname
        self.document = document
        document.add_environment( self )

    def get_environname(self):
        return self.environname

    def render(self,beginp,output):
        pass
    
class InputMacro(Macro):
    def __init__(self, document):
        Macro.__init__(self, document, "input")

    def render(self, argument, output):
        self.document.render_file( argument )

## the macro that defines "start of environment"
class BeginEnvironmentMacro(Macro):
    def __init__(self, document):
        Macro.__init__(self, document, "begin")
        self.document = document
        
    def render(self, argument, output):
        if( self.document.has_environment(argument) ):
            self.document.get_environment(argument).render(true, output)

class EndEnvironmentMacro(Macro):
    def __init__(self, document):
        Macro.__init__(self, document, "end")

    def render(self, argument, output):
        if( self.document.has_environment(argument) ):
            self.document.get_environment(argument).render(false, output)


## the owldoc macros
class OwlMacro(Macro):
    def __init__(self, document):
        Macro.__init__(self,document,"owl")

    def render(self, argument, output):
        ## read the file in and dump it out!
        finputcontent = open( argument ).read()
        self.document.add_output( finputcontent + "\n" )
        

main(sys.argv)

    

