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

class FREDcategories():
    """ FREDcategories

    collect and report stlouisfed.org FRED categories, their series, and
    their observations(timeseries data)
    """
    def __init__(self):
        self.curl = 'https://fred.stlouisfed.org/categories'
        self.acurl = 'https://api.stlouisfed.org/fred/category'
        self.csurl = 'https://api.stlouisfed.org/fred/category/series'
        self.sourl = 'https://api.stlouisfed.org/fred/series/observations'
        self.kurl = 'https://fred.stlouisfed.org/docs/api/api_key.html'
        self.pause = 2 # number of seconds to pause
        self.rapi_key = 'YOURAPIKEYGOESHERE'
        if 'FRED_API_KEY' in os.environ:
            self.api_key = os.environ['FRED_API_KEY']
        else:
            print('FRED api_key required: %s' % (self.kurl), file=sys.stderr)
            print('assign this key to FRED_API_KEY env variable',
                                  file=sys.stderr)
            sys.exit()
        self.npages  = 7
        self.categorydict= {}
        self.seriesdict = {}
        self.observationsdict = {}

    def setpause(self, secs):
        """setpause(secs)

        change the amount of delay between certain operations to
        try to avoit stlouisfed.org rate limits
        """
        si = None
        try:
            si = int(secs)
        except Exception as e:
            print('setpause(%s): %s' % (secs, e) )
            return
        self.pause = si

    def query(self, url=None):
        """ query(url) 
 
        retrieve a url
        url - content to retrieve
        """
        try:
            req = urllib.request.Request(url)
            resp = urllib.request.urlopen(req)
            return resp
        except urllib.error.URLError as e:
            print("Error %s(%s): %s" % ('query', url, e.reason),
                  file=sys.stderr),
            sys.exit(1)

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
            resp = self.query(url)
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
            resp = self.query(url)
            rstr = resp.read().decode('utf-8')
            # observation data doesn't identify itself
            obsa = self.returnseriesobservationdata(sid, units, rstr)
            self.reportobservation(sid, units, obsa, odir)
            time.sleep(1)

    def reportseries(self, ofp):
        """ reportseries(ofp)

        report series data for categories
        rstr - decoded response of a urllib request
        """
        ha = []
        ka = self.seriesdict.keys()
        for sid in ka:
            ra = []
            if len(ha) == 0:
                for k in self.seriesdict[sid].keys():
                    ha.append("'%s'," % k)
                print(''.join(ha), file=ofp)
            ra=[]
            for rk in self.seriesdict[sid].keys():
                if 'notes' not in self.seriesdict[sid].keys():
                    self.seriesdict[k]['notes']=''
                ra.append("'%s'," % self.seriesdict[sid][rk])
            print(''.join(ra), file=ofp)

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
            url='%s?series_id=%s&api_key=%s' % (self.sourl, adict['id'],
                self.rapi_key)
            self.seriesdict[id]['url'] = url
            for k in ka:
                self.seriesdict[id][k] = adict[k]

    def getseriesforsid(self, sid):
        """ getseriesforsid(sid)

        get a series for a series_id
        sid - series_id
        """
        if not sid:
            print('getseriesforsid: sid required', file=stderr)
            sys.exit(1)
        url = '%s?series_id=%s&api_key=%s' % (self.surl, sid,
                                              self.api_key)
        resp = self.query(url)
        rstr = resp.read().decode('utf-8')
        self.getseriesdata(rstr)

    def getseriesforcid(self, cid):
        """ getseriesforcid(cid)

        collect series data for a category_id
        cid - category_id
        """
        url = '%s?category_id=%s&api_key=%s' % (self.csurl, cid, self.api_key)
        resp=self.query(url)
        rstr = resp.read().decode('utf-8')
        self.getseriesdata(rstr)

    def getseries(self):
        """ getseries

        collect series data for all categories collected
        """
        for cid in self.categorydict.keys():
            url = '%s&api_key=%s' % (self.csurl, cid, self.api_key)
            resp=self.query(url)
            rstr = resp.read().decode('utf-8')
            self.getseriesdata(rstr)
            time.sleep(1)

    def reportcategories(self, ofp):
        """ reportcategories(ofp)

        report links to data for categories
        ofp - file pointer to output file
        """
        for k in self.categorydict.keys():
            nm = self.categorydict[k]['name']
            print("'%s','%s'" % (nm, k), file=ofp )

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
                        url = '%s?category_id=%s' % (self.burl, cid)
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
        resp = self.query(url)
        rstr = resp.read().decode('utf-8')
        # print(rstr, file=sys.stderr)
        self.getcategorydata(rstr)

    def getcategories(self):
        """
        getcategories()

        collect all FRED categories
        """
        resp = self.query(self.curl)
        rstr = resp.read().decode('utf-8')
        # print(rstr, file=sys.stderr)
        self.getcategorydata(rstr)

def main():
    argp = argparse.ArgumentParser(description='collect and report stlouisfed.org FRED categories and/or series')

    argp.add_argument('--categories', action='store_true', default=False,
                       help="report category data")
    argp.add_argument('--series', action='store_true', default=False,
                       help="report series urls for categories collected")
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
        fc.reportseries(ofp=fp)
    elif args.series and args.seriesid:
        fc.getseriesforsid(cid=args.seriesid)
        fc.reportseries(ofp=fp)
    elif args.categories:
        fc.getcategories()
        fc.reportcategories(ofp=fp)

if __name__ == '__main__':
    main()
