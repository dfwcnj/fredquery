#¡ sh
set -ex

python $TDIR/fredquery/categories/fredcategories.py --categories --file /tmp/categories.csv 
python $TDIR/fredquery/categories/fredcategories.py --series --categoryid 33500 --file /tmp/cseries33500.csv 
python $TDIR/fredquery/categories/fredcategories.py --observations --directory /tmp --categoryid 33500
#python $TDIR/fredquery/categories/fredcategories.py --observations --directory /tmp --seriesid


python $TDIR/fredquery/releases/fredreleases.py --releases --file /tmp/releases.csv
python $TDIR/fredquery/releases/fredreleases.py --series --releaseid 471 --file /tmp/rseries471.csv
python $TDIR/fredquery/releases/fredreleases.py --observations --directory /tmp --releaseid 471
#python $TDIR/fredquery/releases/fredreleases.py --observations --directory /tmp --seriesid 


python $TDIR/fredquery/tags/fredtags.py --tags --file /tmp/tags.csv
python $TDIR/fredquery/tags/fredtags.py --series --tagname employment --file /tmp/tseriesemployment.csv
python $TDIR/fredquery/tags/fredtags.py --observations --directory /tmp --tagname employment
#python $TDIR/fredquery/tags/fredtags.py --observations --directory /tmp --seriesid 

python $TDIR/fredquery/sources/fredsources.py --sources --file /tmp/sources.csv
