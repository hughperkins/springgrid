
from core import *
from utils import *

def test():
   tester.test()
   dates.test()
   stringhelper.test()

   dbconnection.connectdb()
   roles.test()
   dbconnection.disconnectdb()

if __name__ == '__main__':
   test()

