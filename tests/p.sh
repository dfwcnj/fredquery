#¡ sh
set -ex

D='src/fredquery'
cd $D

python fredcategories.py --categories --file /tmp/categories.csv 
python fredcategories.py --categories --showcategories
python fredcategories.py --series --categoryid 32455 \
        --file /tmp/cseries32455.csv 
python fredcategories.py --series --seriesid 00XALCATM086NEST --file \
       /tmp/00XALCATM086NEST_series.csv 
python fredcategories.py --observations --directory /tmp --categoryid 32455
#    python fredcategories.py --observations --directory /tmp --seriesid
set +x
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv > /dev/null
set -x


python fredreleases.py --releases --file /tmp/releases.csv
python fredreleases.py --releases --showreleases
python fredreleases.py --series --releaseid 365 --file /tmp/rseries365.csv
python fredreleases.py --series --seriesid ALLQ13A12MINR --file \
     /tmp/ALLQ13A12MINR_series.csv
python fredreleases.py --observations --directory /tmp --releaseid 9
#    fredreleases.py --observations --directory /tmp --seriesid 
set +x
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv >/dev/null
set -x

python fredseries.py --series     --seriesid AKIRPD \
        --file /tmp/AKIRPD_series.csv
python fredseries.py --observations     --seriesid AKIRPD \
        --file /tmp/AKIRPD_observations.csv
python fredseries.py --categories --seriesid AKIRPD \
        --file /tmp/AKIRPD_categories.csv
python fredseries.py --releases   --seriesid AKIRPD \
        --file /tmp/AKIRPD_releases.csv
python fredseries.py --sources    --seriesid AKIRPD \
        --file /tmp/AKIRPD_sources.csv
python fredseries.py --tags       --seriesid AKIRPD \
        --file /tmp/AKIRPD_tags.csv
python fredseries.py --updates    --seriesid AKIRPD \
        --file /tmp/AKIRPD_updates.csv
set +x
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv >/dev/null
set -x

python fredsources.py --sources  --file /tmp/sources.csv
python fredsources.py --sources  --showsources
python fredsources.py --releases --sourceid 69 --file /tmp/sreleases69.csv
#    python fredsources.py --releases --file /tmp/sreleases.csv
#    python fredsources.py --sources --directory /tmp
python fredsources.py --series --sourceid 69 --directory /tmp
python fredsources.py --observations --sourceid 69 --directory /tmp
set +x
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv >/dev/null
set -x


python fredtags.py --tags   --file /tmp/tags.csv
python fredtags.py --tags   --showtags
python fredtags.py --series --tagname price --file /tmp/tseriesprice.csv
python fredtags.py --series --seriesid ALLQ14ICNR \
        --file /tmp/ALLQ14ICNR_series.csv
python fredtags.py --observations --tagname price --directory /tmp
#    $D/fredtags --observations --directory /tmp --seriesid 
set +x
ls /private/tmp/[0-9A-Z]*.csv | wc -l
rm /private/tmp/[0-9A-Z]*.csv >/dev/null
set -x

