
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
also collect series and observations(timeseries) for its type.
</p〉


## [Usage]

## fredcategories

usage: fredcategories [-h] [--categories] [--series] [--observations]<br/>
                      [--categoryid CATEGORYID] [--seriesid SERIESID]<br/>
                      [--file FILE] [--directory DIRECTORY]<br/>
<br/>
collect and report stlouisfed.org FRED categories and/or series<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --categories          report category data<br/>
  --series              report series urls for categories collected<br/>
  --observations        report timeseries data for categories<br/>
  --categoryid CATEGORYID<br/>
                        categories are identified by category_id<br/>
  --seriesid SERIESID   series are identified by series_id<br/>
  --file FILE           path to an output filename if just a filename and--<br/>
                        directory is not provided the file is created in the<br/>
                        current directory<br/>
  --directory DIRECTORY<br/>
                        directory to write the output use --directory for<br/>
                        storing observations, filenames autogenerated<br/>
## fredreleases

usage: fredreleases [-h] [--releases] [--series] [--observations]<br/>
                    [--releaseid RELEASEID] [--seriesid SERIESID]<br/>
                    [--file FILE] [--directory DIRECTORY]<br/>
<br/>
collect and report stlouisfed.org FRED releases and/or their time series<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --releases            return releases<br/>
  --series              return series by series_id or by release_id<br/>
  --observations        return timeseries for all series collected<br/>
  --releaseid RELEASEID<br/>
                        a release_id identifies a FRED release<br/>
  --seriesid SERIESID   a series_id identifies a FRED series<br/>
  --file FILE           path to an output filename if just a filename and--<br/>
                        directory is not provided the file is created in the<br/>
                        current directory<br/>
  --directory DIRECTORY<br/>
                        directory to write the output, if --observations<br/>
                        filenames are autogenerated<br/>
## fredseries

usage: fredseries [-h] [--series] [--observations] [--categories] [--releases]<br/>
                  [--sources] [--tags] [--updates] --seriesid SERIESID<br/>
                  [--file FILE] [--directory DIRECTORY]<br/>
<br/>
collect and report stlouisfed.org FRED series<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --series              report series urls for categories collected<br/>
  --observations        report timeseries data for categories<br/>
  --categories          report categories for this series<br/>
  --releases            report categories for this series<br/>
  --sources             report sources for this series<br/>
  --tags                report tags for this series<br/>
  --updates             report updates for this series<br/>
  --seriesid SERIESID   series are identified by series_id<br/>
  --file FILE           path to an output filename if just a filename and--<br/>
                        directory is not provided the file is created in the<br/>
                        current directory<br/>
  --directory DIRECTORY<br/>
                        directory to write the output use --directory for<br/>
                        storing observations, filenames autogenerated<br/>
## fredsources

usage: fredsources [-h] [--sources] [--releases] [--observations]<br/>
                   [--sourceid SOURCEID] [--file FILE] [--directory DIRECTORY]<br/>
<br/>
collect and report stlouisfed.org FRED sources and/or their releases<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --sources             return sources<br/>
  --releases            return releases for a source_id<br/>
  --observations        return observations for a source_id<br/>
  --sourceid SOURCEID   a source_id identifies a FRED source<br/>
  --file FILE           path to an output filename if just a filename and--<br/>
                        directory is not provided the file is created in the<br/>
                        current directory<br/>
  --directory DIRECTORY<br/>
                        directory to write the output, if --observations<br/>
                        filenames are autogenerated<br/>
## fredtags

usage: fredtags [-h] [--tags] [--series] [--observations] [--tagname TAGNAME]<br/>
                [--seriesid SERIESID] [--file FILE] [--directory DIRECTORY]<br/>
<br/>
collect and report stlouisfed.org FRED tags and/or their series<br/>
<br/>
options:<br/>
  -h, --help            show this help message and exit<br/>
  --tags                return tags<br/>
  --series              return series for a tag_id or for a series_id<br/>
  --observations        report timeseries data for tags<br/>
  --tagname TAGNAME     tag_id identifies a FRED tag<br/>
  --seriesid SERIESID   series_id - identifies a series<br/>
  --file FILE           path to an output filename if just a filename and--<br/>
                        directory is not provided the file is created in the<br/>
                        current directory<br/>
  --directory DIRECTORY<br/>
                        save the output to the directory specified<br/>
