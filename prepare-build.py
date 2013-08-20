#!/usr/bin/python

NDEBUG=False

import md5
import os
import os.path
import shutil

src_base = '/home/snnw/src/chromium/src/'
dest_base = '/home/snnw/tmp/chromium'

excludes = ['.git', '.svn', 'out']

def relative_to_src_base(path):
  assert(path.startswith(src_base))

  return path[len(src_base):]

def copy_file(src, dest):
  shutil.copy(src, dest)
  print relative_to_src_base(src)

def chksum(f, block_size=2**20):
  fd = open(f, 'rb')
  md5 = haslib.md5()
  while True:
    data = f.read(block_size)
    if not data:
      break
    md5.update(data)
  return md5.digest()

def pre_process_dir(root, d):
  if d in excludes:
    del d
    return

  src = os.path.join(root, d)
  src_rel = relative_to_src_base(src)
  dest = os.path.join(dest_base, src_rel)

  if not os.path.exists(dest):
    return

  if not os.path.isdir(dest):
    # dest should be a directory
    os.remove(dest)
    return

  src_mtime = os.path.getmtime(src)
  dest_mtime = os.path.getmtime(dest)

  if src_mtime <= dest_mtime:
    # dest was copied more recently than src was modified
    del d
    return

def process_dir(src):
  src_rel = relative_to_src_base(src)
  dest = os.path.join(dest_base, src_rel)
  src_mode = os.stat(src).st_mode

  if not os.path.exists(dest):
    os.mkdir(dest, src_mode)
  else:
    os.utime(dest)

def process_file(root, f):
  if f in excludes:
    return

  src = os.path.join(root, f)
  src_rel = relative_to_src_base(src)
  dest = os.path.join(dest_base, src_rel)

  if not os.path.exists(dest):
    copy_file(src, dest)
    return

  if os.path.isdir(dest):
    shutil.rmtree(dest)
    copy_file(src, dest)
    return

  src_mtime = os.path.getmtime(src)
  dest_mtime = os.path.getmtime(dest)

  if src_mtime <= dest_mtime:
    return

  src_size = os.path.getsize(src)
  dest_size = os.path.getsize(dest)

  if src_size == dest_size:
    return

  if chksum(src) == chksum(dest):
    return

  copy_file(src, dest)

if __name__ == '__main__':
  os.makedirs(dest_base)

  for root, dirs, files in os.walk(src_base):
    process_dir(root)

    for d in dirs:
      pre_process_dir(d)
    
    for f in files:
      process_file(root, f)
