#! env python

# return information on tags
#
# report tags, their releases, or their series
#

import os
import sys
import argparse
import re
import urllib.request
import time
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

class FREDtags():
    def __init__(self):
        """ FREDtags

        collects FRED tags, their releases, their series, and their
        observations(timeseries data)
        """
        self.turl = 'https://api.stlouisfed.org/fred/tags'
        self.tsurl = '%s/series' % self.turl
        self.surl = 'https://api.stlouisfed.org/fred/series'
        self.sourl = '%s/observations' % self.surl
        self.kurl = 'https://fred.stlouisfed.org/docs/api/api_key.html'
        self.npages = 30
        self.tnm = None
        self.tagdict = {}
        self.seriesdict = {}
        self.rapi_key = '$FRED_API_KEY'
        if 'FRED_API_KEY' in os.environ:
            self.api_key = os.environ['FRED_API_KEY']
        else:
            print('FRED api_key required: %s' % (self.kurl), file=sys.stderr)
            print('assign this key to FRED_API_KEY env variable',
                                  file=sys.stderr)
            sys.exit()
        self.verbose = False
        self.pause   = 2 # number of seconds to pause
        self.retries = 5 # number of seconds to pause
        self.tid     = None
        self.sid     = None
        self.observationsdict = {}

        self.uq = query._URLQuery()
        self.ah = aa2html._AA2HTML()
        self.xa = xmlstr2aa._XMLStr2AA()

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
            keys=[]
            for obs in obsa:
                rw = "','".join(obs)
                print("'%s'" % (rw), file=fp )

    def getandreportobservations(self, odir):
        """ getandreportobservations()

        incrementally get and store observation data for all
        series collected
        observation = time series data
        """
        for id in self.seriesdict.keys():
            aa = self.seriesdict[id]
            assert aa[0][0] == 'id'
            assert aa[0][8] == 'units'
            for i in range(1, len(aa) ):
                a = aa[i]
                id = a[0]
                units = a[8]
                url = '%s?series_id=%s&api_key=%s' % (self.sourl, id,
                      self.api_key)
                resp = self.uq.query(url)
                rstr = resp.read().decode('utf-8')
                # observation data doesn't identify itself
                obsa = self.xa.xmlstr2aa(rstr)
                self.reportobservation(id, units, obsa, odir)
                time.sleep(1)

    def showseries(self):
        """ showseries()

        show series for a tagname in your browser
        """
        for k in self.seriesdict.keys():
            self.ah.aashow(self.seriesdict[k],
                'FRED Tagname %s series' % k)

    def reportseries(self, ofp):
        """ reportseries - report series for all collected
        """
        hdr = []
        for k in self.seriesdict.keys():
            aa =  self.seriesdict[k]
            for a in aa:
                row = "','".join(a)
                print("'%s'" % (row), file=ofp)

    def getseriesforsid(self, sid):
        """ getseriesforsid get series for a series_id
            sid - series_id - required
        """
        if not sid:
            print('getseriesfromsid: sid required', file=sys.stderr)
            sys.exit(1)
        self.sid = sid
        url = '%s?series_id=%s&api_key=%s' % (self.surl, sid, self.api_key)
        resp = self.uq.query(url)
        rstr = resp.read().decode('utf-8')
        aa = self.xa.xmlstr2aa(rstr)
        if len(aa) == 0:
            print('getseriesforrid(rid): no data' % (sid), file=sys.stderr)
            return
        self.seriesdict[sid] = aa

    def getseriesfortnm(self, tnm):
        """ getseriesfortnm get series for a tag_id
            tnm - tag_name - required
        """
        if not tnm:
            print('getseriesfromtnm: tnm required', file=sys.stderr)
            sys.exit(1)
        self.tnm = tnm
        url = '%s?tag_names=%s&api_key=%s' % (self.tsurl, tnm, self.api_key)
        resp = self.uq.query(url)
        rstr = resp.read().decode('utf-8')
        aa = self.xa.xmlstr2aa(rstr)
        if len(aa) == 0:
            print('getseriesfortnm(tnm): no data' % (sid), file=sys.stderr)
            return
        self.seriesdict[tnm] = aa

    def getseries(self):
        """ getseries get series for all tags collected
        """
        aa = self.tagdict[0]
        assert aa[0][0] == 'name'
        for i in range(1, len(aa) ):
            a == aa[i]
            id = a[0]
            self.getseriesfortnm(id)
            time.sleep(1)

    def showtags(self):
        """ showtags()

        show FRED tags in your browser
        """
        for k in self.tagdict.keys():
            self.ah.aashow(self.tagdict[k], 'FRED Tags')


    def reporttags(self, ofp):
        """ reporttags - report for all tags collected
        """
        keys = []
        aa = self.tagdict[0]
        keys = aa[0]
        for i in range(1, len(aa) ):
            a = aa[i]
            row = "','".join(a)
            print("'%s'" % (row), file=ofp)

    def gettags(self):
        url = '%s?api_key=%s' % (self.turl, self.api_key)
        resp = self.uq.query(url)
        rstr = resp.read().decode('utf-8')
               #  print(rstr)
        aa = self.xa.xmlstr2aa(rstr)
        aa[0].append('url')
        for i in range(1, len(aa) ):
            id = aa[i][0]
            url = '%s?series_id=%s&api_key=FRED_API_KEY' % (self.tsurl, id)
            aa[i].append(url)
        self.tagdict[0] = aa

def main():

    argp = argparse.ArgumentParser(description='collect and report stlouisfed.org FRED tags and/or their series')
    argp.add_argument('--tags', action='store_true', default=False,
       help='return tags')
    argp.add_argument('--showtags', action='store_true', default=False,
       help='show tags in your browser')
    argp.add_argument('--series', action='store_true', default=False,
       help='return series for a tag_id or for a series_id')
    argp.add_argument('--showseries', action='store_true', default=False,
       help='show series for a tagname in your browser')
    argp.add_argument('--observations', action='store_true', default=False,
                       help="report timeseries data for tags")

    argp.add_argument('--tagname', required=False,
       help='tag_id identifies a FRED tag')
    argp.add_argument('--seriesid', required=False,
       help='series_id - identifies a series')

    argp.add_argument('--file', help="path to an output filename\n\
            if just a filename and--directory is not provided\
            the file is created in the current directory")
    argp.add_argument('--directory', required=False,
       help='save the output to the directory specified')

    args=argp.parse_args()

    if not args.tags and not args.series and not args.observations:
        argp.print_help()
        sys.exit(1)

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
                sys.exit()

    ft = FREDtags()

    if args.observations:
        if not args.directory:
            argp.print_help() 
            sys.exit()
        if args.tagname:
            ft.getseriesfortnm(args.tagname)
            ft.getandreportobservations(odir=args.directory)
        else:
            ft.gettags()
            ft.getseries()
            ft.getandreportobservations(odir=args.directory)
    elif args.series and args.tagname:
        ft.getseriesfortnm(args.tagname)
        if args.showseries:
            ft.showseries()
            if fp != sys.stdout:
                ft.reportseries(ofp=fp)
        else:
            ft.reportseries(ofp=fp)
    elif args.series and args.seriesid:
        ft.getseriesforsid(args.seriesid)
        ft.reportseries(ofp=fp)
    elif args.tags:
        ft.gettags()
        if args.showtags:
            ft.showtags()
            if fp != sys.stdout:
                ft.reporttags(ofp=fp)
        else:
            ft.reporttags(ofp=fp)

if __name__ == '__main__':
    main()
