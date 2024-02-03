
-[Usage]
`
usage: fredcategories.py [-h] [--series] [--file FILE]
collect and report stlouisfed.org FRED categories and/or series
options:
  -h, --help   show this help message and exit
  --series     report series urls for categories
  --file FILE  store the output in this file


usage: fredreleases.py [-h] [--releases] [--releasesandseries] [--series]
                       [--releaseid RELEASEID] [--seriesid SERIESID]
                       [--file FILE]
collect and report stlouisfed.org FRED releases and/or their time series
options:
  -h, --help            show this help message and exit
  --releases            return releases
  --releasesandseries   return all series for all releases - not recommended
  --series              return series by series_id or by release_id
  --releaseid RELEASEID
                        a release_id identifies a FRED release
  --seriesid SERIESID   a series_id identifies a FRED series
  --file FILE           save the output to the file specified


usage: fredtags.py [-h] [--tags] [--tagsandseries] [--series]
                   [--tagname TAGNAME] [--seriesid SERIESID] [--file FILE]
collect and report stlouisfed.org FRED tags and/or their series
options:
  -h, --help           show this help message and exit
  --tags               return tags
  --tagsandseries      return all series for all tags - not recommended
  --series             return series for a tag_id or for a series_id
  --tagname TAGNAME    tag_id identifies a FRED tag
  --seriesid SERIESID  series_id - identifies a series
  --file FILE          save the output to the file specified


