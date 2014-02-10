""" State class for defining clusterd wide variables.  These are mainly set
by parsing command line arguments, but can be modified individually if necessary.
"""

# supported platforms by clusterd
supported_platforms = ['jboss', 'coldfusion', 'weblogic', 'tomcat']

# proxy to use for outgoing connections
proxy = None

# if necessary, authentication credentials for the aforementioned
# proxy.  This should be in the format username:password
proxy_auth = None

# credentials to authenticate to the service with.  This should be in
# the form username:password
usr_auth = None

# whether or not we are dumping debug strings
isdebug = False

# connection timeout to remote hosts
timeout = 5.0

# wordlist for brute forcing credentials
bf_wordlist = None

# with a loaded wordlist, use the following user to brute force
bf_user = None

# we don't want to brute force services more than once; resets after
# each service
hasbf = False

# if we're using a random User-Agent for requests, set that here
random_agent = None

# sets our HTTP type; default is http, but --ssl sets https
ssl = False

# filename for logging to file
flog = None

# for deployers that need to serve files to remote hosts,
# we copy payloads into this location and clean it at
# the end 
serve_dir = "/tmp/.clusterd"
