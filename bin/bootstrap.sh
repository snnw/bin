#!/bin/bash

set -e
set -x

HOME=`pwd`

BIN='bin'
TMP='tmp'
MM='multimedia'
EXP='experiments'
PR='projects'
SRC='src'
LISTS='lists'

LISTS_SRC="$SRC/$LISTS"
BIN_SRC="$SRC/$BIN"

OLDHOME="$TMP/home"
DROPBOX='Dropbox'

CHECKOUT_EXTERNAL=1

if [ ! -d .ssh ]; then
  echo "ERROR: no ./.ssh directory"
  exit 1
fi

if [ ! -f .ssh/id_rsa ]; then
  echo "ERROR: no private key found"
  exit 1
fi

mkdir -p $HOME/tmp/home

shopt -s dotglob
GLOBIGNORE=tmp
mv * $HOME/tmp/home/
unset GLOBIGNORE
shopt -u dotglob

mv $HOME/tmp/home/.ssh $HOME

# TODO(snnw) separate README generation
cat > $HOME/README << EOF
WARNING: This file is auto-generated. Please update bootstrap.sh.

./$BIN/            -> $BIN_SRC
./$TMP/            automatic removal
./$EXP/    code without need of permanent saving / backups
./$MM/             multimedia / games: backups, yes. version control, no.
./$LISTS/          -> $LISTS_SRC
./$SRC/            code with external version control. backup, yes.
    $LISTS/        checklists / ideas lists / any list
    $BIN/          scripts in PATH
./$PR/       
    cse/
    q/
    
./$DROPBOX/        managed by Dropbox
EOF

ln -s $BIN_SRC   $HOME/$BIN
ln -s $LISTS_SRC $HOME/$LISTS

mkdir -p $HOME/{$EXP,$MM,$SRC,$PR}

git clone git@bitbucket.org:snnw/snnw_lists.git $HOME/$LISTS_SRC
git clone git@bitbucket.org:snnw/snnw_bin.git   $HOME/$BIN_SRC
git clone git@bitbucket.org:snnw/snnw_projects.git $HOME/$PR


# Repository for System validation
# hg clone ssh://hg@bitbucket.org/saberwolf/2iw26-system-validation $HOME/$SRC/mcrl2

if [ $CHECKOUT_EXTERNAL ]; then
  wget http://c758482.r82.cf2.rackcdn.com/sublime_text_3_build_3047_x64.tar.bz2 -O - | tar xjC $HOME/$SRC
fi

echo
echo "Default download directory:  $HOME/$TMP" 
echo "Dropbox folder:              $HOME/$DROPBOX"
echo
echo "Your old home can be found at: $HOME/$OLDHOME"
echo
