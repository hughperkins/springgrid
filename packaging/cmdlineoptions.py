from optparse import OptionParser

parser = OptionParser()
# parser.add_option( "--testing-local", help = 'activate configuration for testing locally', dest = 'testinglocal', action='store_true' )
parser.add_option( "--urllisturl", help = 'url of usrllist.py', dest = 'urllisturl' )

(options, args ) = parser.parse_args()

