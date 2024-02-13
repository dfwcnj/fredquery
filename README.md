
# FREDquery
#

<p>
FredQuery uses the stlouisfed.org FRED
API(https://fred.stlouisfed.org/docs/api/fred/) for the most part to
access FRED data. To access the data you have to use an api_key that can
be acquired here(https://fred.stlouisfed.org/docs/api/api_key.html).
These scripts assume that the api_key is available through the FRED_API_KEY
environmental variable. Each script including fredsources
script will collect basic data for its type. For example
fredcategories.py will collect data for all its categories. They can
also collect series and obsrevations(timeseries) for its type.
</p〉


## [Usage]

### fredcategories
usage: fredcategories [-h] [--categories] [--series] [--observations] 
                    [--categoryid CATEGORYID] [--seriesid SERIESID] 
                    [--file FILE] [--directory DIRECTORY] 
 
collect and report stlouisfed.org FRED categories and/or series 
 
options: 
  -h, --help            show this help message and exit 
  --categories          report category data 
  --series              report series urls for categories collected 
  --observations        report timeseries data for categories 
  --categoryid CATEGORYID 
                        categories are identified by category_id 
  --seriesid SERIESID   series are identified by series_id 
  --file FILE           path to an output filename if just a filename and-- 
                        directory is not provided the file is created in the 
                        current directory 
  --directory DIRECTORY 
                        directory to write the output use --directory for 
                        storing observations, filenames autogenerated 
 
### fredreleases 
usage: fredreleases [-h] [--releases] [--series] [--observations] 
                    [--releaseid RELEASEID] [--seriesid SERIESID] 
                    [--file FILE] [--directory DIRECTORY] 
 
collect and report stlouisfed.org FRED releases and/or their time series 
 
options: 
  -h, --help            show this help message and exit 
  --releases            return releases 
  --series              return series by series_id or by release_id 
  --observations        return timeseries for all series collected 
  --releaseid RELEASEID 
                        a release_id identifies a FRED release 
  --seriesid SERIESID   a series_id identifies a FRED series 
  --file FILE           path to an output filename if just a filename and-- 
                        directory is not provided the file is created in the 
                        current directory 
  --directory DIRECTORY 
                        directory to write the output, if --observations 
                        filenames are autogenerated 
 
 
### fredsources 
usage: fredsources [-h] [--sources] [--releases] [--observations] 
                   [--sourceid SOURCEID] [--file FILE] [--directory DIRECTORY] 
 
collect and report stlouisfed.org FRED sources and/or their releases 
 
options: 
  -h, --help            show this help message and exit 
  --sources             return sources 
  --releases            return releases for a source_id 
  --observations        return observations for a source_id 
  --sourceid SOURCEID   a source_id identifies a FRED source 
  --file FILE           path to an output filename if just a filename and-- 
                        directory is not provided the file is created in the 
                        current directory 
  --directory DIRECTORY 
                        directory to write the output, if --observations 
                        filenames are autogenerated 
 
 
### fredtags 
usage: fredtags [-h] [--tags] [--series] [--observations] [--tagname TAGNAME] 
                [--seriesid SERIESID] [--file FILE] [--directory DIRECTORY] 
 
collect and report stlouisfed.org FRED tags and/or their series 
 
options: 
  -h, --help            show this help message and exit 
  --tags                return tags 
  --series              return series for a tag_id or for a series_id 
  --observations        report timeseries data for tags 
  --tagname TAGNAME     tag_id identifies a FRED tag 
  --seriesid SERIESID   series_id - identifies a series 
  --file FILE           path to an output filename if just a filename and-- 
                        directory is not provided the file is created in the 
                        current directory 
  --directory DIRECTORY 
                        save the output to the directory specified 
