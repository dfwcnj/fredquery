#¡ sh
set -ex

fredcategories --categories --file /tmp/categories.csv 
fredcategories --series --categoryid 33500 --file /tmp/cseries33500.csv 
fredcategories --observations --directory /tmp --categoryid 33500
#fredcategories --observations --directory /tmp --seriesid


fredreleases --releases --file /tmp/releases.csv
fredreleases --series --releaseid 471 --file /tmp/rseries471.csv
fredreleases --observations --directory /tmp --releaseid 471
#fredreleases --observations --directory /tmp --seriesid 


fredtags --tags --file /tmp/tags.csv
fredtags --series --tagname employment --file /tmp/tseriesemployment.csv
fredtags --observations --directory /tmp --tagname employment
#fredtags --observations --directory /tmp --seriesid 

fredsources --sources --file /tmp/sources.csv
fredsources --releases --file /tmp/sreleases.csv
#fredsources --sources --releasid 471

