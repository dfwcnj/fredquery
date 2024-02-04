
# FREDquery
#

<p>
FredQuery uses the stlouisfed.org FRED
API(https://fred.stlouisfed.org/docs/api/fred/) for the most part to
access FRED data. To access the data you have to use an api_key that can
be acquired here(https://fred.stlouisfed.org/docs/api/api_key.html).
These scripts assume that the api_key is available through the FREDKEY
environmental variable. 
</p〉


## [Usage]

### FREDcategories
<P>
usage: fredcategories.py [-h] [--series] [--file FILE]<br>
collect and report stlouisfed.org FRED categories and/or series<br>
options:<br>
&nbsp&nbsp  -h, --help   show this help message and exit<br>
&nbsp&nbsp  --series     report series urls for categories<br>
&nbsp&nbsp  --file FILE  store the output in this file<br>
</p>


### FREDreleases
<P>
usage: fredreleases.py [-h] [--releases] [--releasesandseries] [--series]<br>
                       [--releaseid RELEASEID] [--seriesid SERIESID]<br>
                       [--file FILE]<br>
collect and report stlouisfed.org FRED releases and/or their time series<br>
options:<br>
&nbsp&nbsp  -h, --help            show this help message and exit<br>
&nbsp&nbsp  --releases            return releases<br>
&nbsp&nbsp  --releasesandseries   return all series for all releases - not recommended<br>
&nbsp&nbsp  --series              return series by series_id or by release_id<br>
&nbsp&nbsp  --releaseid RELEASEID<br>
&nbsp&nbsp                        a release_id identifies a FRED release<br>
&nbsp&nbsp  --seriesid SERIESID   a series_id identifies a FRED series<br>
&nbsp&nbsp  --file FILE           save the output to the file specified<br>
</p>


### FREDtags
<P>
usage: fredtags.py [-h] [--tags] [--tagsandseries] [--series]<br>
                   [--tagname TAGNAME] [--seriesid SERIESID] [--file FILE]<br>
collect and report stlouisfed.org FRED tags and/or their series<br>
options:<br>
&nbsp&nbsp  -h, --help           show this help message and exit<br>
&nbsp&nbsp  --tags               return tags<br>
&nbsp&nbsp  --tagsandseries      return all series for all tags - not
&nbsp&nbsp  recommended<br>
&nbsp&nbsp  --series             return series for a tag_id or for a series_id<br>
&nbsp&nbsp  --tagname TAGNAME    tag_id identifies a FRED tag<br>
&nbsp&nbsp  --seriesid SERIESID  series_id - identifies a series<br>
&nbsp&nbsp  --file FILE          save the output to the file specified<br>
</p>


