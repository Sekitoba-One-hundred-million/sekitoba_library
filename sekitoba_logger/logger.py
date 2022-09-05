import datetime

class Logger:
    def __init__( self, log_dir ):
        self.log_dir = log_dir
        #self.file_name = ""

    def create_timestamp( self ):
        now = datetime.datetime.now()
        return now.strftime( '%Y-%m-%d %H:%M:%S' )

    def file_name( self ):
        now = datetime.datetime.now()
        return now.strftime( '%Y-%m-%d' )

    def write( self, message ):
        write_file_name = ""
        write_file_name = self.log_dir + self.file_name()            
        f = open( self.log_dir + self.file_name(), "a" )
        f.write( message )
        f.close()

    def info( self, message ):
        write_str = self.create_timestamp() + " INFO " + message + "\n"
        self.write( write_str )

    def warning( self, message ):
        write_str = self.create_timestamp() + " WARN " + message + "\n"
        self.write( write_str )

    def error( self, message ):
        write_str = self.create_timestamp() + " ERROR " + message + "\n"
        self.write( write_str )

    def fatal( self, message ):
        write_str = self.create_timestamp() + " FATAL " + message + "\n"
        self.write( write_str )
