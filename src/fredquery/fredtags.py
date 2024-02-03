#! env python

# return information on tags
#
# XXX print to output file param or sys.stdout
#

import os
import sys
import argparse
import re
import urllib.request
import xml
from xml.etree import ElementTree as ET

class FREDtags():
    def __init__(self):
        self.turl = 'https://api.stlouisfed.org/fred/tags'
        self.tsurl = '%s/series' % self.turl
        self.surl = 'https://api.stlouisfed.org/fred/series'
        self.sourl = '%s/series/observations' % self.surl
        self.kurl = 'https://fred.stlouisfed.org/docs/api/api_key.html'
        self.npages = 30
        self.tagdict = {}
        self.seriesdict = {}
        self.rapi_key = 'YOURAPIKEYGOESHERE'
        if 'FREDKEY' in os.environ:
            self.api_key = os.environ['FREDKEY']
        else:
            print('FRED api_key required: %s' % (self.kurl), file=sys.stderr)
            sys.exit()

    def query(self, url=None):
        """query - query an url
         url  - required
        """
        try:
            req = urllib.request.Request(url)
            resp = urllib.request.urlopen(req)
            return resp
        except urllib.error.URLError as e:
            print("Error %s(%s): %s" % ('query', url, e.reason),
                  file=sys.stderr),
            sys.exit(1)

    # XXX add output file param and print to that
    def reportseries(self, ofp):
        """ reportseries - report series for all collected
        """
        if not ofp: ofp = sys.stderr
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
                ra.append("'%s'," % self.seriesdict[sid][rk])
            print(''.join(ra), file=ofp)

    def getseriesdata(self, rstr):
        """parse the xml to find relative link to tags
           complete the url and return it
        """
        # print(rstr)
        xroot = ET.fromstring(rstr)
        for child in xroot:
            #print(child.tag, child.attrib)
            adict = child.attrib
            if 'DISCONTINUED' in child.attrib['title']:
                continue
            id = child.attrib['id']
            url = '%s?series_id=%s&api_key=%s' % (self.sourl, id, self.rapi_key)
            if len(id.split() ) > 1:
                print('getseriesdata: %s' % (child.attrib), file=sys.stderr)
            self.seriesdict[id]={}
            for k in child.attrib.keys():
                self.seriesdict[id][k] = child.attrib[k]
            self.seriesdict[id]['url'] = url

    def getseriesforsid(self, sid):
        """ getseriesforsid get series for a series_id
            sid - series_id - required
        """
        if not sid:
            print('getseriesfromsid: sid required', file=sys.stderr)
            sys.exit(1)
        url = '%s?series_id=%s&api_key=%s' % (self.surl, sid, self.api_key)
        resp = self.query(url)
        rstr = resp.read().decode('utf-8')
        self.getseriesdata(k, rstr)

    def getseries(self):
        """ getseries get series for all tags collected
        """
        for k in self.tagdict.keys():
            # XXX eliminate illegal tag names and escape spaces in others
            if ' ' in k:
               print('getseries: %s' % (self.tagѕict[k]),
                     file=sys.stderr)
               continue
            url = '%s?tag_names=%s&api_key=%s' % (self.tsurl, k, self.api_key)
            resp = self.query(url)
            rstr = resp.read().decode('utf-8')
            self.getseriesdata(k, rstr)

    def reporttags(self, ofp):
        """ reporttags - report for all tags collected
        """
        if not ofp: ofp = sys.stderr
        ha = []
        for tnm in self.tagdict.keys():
            ka = self.tagdict[tnm].keys()
            ra = []
            if len(ha) == 0:
                for k in ka:
                    ha.append("'%s'," % k)
                print(''.join(ha), file=ofp)
            ra=[]
            for rk in ka:
                ra.append("'%s'," % self.tagdict[tnm][rk])
            print(''.join(ra), file=ofp)

    def gettagdata(self, rstr):
        """parse the xml for FRED tags
        """
        xroot = ET.fromstring(rstr)
        for child in xroot:
            adict = child.attrib
            nm = child.attrib['name']
            self.tagdict[nm]={}
            for k in child.attrib.keys():
                self.tagdict[nm][k] = child.attrib[k]

    def getseriesfortnm(self, tnm):
        """ getseriesfortnm get series for a tag_id
            tnm - tag_name - required
        """
        if not tnm:
            print('getseriesfromtnm: tnm required', file=sys.stderr)
            sys.exit(1)
        url = '%s?tag_names=%s&api_key=%s' % (self.tsurl, tnm, self.api_key)
        resp = self.query(url)
        rstr = resp.read().decode('utf-8')
        self.getseriesdata(rstr)

    def gettags(self):
        url = '%s?api_key=%s' % (self.turl, self.api_key)
        resp = self.query(url)
        rstr = resp.read().decode('utf-8')
        self.gettagdata(rstr)

def main():

    argp = argparse.ArgumentParser(description='collect and report stlouisfed.org FRED tags and/or their series')
    argp.add_argument('--tags', action='store_true', default=False,
       help='return tags')
    argp.add_argument('--tagsandseries', action='store_true', default=False,
       help='return all series for all tags - not recommended')
    argp.add_argument('--series', action='store_true', default=False,
       help='return series for a tag_id or for a series_id')

    argp.add_argument('--tagname', required=False,
       help='tag_id identifies a FRED tag')
    argp.add_argument('--seriesid', required=False,
       help='series_id - identifies a series')

    argp.add_argument('--file', required=False,
       help='save the output to the file specified')
    args=argp.parse_args()

    if not args.tags and not args.series and not args.tagsandseries:
        argp.print_help()
        sys.exit(1)

    fp = sys.stdout
    if args.file:
        try:
            fp = open(args.file, 'w')
        except Exception as e:
            print('%s: %s' % (args.file, e), file=sys.stderr )
            sys.exit(1)
    fr = FREDtags()
    if args.series and args.tagname:
        fr.getseriesfortnm(tnm=args.tagname)
        fr.reportseries(ofp=fp)
    elif args.series and rgs.seriesid:
        fr.getseriesforsid(sid=args.seriesid)
        fr.reportseries(ofp=fp)
    elif args.tags:
        fr.gettags()
        fr.reporttags(ofp=fp)
    elif args.releasesandseries:
        while True:
            try:
                ans = input("Are you sure that you want to retrieve all series for all tags? It will pull enormous amounts of data and will possibly exceed the rate limit (yN): ")
            except ValueError:
                print("Sorry, I didn't understand that.")
                # No valid input will restart loop.
                continue
            else:
                break

        if isinstance(ans, str):
            if ans == 'y':
                fr.gettags()
                fr.getseries()
                fr.reportseries(ofp=fp)
            else:
                print("Good choice.")
                sys.exit(0)
        else:
            print("Good choice.")
            sys.exit(0)


main()
