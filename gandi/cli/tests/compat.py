
try:
    from unittest import mock
except ImportError:
    import mock


try:
    import unittest2 as unittest
except ImportError:
    import unittest


try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


try:
    from cStringIO import StringIO as ReasonableBytesIO
except ImportError:
    from io import BytesIO as ReasonableBytesIO
