class LOG:
    """ This class specifies the different logging levels that we support.
    Levels can be trivially added here and in src/core/utility.py#Msg along
    with their pretty output information.
    """

    INFO = 1        # green
    SUCCESS = 2     # bold green
    ERROR = 3       # red
    DEBUG = 4       # blue
    UPDATE = 5      # yellow
