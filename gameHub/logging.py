"""Logging for gameHub backend."""

import logging
from logging import Formatter

from django.utils import timezone

def reverseEscape(string):
  """Replaces newline and tab with their escape sequences, and isolates '\\' in an escape sequence.
  """
  return string.replace('\\', '<%\\%>').replace('\n', '\\n').replace('\t', '\\t').replace('<%', '<%<%><%%%>').replace('%>', '<%%%><%>%>')

class SingleLineFormatter(Formatter):
  """Standard compliant formatter for formatting a single line in the log files.
  
    Formats any log message onto a single line, along with timestamp, logging level
    and name of the logger, separated by tab.
  """
  
  def __init__(self, fmt=None, datefmt=None, style='%'):
    self.datefmt = datefmt
    super(SingleLineFormatter, self).__init__(fmt, datefmt, style)
  
  def format(self, record):
    msg = super(SingleLineFormatter, self).format(record)
    time = super(SingleLineFormatter, self).formatTime(record, self.datefmt)
    return '{0}\t{1}\t{2}\t{3}'.format(
      time,
      record.levelno,
      record.name,
      reverseEscape(msg)
    )
  
  def formatException(self, exc_info):
    msg = super(SingleLineFormatter, self).formatException(exc_info)
    return msg
  
  def formatStack(self, stack_info):
    msg = super(SingleLineFormatter, self).formatStack(stack_info)
    return msg
