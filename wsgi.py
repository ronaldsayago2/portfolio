import sys
# path = '/home/ronaldsayago2/portfolio_web'
path = '/mnt/hgfs/development/python/portfolio_web'

if path not in sys.path:
    sys.path.append(path)

from app import app as application