#¡ sh
set -ex

fredcategories --categories --file /tmp/categories.csv 
fredcategories --series --categoryid 32455 --file /tmp/cseries32455.csv 
fredcategories --series --seriesid 00XALCATM086NEST --file \
       /tmp/00XALCATM086NEST_series.csv 
fredcategories --observations --directory /tmp --categoryid 32455
#    fredcategories --observations --directory /tmp --seriesid
ls /private/tmp/[0-9]*.csv | wc -l
rm /private/tmp/[0-9]*.csv >/dev/null


fredreleases --releases --file /tmp/releases.csv
fredreleases --series --releaseid 9 --file /tmp/rseries9.csv
fredreleases --series --serieid ALLQ13A12MINR --file \
     /tmp/ALLQ13A12MINR_series.csv
fredreleases --observations --directory /tmp --releaseid 9
#    fredreleases --observations --directory /tmp --seriesid 
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv >/dev/null


fredsources --sources  --file /tmp/sources.csv
fredsources --releases --sourceid 69 --file /tmp/sreleases69.csv
#    fredsources --releases --file /tmp/sreleases.csv
#    fredsources --sources --directory /tmp
fredsources --observations --sourceid 69 --directory /tmp
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv >/dev/null

fredseries --series     --seriesid AKIRPD --file /tmp/AKIRPD_series.csv
fredseries --categories --seriesid AKIRPD --file /tmp/AKIRPD_categories.csv
fredseries --releases   --seriesid AKIRPD --file /tmp/AKIRPD_releases.csv
fredseries --sources    --seriesid AKIRPD --file /tmp/AKIRPD_sources.csv
fredseries --tags       --seriesid AKIRPD --file /tmp/AKIRPD_tags.csv
fredseries --updates    --seriesid AKIRPD --file /tmp/AKIRPD_updates.csv
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv >/dev/null

fredtags --tags   --file /tmp/tags.csv
fredtags --series --tagname price --file /tmp/tseriesprice.csv
fredtags --series --seriesid ALLQ14ICNR --file /tmp/ALLQ14ICNR_series.csv
fredtags --observations --tagname price --directory /tmp
#    fredtags --observations --directory /tmp --seriesid 
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv >/dev/null

