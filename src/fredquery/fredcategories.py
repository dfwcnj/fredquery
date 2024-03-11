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
    from fredquery import dict2html
except ImportError as e:
    import query
    import dict2html

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
        self.rapi_key = '$FRED_API_KEY'
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
        self.dh = dict2html.Dict2HTML()

    def reportobservations(self, odir):
        """ reportobservations(odir)

        report category timeseries
        odir - directory that will hold the output
        """
        if not odir:
            print('no output directory provided', file=sys.stderr)
            sys.exit(0)
        for sid in self.observationsdict.keys():
            sfn=os.path.join('%s/%s_%s.csv' % (odir,
                    sid, self.seriesdict[sid]['units']) )
            fn = ''.join(sfn.split() )
            with open(fn, 'w') as fp:
                ha=[]
                for obs in self.observationsdict[sid]:
                    ka=obs.keys()
                    if len(ha) == 0:
                        for f in ka:
                            if f == 'value':
                                sv = '%s_%s' % (sid,
                                      self.seriesdict[sid]['units'])
                                ha.append("'%s'" % ''.join(sv.split()) )
                            else:
                                ha.append("'%s'" % f)
                        print(''.join(ha), file=fp )
                    ra = []
                    for rk in obs.keys():
                        ra.append("'%s'," % (obs[rk]) )
                    print(''.join(ra), file=fp )


    def getobservationdata(self, sid, rstr):
        """getobservationdata(sid, rstr)

        parse the observation xml
        rstr - decoded response of a urllib request
        """
        xroot = ET.fromstring(rstr)
        self.observationsdict[sid]=[]
        for child in xroot:
            adict = child.attrib
            #print(child.tag, child.attrib, file=sys.stderr)
            ka = adict.keys()
            obs={}
            for k in ka:
                obs[k] = adict[k]
            self.observationsdict[sid].append(obs)

    def getobservations(self):
        """ getobservations()

        time observation(timeseries) data for all series collected
        """
        for sid in self.seriesdict:
            url = '%s?series_id=%s&api_key=%s' % (self.sourl, sid,
                   self.api_key)
            resp = self.uq.query(url)
            rstr = resp.read().decode('utf-8')
            # observation data doesn't identify itself
            self.getobservationdata(sid, rstr)
            time.sleep(1)


    def returnseriesobservationdata(self, sid, units, rstr):
        """ returnseriesobservationdata(sid, units, rstr)

        parse the observation xml
        sid - series id because the observation data doesn't have it
        units - each observation is in this unit
        rstr - decoded response of a urllib request
        """
        xroot = ET.fromstring(rstr)
        self.observationsdict[sid]=[]
        obsa = []
        for child in xroot:
            adict = child.attrib
            #print(child.tag, child.attrib, file=sys.stderr)
            ka = adict.keys()
            obs={}
            obs['sid']   = sid
            obs['units'] = units
            for k in ka:
                obs[k] = adict[k]
            obsa.append(obs)
        return obsa

    def reportobservation(self, sid, units, obsa, odir):
        """ reportobservation(sid, obsa, odir)

        report observations for a series_id
        sid - series_id
        obsa - list of observations for a series_id
        odir - directory for storing observations
        """
        sfn = os.path.join('%s/%s_%s.csv' % (odir, sid, units) )
        # units can contain spaces
        fn = ''.join(sfn.split() )
        with open(fn, 'w') as fp:
            ha=[]
            for obs in obsa:
                ka = obs.keys()
                if len(ha) == 0:
                    for f in ka:
                        if f == 'value':
                            sv = '%s_%s' % (sid, units)
                            ha.append("'%s'" % ''.join(sv.split()) )
                        else:
                            ha.append("'%s'" % f)
                    print(''.join(ha), file=fp)
                ra=[]
                for rk in obs.keys():
                    ra.append("'%s'," % (obs[rk]) )
                print(''.join(ra), file=fp)

    def getandreportobservations(self, odir):
        """ getandreportobservations()

        incrementally get and store observation data for all
        series collected
        observation = time series data
        """
        for sid in self.seriesdict:
            url = '%s?series_id=%s&api_key=%s' % (self.sourl, sid,
                   self.api_key)
            units = self.seriesdict[sid]['units']
            resp = self.uq.query(url)
            rstr = resp.read().decode('utf-8')
            # observation data doesn't identify itself
            obsa = self.returnseriesobservationdata(sid, units, rstr)
            self.reportobservation(sid, units, obsa, odir)
            time.sleep(1)

    def showseries(self):
        """ showseries()

        show the series list for a category in your browser
        """
        self.dh.dictshow(self.seriesdict, 'Category %s series' % self.cid)

    def reportseries(self, ofp):
        """ reportseries(ofp)

        report series data for categories
        rstr - decoded response of a urllib request
        """
        hdr = None
        keys = []
        for k in self.seriesdict.keys():
            row = self.seriesdict[k]
            if len(keys) == 0:
                keys = [k for k in sorted(row.keys() )]
                hdr = "','".join(keys)
                print("'%s'" % (hdr), file=ofp )
            fa = [row[k] for k in keys]
            rw = "','".join(fa)
            print("'%s'" % (rw), file=ofp )

    def getseriesdata(self, rstr):
        """ getseriesdata(rstr)

        get series data for a category
        rstr - decoded response of a urllib request
        """
        xroot = ET.fromstring(rstr)
        for child in xroot:
            adict = child.attrib
            if 'DISCONTINUED' in adict['title']:
                continue
            #print(child.tag, child.attrib, file=sys.stderr)
            ka = adict.keys()
            id = adict['id']
            self.seriesdict[id]={}
            for k in ka:
                self.seriesdict[id][k] = adict[k]
            url='%s?series_id=%s&api_key=%s' % (self.sourl, adict['id'],
                self.rapi_key)
            self.seriesdict[id]['url'] = url

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
        self.getseriesdata(rstr)

    def getseriesforcid(self, cid):
        """ getseriesforcid(cid)

        collect series data for a category_id
        cid - category_id
        """
        self.cid = cid
        url = '%s?category_id=%s&api_key=%s' % (self.csurl, cid, self.api_key)
        resp=self.uq.query(url)
        rstr = resp.read().decode('utf-8')
        self.getseriesdata(rstr)

    def getseries(self):
        """ getseries

        collect series data for all categories collected
        """
        for cid in self.categorydict.keys():
            url = '%s&api_key=%s' % (self.csurl, cid, self.api_key)
            resp=self.uq.query(url)
            rstr = resp.read().decode('utf-8')
            self.getseriesdata(rstr)
            time.sleep(1)

    def showcategories(self):
        """ showcategories()

        display the categories in your browser
        """
        self.dh.dictshow(self.categorydict, 'FRED Categories')


    def reportcategories(self, ofp):
        """ reportcategories(ofp)

        report links to data for categories
        ofp - file pointer to output file
        """
        hdr = None
        keys = []
        for k in self.categorydict.keys():
            row = self.categorydict[k]
            if len(keys) == 0:
                keys = [k for k in sorted(row.keys() )]
                hdr = "','".join(keys)
                print("'%s'" % (hdr), file=ofp )
            fa = [row[k] for k in keys]
            rw = "','".join(fa)
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
        self.categorydict = parser.cdict

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
    fp = sys.stderr

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
            fc.showseries()
            if fp != sys.stdout:
                fc.reportseries(ofp=fp)
        else:
                fc.reportseries(ofp=fp)
    elif args.series and args.seriesid:
        fc.getseriesforsid(sid=args.seriesid)
        fc.reportseries(ofp=fp)
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
