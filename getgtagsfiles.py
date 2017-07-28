#!/bin/env python

import fnmatch
import os
import pprint
import re
import subprocess
import sys


extnames = None
excludedpatterns = None
pp = pprint.PrettyPrinter(indent=4)
# debugpath = 'src/abc'


def usage():
  print('Usage:')
  print('  python ' + sys.argv[0] + ' rulesfile')


def get_entry_path(path, entry):
  if path == '.':
    return entry

  if not path.endswith('/'):
    path = path + '/'

  return path + entry


def exclude(name, logout):
  global excludedpatterns
  
  if name.startswith('.'):
    return True

  if excludedpatterns is None:
    return False

  for pattern in excludedpatterns:
    if fnmatch.fnmatchcase(name, pattern):
      if logout:
        print '= ' + name + ' matched ' + pattern
      return True
    if logout:
      print name + ' not matched'

  return False


def process(filepaths, rules, path, included=False):
  global debugpath

  logout = False
  if 'debugpath' in globals() and (debugpath is None or path.startswith(debugpath)):
    logout = True
    print '---------------'
    print path

  if not included:
    pos = path.rfind('/')
    if pos < 0:
      print 'error: nonexpected path: ' + path
      return

    if exclude(path[pos+1:], logout):
      return
    
  if os.path.isfile(path):
    pos = path.rfind('.')
    if pos <= 0:
      return

    ext = path[pos+1:]
    if ext in extnames:
      filepaths.append(path)
    return

  if not os.path.isdir(path):
    print 'not a dir: ' + path
    return
  
  if rules is None:
    for entry in os.listdir(path):
      process(filepaths, None, get_entry_path(path, entry))
    return

  if '-' in rules:
    entries = os.listdir(path)
      
    excludedentries = set();
    for name in rules['-']:
      names = fnmatch.filter(entries, name)
      if len(names) > 0:
        excludedentries |= set(names)

    entries = set(entries) - excludedentries
    for entry in entries:
      if entry not in rules.keys():
        process(filepaths, None, get_entry_path(path, entry))

  if '+' in rules:
    for entry in rules['+']:
      if entry not in rules.keys():
        process(filepaths, None, get_entry_path(path, entry), True)

  for entry in rules.keys():
    if entry != '+' and entry != '-':
      process(filepaths, rules[entry], get_entry_path(path, entry), True)


def main():
  global extnames
  global excludedpatterns

  if (len(sys.argv) != 3):
    usage()
    return

  rulesfile = sys.argv[1]
  if not os.path.isfile(rulesfile):
    print 'rulesfile is not a file.'
    usage()
    return

  destdir = sys.argv[2]
    
  with open(rulesfile) as f:
    conf = eval(f.read())

  rules = conf['rules']
  extnames = conf['extnames']

  if 'excludedpatterns' in conf:
    excludedpatterns = conf['excludedpatterns']

  fo = open('gtags.files', 'w')

  filepaths = []
  process(filepaths, rules, destdir, True)

  for line in sorted(filepaths):
    fo.write(line + '\n')
  fo.close()


##############################
if __name__ == '__main__':
  main()
