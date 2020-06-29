#!/bin/bash
wget --recursive --no-clobber --page-requisites --html-extension --convert-links --restrict-file-names=windows --no-parent \
     --domains website.org www.website.org/tutorials/html/This

# 用于下载 一个网页上的所有直接内容
#  
#   --recursive: download the entire Web site.
#   --no-clobber: don't overwrite any existing files (used in case the download is interrupted andresumed)
#   --page-requisites: get all the elements that compose the page (images, CSS and so on).
#   --html-extension: save files with the .html extension.
#   --convert-links: convert links so that they work locally, off-line.
#   --restrict-file-names=windows: modify filenames so that they will work in Windows as well.
#   --no-parent: don't follow links outside the directory tutorials/html/.
#   --domains website.org: don't follow links outside website.org.

