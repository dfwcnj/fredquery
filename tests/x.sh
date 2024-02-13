#¡ sh
set -ex

fredcategories --categories --file /tmp/categories.csv 
fredcategories --series --categoryid 32455 --file /tmp/cseries32455.csv 
fredcategories --observations --directory /tmp --categoryid 32455
#    fredcategories --observations --directory /tmp --seriesid
ls /private/tmp/[A-Z]*.csv | wc -l
rm /private/tmp/[A-Z]*.csv


fredreleases --releases --file /tmp/releases.csv
fredreleases --series --releaseid 9 --file /tmp/rseries9.csv
fredreleases --observations --directory /tmp --releaseid 9
#    fredreleases --observations --directory /tmp --seriesid 
ls /private/tmp/[A-Z]*.csv | wc -l
rm /private/tmp/[A-Z]*.csv


fredsources --sources --file /tmp/sources.csv
fredsources --releases --sourceid 69 --file /tmp/sreleases69.csv
#    fredsources --releases --file /tmp/sreleases.csv
#    fredsources --sources --directory /tmp
fredsources --observations --sourceid 69
#ls /private/tmp/[A-Z]*.csv | wc -l
#rm /private/tmp/[A-Z]*.csv

fredtags --tags --file /tmp/tags.csv
fredtags --series --tagname price --file /tmp/tseriesprice.csv
fredtags --observations --directory /tmp --tagname price
#    fredtags --observations --directory /tmp --seriesid 
ls /private/tmp/[A-Z]*.csv | wc -l
rm /private/tmp/[A-Z]*.csv

