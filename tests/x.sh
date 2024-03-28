#¡ sh
set -ex

fredcategories --categories --file /tmp/categories.csv 
fredcategories --categories --showcategories
fredcategories --series --categoryid 32455 --file /tmp/cseries32455.csv 
fredcategories --series --categoryid 32455 --showseries
fredcategories --observations --directory /tmp --categoryid 32455
#    fredcategories --observations --directory /tmp --seriesid
set +x
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv > /dev/null
set -x


fredreleases --releases --file /tmp/releases.csv
fredreleases --releases --showreleases
fredreleases --series --releaseid 365 --file /tmp/rseries365.csv
fredreleases --series --releaseid 365 --showseries
fredreleases --observations --directory /tmp --releaseid 9
set +x
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv >/dev/null
set -x

fredseries --series     --seriesid AKIRPD --file /tmp/AKIRPD_series.csv
fredseries --observations --seriesid AKIRPD --directory /tmp
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
fredsources --sources  --showsources
fredsources --releases --sourceid 69 --file /tmp/sreleases69.csv
fredsources --releases --sourceid 69 --showreleases
fredsources --series --sourceid 69 --file /tmp/Source69Series.csv
fredsources --series --sourceid 69 --showseries
fredsources --observations --sourceid 69 --directory /tmp
set +x
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv >/dev/null
set -x


fredtags --tags   --file /tmp/tags.csv
fredtags --tags   --showtags
fredtags --series --tagname price --file /tmp/tseriesprice.csv
fredtags --series --tagname price --showseries
fredtags --observations --tagname price --directory /tmp
set +x
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv >/dev/null
set -x

