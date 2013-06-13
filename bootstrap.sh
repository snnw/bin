#!/bin/bash

HOME=`pwd`

BIN='bin'
TMP='tmp'
MM='multimedia'
EXP='experiments'
REF='reference'
PR='projects'
SRC='src'
LISTS='lists'

LISTS_SRC="$SRC/$LISTS"
BIN_SRC="$SRC/$BIN"

OLDHOME="$TMP/home"
DOWNLOADS="$TMP/Downloads"
DROPBOX='Dropbox'

CHECKOUT_EXTERNAL=1


mkdir -p $HOME/tmp/home

mv * .* $HOME/tmp/home/ 2>/dev/null

# TODO(snnw) separate README generation
cat > $HOME/README << EOF
WARNING: This file is auto-generated. Please update bootstrap.sh.

./$BIN/            -> $BIN_SRC
./$TMP/            automatic removal
./$DOWNLOADS/  destination of temporary internet downloads
./$EXP/    code without need of permanent saving / backups
./$MM/             multimedia / games: backups, yes. version control, no.
./$LISTS/          -> $LISTS_SRC
./$SRC/            code with external version control. backup, yes.
    $LISTS/        checklists / ideas lists / any list
    $BIN/          scripts in PATH
./$PR/       
    cse/
    q/
    
./$REF/

./$DROPBOX/        managed by Dropbox
EOF

ln -s $BIN_SRC   $HOME/$BIN
ln -s $LISTS_SRC $HOME/$LISTS

mkdir -p $HOME/{$DOWNLOADS,$EXP,$MM,$SRC,$PR,$REF}

git clone git@bitbucket.org:snnw/snnw_lists.git $HOME/$LISTS_SRC
git clone git@bitbucket.org:snnw/snnw_bin.git   $HOME/$BIN_SRC
git clone git@bitbucket.org:snnw/snnw_projects.git $HOME/$PR


# Repository for System validation
# hg clone ssh://hg@bitbucket.org/saberwolf/2iw26-system-validation $HOME/$SRC/mcrl2

if [ $CHECKOUT_EXTERNAL ]; then
  hg clone -u release https://code.google.com/p/go $HOME/$SRC/go
  git clone git://github.com/martine/ninja.git $HOME/$SRC/ninja
fi

echo
echo "Default download directory:  $HOME/$DOWNLOADS" 
echo "Dropbox folder:              $HOME/$DROPBOX"
echo
echo "Your old home can be found at: $HOME/$OLDHOME"
echo
