#! env python

# return information on categories, their releases, or their series
#
#

import os
import sys
import argparse
import html
from html.parser import HTMLParser
import re
import time
import urllib.request
import xml
from xml.etree import ElementTree as ET

try:
    from fredquery import query
    from fredquery import aa2html
    from fredquery import xmlstr2aa
except ImportError as e:
    import query
    import aa2html
    import xmlstr2aa

class FREDcategories():
    """ FREDcategories

    collect and report stlouisfed.org FRED categories, their series, and
    their observations(timeseries data)
    """
    def __init__(self):
        self.cid = None
        self.curl = 'https://fred.stlouisfed.org/categories'
        self.acurl = 'https://api.stlouisfed.org/fred/category'
        self.csurl = 'https://api.stlouisfed.org/fred/category/series'
        self.ssurl = 'https://api.stlouisfed.org/fred/series'
        self.sourl = 'https://api.stlouisfed.org/fred/series/observations'
        self.kurl = 'https://fred.stlouisfed.org/docs/api/api_key.html'
        self.rapi_key = 'FRED_API_KEY'
        if 'FRED_API_KEY' in os.environ:
            self.api_key = os.environ['FRED_API_KEY']
        else:
            print('FRED api_key required: %s' % (self.kurl), file=sys.stderr)
            print('assign this key to FRED_API_KEY env variable',
                                  file=sys.stderr)
            sys.exit()
        self.npages  = 7
        self.verbose = False
        self.pause   = 2 # number of seconds to pause
        self.retries = 5 # number of query retries
        self.categorydict= {}
        self.seriesdict = {}
        self.observationsdict = {}

        self.uq = query._URLQuery()
        self.ah = aa2html._AA2HTML()
        self.xa = xmlstr2aa._XMLStr2AA()

    def reportobservation(self, obsa, sid, units, odir):
        """ reportobservation(sid, obsa, sid, units, odir)

        report observations for a series_id
        obsa - list of observations for a series_id
        sid - series_id
        units - the units of the observation values
        odir - directory for storing observations
        """
        units = ''.join(units.split() )
        fn = os.path.join('%s/%s_%s.csv' % (odir, sid, units) )
        with open(fn, 'w') as fp:
            keys=[]
            for row in obsa:
                rw = "','".join(row)
                print("'%s'" % (rw), file=fp )

    def getandreportobservations(self, odir):
        """ getandreportobservations()

        incrementally get and store observation data for all
        series collected
        observation = time series data
        """
        for id in self.seriesdict:
            aa = self.seriesdict[id]
            assert aa[0][0] == 'id'
            for i in range(1, len(aa) ):
                id = aa[i][0]
                units = aa[i][8]
                url = '%s?series_id=%s&api_key=%s' % (self.sourl, id,
                       self.api_key)
                resp = self.uq.query(url)
                rstr = resp.read().decode('utf-8')
                obsa = self.xa.xmlstr2aa(rstr)
                self.reportobservation(obsa, id, units, odir)
                time.sleep(1)

    def showseries(self, id):
        """ showseries()

        show the series list for a category in your browser
        """
        self.ah.aashow(self.seriesdict[id], '%s series' % id)

    def reportseries(self, id, ofp):
        """ reportseries(ofp)

        report series data for categories
        rstr - decoded response of a urllib request
        """
        aa = self.seriesdict[id]
        for a in aa:
            row = "','".join(a)
            print("'%s'" % (row), file=ofp)

    def getseriesforsid(self, sid):
        """ getseriesforsid(sid)

        get a series for a series_id
        sid - series_id
        """
        if not sid:
            print('getseriesforsid: sid required', file=stderr)
            sys.exit(1)
        url = '%s?series_id=%s&api_key=%s' % (self.ssurl, sid,
                                              self.api_key)
        resp = self.uq.query(url)
        rstr = resp.read().decode('utf-8')
        aa = self.xa.xmlstr2aa(rstr)
        if len(aa) == 0:
            print('getseriesforsid(sid): no data' % (sid), file=sys.stderr)
        self.seriesdict[sid] = aa

    def getseriesforcid(self, cid):
        """ getseriesforcid(cid)

        collect series data for a category_id
        cid - category_id
        """
        if not cid:
            print('getseriesforcid: cid required', file=stderr)
            sys.exit(1)
        self.cid = cid
        url = '%s?category_id=%s&api_key=%s' % (self.csurl, cid, self.api_key)
        resp=self.uq.query(url)
        rstr = resp.read().decode('utf-8')
        aa = self.xa.xmlstr2aa(rstr)
        if len(aa) == 0:
            print('getseriesforcid(%s): no data' % (cid), file=sys.stderr)
            return
        aa[0].append('url')
        for i in range(1, len(aa) ):
            url = '%s?series_id=%s&api_key=FRED_API_KEY' % (self.ssurl,
                     aa[i][0])
            aa[i].append(url)
        self.seriesdict[cid] = aa

    def getseries(self):
        """ getseries

        collect series data for all categories collected
        """
        for k in self.categorydict.keys():
            aa = self.categorydict[k]
            assert aa[0][0] == 'cid'
            for i in range(1, len(aa) ):
                a = aa[i]
                cid = a[0]
            url = '%s&api_key=%s' % (self.csurl, cid, self.api_key)
            resp=self.uq.query(url)
            rstr = resp.read().decode('utf-8')
            aa = self.xa.xmlstr2aa(rstr)
            self.seriesdict[cid] = aa
            time.sleep(1)

    def showcategories(self):
        """ showcategories()

        display the categories in your browser
        """
        for k in self.categorydict.keys():
            self.ah.aashow(self.categorydict[k], 'FRED Categories')


    def reportcategories(self, ofp):
        """ reportcategories(ofp)

        report links to data for categories
        ofp - file pointer to output file
        """
        keys = []
        for k in self.categorydict.keys():
            aa = self.categorydict[k]
            for row in aa:
                rw = "','".join(row)
                print("'%s'" % (rw), file=ofp )

    def getcategorydata(self, rstr):
        """ getcategorydata(rstr)

        parse the html to find relative link to tags complete the url
        the FRED api doesn't seem to have an xml interface yet
        rstr - html string to parse
        """
        # print(rstr, file=sys.stderr)
        class MyHTMLParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.cid = None
                self.cdict = {}
                self.type = None
                self.burl = 'https://api.stlouisfed.org/fred/category/series'
            def handle_starttag(self, tag, attrs):
                if tag == 'a':
                    if self.type:
                        cid = attrs[0][1].split('/')[-1]
                        self.cid= cid
                        self.cdict[cid]={}
                        self.cdict[cid]['cid'] = cid
                        url = '%s?category_id=%s&api_key=%s' % (self.burl,
                            cid, '$FRED_API_KEY')
                        self.cdict[cid]['url'] = url
                        self.type = None
                if tag == 'p':
                    if len(attrs) and 'fred-categories-parent' in attrs[0][1]:
                        self.type = 'parent'
                if tag == 'span':
                    if len(attrs) and 'fred-categories-child' in attrs[0][1]:
                        self.type = 'child'
            def handle_endtag(self, tag):
                pass
            def handle_data(self, data):
                if data and self.cid:
                    self.cdict[self.cid]['name'] = data
                    self.cid = None

        parser = MyHTMLParser()
        parser.feed(rstr)
        aa = []
        aa.append(['cid','name','url'])
        for k in parser.cdict.keys():
            c = []
            c.append(parser.cdict[k]['cid'])
            c.append(parser.cdict[k]['name'])
            c.append(parser.cdict[k]['url'])
            aa.append(c)
        self.categorydict[0] = aa

    def getcategory(self, cid):
        """ getcategory(cid)

        collect data for a  category
        cid - category_id to collect
        """
        url = '%s?category_id=%s&api_key=%s' % (self.acurl, cid,
              self.api_key)
        resp = self.uq.query(url)
        rstr = resp.read().decode('utf-8')
        # print(rstr, file=sys.stderr)
        self.getcategorydata(rstr)

    def getcategories(self):
        """
        getcategories()

        collect all FRED categories
        """
        resp = self.uq.query(self.curl)
        rstr = resp.read().decode('utf-8')
        # print(rstr, file=sys.stderr)
        self.getcategorydata(rstr)

def main():
    argp = argparse.ArgumentParser(description='collect and report stlouisfed.org FRED categories and/or series')

    argp.add_argument('--categories', action='store_true', default=False,
                       help="report category data")
    argp.add_argument('--showcategories', action='store_true', default=False,
                       help="show categories in your browser")
    argp.add_argument('--series', action='store_true', default=False,
                       help="report series urls for categories collected")
    argp.add_argument('--showseries', action='store_true', default=False,
                       help="show series for a category in your browser")
    argp.add_argument('--observations', action='store_true', default=False,
                       help="report timeseries data for categories")

    argp.add_argument('--categoryid', help="categories are identified by\
          category_id")
    argp.add_argument('--seriesid', help="series are identified by series_id")

    argp.add_argument('--file', help="path to an output filename\n\
            if just a filename and--directory is not provided\
            the file is created in the current directory")
    argp.add_argument('--directory',
                    help="directory to write the output use --directory for\n\
                         storing observations, filenames autogenerated")

    args = argp.parse_args()

    if not args.categories and not args.series and not args.observations:
        argp.print_help()
        sys.exit()

    ofn = None
    fp = sys.stdout

    if not args.observations:
        if not args.directory and args.file:
            ofn = args.file
        elif args.directory and args.file:
            if '/' in args.file:
                argp.print_help()
                sys.exit()
            ofn = os.path.join(args.directory, args.file)
        if ofn:
            try:
                fp = open(ofn, 'w')
            except Exception as e:
                print('%s: %s' % (ofn, e) )

    fc = FREDcategories()
    if args.observations:
        if not args.directory:
            argp.print_help()
            sys.exit()
        if args.categoryid:
            fc.getseriesforcid(cid=args.categoryid)
            fc.getandreportobservations(odir=args.directory)
        else:
            fc.getcategories()
            fc.getseries()
            fc.getandreportobservations(odir=args.directory)
    elif args.series and args.categoryid:
        fc.getseriesforcid(cid=args.categoryid)
        if args.showseries:
            fc.showseries(args.categoryid)
            if fp != sys.stdout:
                fc.reportseries(args.categoryid, ofp=fp)
        else:
                fc.reportseries(args.categoryid, ofp=fp)
    elif args.series and args.seriesid:
        fc.getseriesforsid(sid=args.seriesid)
        fc.reportseries(args.seriesid, ofp=fp)
    elif args.categories:
        fc.getcategories()
        if args.showcategories:
            fc.showcategories()
            if fp != sys.stdout:
                fc.reportcategories(ofp=fp)
        else:
            fc.reportcategories(ofp=fp)

if __name__ == '__main__':
    main()
