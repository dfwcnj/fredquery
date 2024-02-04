
# FREDquery
#
-[Usage]
`
<P>
usage: fredcategories.py [-h] [--series] [--file FILE]<br>
collect and report stlouisfed.org FRED categories and/or series<br>
options:<br>
  -h, --help   show this help message and exit<br>
  --series     report series urls for categories<br>
  --file FILE  store the output in this file<br>
</p>


<P>
usage: fredreleases.py [-h] [--releases] [--releasesandseries] [--series]<br>
                       [--releaseid RELEASEID] [--seriesid SERIESID]<br>
                       [--file FILE]<br>
collect and report stlouisfed.org FRED releases and/or their time series<br>
options:<br>
  -h, --help            show this help message and exit<br>
  --releases            return releases<br>
  --releasesandseries   return all series for all releases - not recommended<br>
  --series              return series by series_id or by release_id<br>
  --releaseid RELEASEID<br>
                        a release_id identifies a FRED release<br>
  --seriesid SERIESID   a series_id identifies a FRED series<br>
  --file FILE           save the output to the file specified<br>
</p>


<P>
usage: fredtags.py [-h] [--tags] [--tagsandseries] [--series]<br>
                   [--tagname TAGNAME] [--seriesid SERIESID] [--file FILE]<br>
collect and report stlouisfed.org FRED tags and/or their series<br>
options:<br>
  -h, --help           show this help message and exit<br>
  --tags               return tags<br>
  --tagsandseries      return all series for all tags - not
  recommended<br>
  --series             return series for a tag_id or for a series_id<br>
  --tagname TAGNAME    tag_id identifies a FRED tag<br>
  --seriesid SERIESID  series_id - identifies a series<br>
  --file FILE          save the output to the file specified<br>
</p>


