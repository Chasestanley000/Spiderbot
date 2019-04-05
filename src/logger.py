import logging


class Logger:
    """
    A basic class to extend the default Python logger to add
    easier functionality and top level methods
    """
    def __init__( self, log_name ):
        self.logger = logging.getLogger( log_name )
        self.logger.setLevel( logging.DEBUG )
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    def set_file_handler( self, filename, level ):
        handler = logging.FileHandler( filename, 'w' )
        handler.setFormatter( self.formatter )
        handler.setLevel( logging.getLevelName( level ) )
        self.logger.addHandler( handler )

    def set_stream_handler( self, stream, level ):
        handler = logging.StreamHandler( stream )
        handler.setFormatter( self.formatter )
        handler.setLevel( logging.getLevelName( level ))
        self.logger.addHandler( handler )

    def remove_handlers( self ):
        handlers = self.logger.handlers
        for handler in handlers[:]:
            self.logger.removeHandler( handler )

    def debug(self, *args):
        message = ''
        for arg in args:
            message += "%s " % arg

        self.logger.debug(message)

    def info( self, *args ):
        message = ''
        for arg in args:
            message += "%s " % arg

        self.logger.info( message )

    def warning(self, *args):
        message = ''
        for arg in args:
            message += "%s " % arg

        self.logger.warning(message)

    def error(self, *args):
        message = ''
        for arg in args:
            message += "%s " % arg

        self.logger.error(message)

    def critical(self, *args):
        message = ''
        for arg in args:
            message += "%s " % arg

        self.logger.critical(message)
