#!/usr/bin/env python

import sys
import re
import fileinput
import os


def main( filename ):
    omnowldoc = OmnOwlDoc( filename )
    omnowldoc.split()
    OmnDocTexReport( omnowldoc ).write_text_report()


class OmnDocTexReport:
    def __init__(self, omnowldoc):
        self.omnowldoc = omnowldoc 

    def get_tex_report(self):

        line = "";

        entity_no = str( len( self.omnowldoc.get_entities() ) )
        subentity_no = {}
        for i in self.omnowldoc.get_entities():
            if i.get_type() in subentity_no:
                subentity_no[ i.get_type() ] = \
                   subentity_no[ i.get_type() ] + 1
            else:
                subentity_no[ i.get_type() ] = 1

        line = line +  "\OmnEntityNoSet{" + \
               entity_no + "}\n"

        line = line + "\OmnEntityFileNameSet{" + \
               self.omnowldoc.get_filename() + "}\n"

        for i in subentity_no.keys():
            line = line + "\OmnEntitySet" + i + "{" \
               + str( subentity_no[ i ] ) + "}\n"


        return line
        

    def write_text_report(self):

        filestem = self.omnowldoc.get_filename().split( "." )[ 0 ]
        output = open( filestem + "_summary.spt", "w" )
        output.write( self.get_tex_report() )
        
    

class OmnOwlDoc:
    def __init__(self, filename):
        self.entities = []
        self.filename = filename
        
    def add_entity(self, entity):
        self.entities.append( entity )

    def get_entities(self):
        return self.entities

    def get_filename(self):
        return self.filename

    def split(self):
        entities = ["Class:", "ObjectProperty:", "Individual:", "DataProperty:" ]

        regexp = "^(" + " |".join( entities ) + " )([\w:]*)"

        splitre = re.compile( regexp )

        labelre = re.compile( r'rdfs:label "(.*)"' )
        
        current_entity = OmnEntity( "Header", "", "header" )
        self.add_entity( current_entity )
        
        for line in fileinput.input( self.filename ):
            line = line.rstrip() 

            ## check for new entity
            match = splitre.match( line )
            if( match ):
                entitytype = match.group( 1 )
                entityfullname = match.group( 2 )

                ## split the name space of
                splitfullname = entityfullname.split(":")
                if( len( splitfullname ) == 1 ):
                    entitynamespace = ""
                    entityname = entityfullname
                else:
                    entitynamespace = splitfullname[0]
                    entityname = splitfullname[1]


                ## remove the ": " from the end of the type
                current_entity = OmnEntity( entitytype[:-2], entitynamespace,
                                        entityname )
                self.add_entity( current_entity )
            
            matchlabel = labelre.search( line )
            if( matchlabel ):
                current_entity.set_label( matchlabel.group( 1 ) )

            current_entity.add_definition( line )

        for i in self.get_entities():
            output = open( i.get_type() + "_" + i.get_namespace()
                           + "!" + i.get_stated_name() + ".pomn", "w" )
            output.write( i.get_definition() )


class OmnEntity:
    label_manipulate = re.compile( " " )
    
    def __init__(self, type, namespace, name):
        self.type = type
        self.name = name
        self.label = ""
        self.namespace = namespace
        self.definition = ""

    def get_type(self):
        return self.type

    def get_namespace(self):
        return self.namespace

    def get_name(self):
        return self.name

    def add_definition(self, line):
        self.definition = self.definition + line + "\n"

    def get_definition(self):
        return self.definition.rstrip()

    def get_label(self):
        return self.label

    def set_label(self, label):
        self.label = label

    def get_stated_name(self):
        if( self.label ):
            name = OmnEntity.label_manipulate.sub( "_", self.label )
            if( len( name ) > 50 ):
                return name[:50]
            else:
                return name
            

            
        return self.name
    
        

if( __name__ == "__main__" ):
    main( sys.argv[ 1 ] )





