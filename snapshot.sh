#!/usr/bin/env bash

##
# @author Jay Taylor [@jtaylor]
#
# Date: 2012-09-02
#
# Description: HackerNews Archiver
#


ts=$(date --utc)

unixTime=$(date --utc --date="$ts" +'%s')
prettyTs=$(date --utc --date="$ts" +'%Y-%m-%d %H:%M:%S')


basePath="$(dirname $0)/data"

if ! [ -d "$basePath" ] ; then
    mkdir -p "$basePath"
fi

cd "$basePath"


mkdir "$unixTime"
cd "$unixTime"

echo "$ts" > date.txt
echo "$unixTime" > unixtime.txt
echo "$prettyTs" > prettydate.txt

wget -erobots=off -N --no-remove-listing --page-requisites --user-agent='Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3' --convert-links --backup-converted 'http://news.ycombinator.com/'

cd ../..

python python-inlineify-html/inlineify.py -i data/$unixTime/news.ycombinator.com/index.html -d 'ycombinator.com' > data/$unixTime/index.html


