#!/bin/bash
#this is a comment-the first line sets bash as the shell script
cd "$(dirname "$BASH_SOURCE")" || {
    echo "Error getting script directory" >&2
    exit 1
}
pwd
#sudo chown -R $(whoami) /usr/local/var/homebrew
#brew install phantomjs
#pip3 install selenium
pip3 install pandas
python3 picture_downloads_fixed.py 
exit;