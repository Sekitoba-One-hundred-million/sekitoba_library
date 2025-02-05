class data_name():
    def __init__( self ):
        self.name_list = {}

    def write( self, file_name ):
        f = open( file_name, "w" )

        for i in range( 0, len( self.name_list ) ):
            f.write( str( i ) + ":" + self.name_list[str(i)] + "\n" )

        f.close()

    def append( self, teacher, data, name ):
        self.name_list[str(len(teacher))] = name
        teacher.append( data )

"""
class split_data_name():
    def __init__( self ):
        self.name_list = {}

    def write( self, key_name ):
        f = open( key_name + ".txt", "w" )

        for i in range( 0, len( self.name_list[key_name] ) ):
            f.write( str( i ) + ":" + self.name_list[key_name][str(i)] + "\n" )

        f.close()

    def append( self, teacher, key, data, name ):
        lib.dic_append( self.name_list, key, {} )
        lib.dic_append( teacher, key, [] )
        self.name_list[key][str(len(teacher))] = name
        teacher[key].append( data )
"""

