hacker-news-archive
===================

Hacker News Archive System

== Requirements ==

 sudo aptitude install libxml2-dev libxslt-dev python-libxml2
 sudo easy_install lxml
 sudo easy_install PyQuery
 git submodule init
 git submodule update


== Setup ==

 git clone git@github.com:jaytaylor/hacker-news-archive.git

Add the schedule as a cron job:
$ crontab -e
 0 * * * * /var/www/scala.sh/public_html/hackernews-archive/snapshot.sh
