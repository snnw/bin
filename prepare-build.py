#!/usr/bin/python

NDEBUG=False

import md5
import os
import os.path
import shutil
import sys

src_base = '/home/snnw/src/chromium/src/'
dest_base = '/home/snnw/tmp/chromium'

excludes = ['.git', '.svn', 'out']

def relative_to_src_base(path):
  assert(path.startswith(src_base))

  return path[len(src_base):]

def copy_file(src, dest):
  if os.path.islink(src):
    linkto = os.readlink(src)
    os.symlink(linkto, dest)
  else:
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
    return False

  src = os.path.join(root, d)
  src_rel = relative_to_src_base(src)
  dest = os.path.join(dest_base, src_rel)

  if not os.path.exists(dest):
    return True

  if not os.path.isdir(dest):
    # dest should be a directory
    os.remove(dest)
    return True

  return True

def process_dir(src):
  src_rel = relative_to_src_base(src)
  dest = os.path.join(dest_base, src_rel)
  src_mode = os.stat(src).st_mode

  if not os.path.exists(dest):
    os.mkdir(dest, src_mode)

def process_file(root, f):
  if f in excludes:
    return

  src = os.path.join(root, f)
  src_rel = relative_to_src_base(src)
  dest = os.path.join(dest_base, src_rel)

  if not os.path.exists(dest) and not os.path.islink(dest):
    copy_file(src, dest)
    return

  if os.path.islink(src):
    if not os.path.islink(dest):
      os.remove(dest)
      copy_file(src, dest)
      return

    if os.readlink(src) == os.readlink(dest):
      return

    os.remove(dest)
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
  if len(sys.argv) == 2:
    dest_base = sys.argv[1]
  if len(sys.argv) > 2:
    sys.exit()

  if not os.path.isdir(dest_base):
    os.makedirs(dest_base)

  for root, dirs, files in os.walk(src_base):
    process_dir(root)

    dirs[:] = [d for d in dirs if pre_process_dir(root, d)]
    
    for f in files:
      process_file(root, f)
