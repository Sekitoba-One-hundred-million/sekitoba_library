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

    def message_list_create( self, message, kind ):
        message_list = []
        split_message = message.split( "\n" )

        for m in split_message:
            if len( m ) == 0:
                continue

            message_list.append( self.create_timestamp() + " " + kind + " " + m + "\n" )

        return message_list

    def write( self, message_list ):
        write_file_name = self.log_dir + self.file_name()
        f = open( self.log_dir + self.file_name(), "a" )

        for message in message_list:
            f.write( message )
            
        f.close()

    def info( self, message ):
        self.write( self.message_list_create( message, "INFO" ) )

    def warning( self, message ):
        self.write( self.message_list_create( message, "WARN" ) )

    def error( self, message ):
        self.write( self.message_list_create( message, "ERROR" ) )

    def fatal( self, message ):
        self.write( self.message_list_create( message, "FATAL" ) )
