#¡ sh
set -ex

fredcategories --categories --file /tmp/categories.csv 
fredcategories --series --categoryid 32455 --file /tmp/cseries32455.csv 
fredcategories --series --seriesid 00XALCATM086NEST --file \
       /tmp/00XALCATM086NEST_series.csv 
fredcategories --observations --directory /tmp --categoryid 32455
#    fredcategories --observations --directory /tmp --seriesid
set +x
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv > /dev/null
set -x


fredreleases --releases --file /tmp/releases.csv
fredreleases --series --releaseid 365 --file /tmp/rseries365.csv
fredreleases --series --seriesid ALLQ13A12MINR --file \
     /tmp/ALLQ13A12MINR_series.csv
fredreleases --observations --directory /tmp --releaseid 9
#    fredreleases --observations --directory /tmp --seriesid 
set +x
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv >/dev/null
set -x

fredseries --series     --seriesid AKIRPD --file /tmp/AKIRPD_series.csv
fredseries --observations --seriesid AKIRPD --file\
    /tmp/AKIRPD_observations.csv
fredseries --categories --seriesid AKIRPD --file /tmp/AKIRPD_categories.csv
fredseries --releases   --seriesid AKIRPD --file /tmp/AKIRPD_releases.csv
fredseries --sources    --seriesid AKIRPD --file /tmp/AKIRPD_sources.csv
fredseries --tags       --seriesid AKIRPD --file /tmp/AKIRPD_tags.csv
fredseries --updates    --seriesid AKIRPD --file /tmp/AKIRPD_updates.csv
set +x
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv >/dev/null
set -x

fredsources --sources  --file /tmp/sources.csv
fredsources --releases --sourceid 69 --file /tmp/sreleases69.csv
#    fredsources --releases --file /tmp/sreleases.csv
#    fredsources --sources --directory /tmp
fredsources --series --sourceid 69 --directory /tmp
fredsources --observations --sourceid 69 --directory /tmp
set +x
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv >/dev/null
set -x


fredtags --tags   --file /tmp/tags.csv
fredtags --series --tagname price --file /tmp/tseriesprice.csv
fredtags --series --seriesid ALLQ14ICNR --file /tmp/ALLQ14ICNR_series.csv
fredtags --observations --tagname price --directory /tmp
#    fredtags --observations --directory /tmp --seriesid 
set +x
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv >/dev/null
set -x

