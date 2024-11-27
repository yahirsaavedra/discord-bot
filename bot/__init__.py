"""
CENSURADO
~~~~~~~~~~~~~~~~~~~

CENSURADO, a multifunctional Discord bot.

:copyright: CENSURADO - REALIZADO EN 2017
:license: Apache License 2.0, see LICENSE for more details.

"""
from collections import namedtuple

from bot.CENSURADO import CENSURADO
from bot.session_manager import HTTPStatusError, SessionManager

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(
    major=0, minor=2, micro=0, releaselevel='alpha', serial=1
)

__title__ = 'CENSURADO'
__author__ = ['CENSURADO', 'CENSURADO', 'CENSURADO']
__author_plain__ = ['CENSURADO', 'CENSURADO', 'CENSURADO']
__helper__ = ['CENSURADO']
__helper_plain__ = ['CENSURADO']
__license__ = 'Apache License 2.0'
__copyright__ = 'CENSURADO'
__version__ = '.'.join([str(i) for i in list(version_info)[:3]])

__all__ = ['__title__', '__author__', '__author_plain__',
           '__helper__', '__helper_plain__', '__license__', '__copyright__',
           '__version__', 'version_info', 'CENSURADO', 'SessionManager',
           'HTTPStatusError']
