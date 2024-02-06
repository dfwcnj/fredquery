
#! env python

# return information on releases or their sries
#

import os
import sys
import argparse
import re
import time
import urllib.request
import xml
from xml.etree import ElementTree as ET

class FREDreleases():

    def __init__(self):
        # fred sources
        self.surl = 'https://api.stlouisfed.org/fred/sources'
        self.sourcedict = {}
        # releases for a source_id
        self.srurl = 'https://api.stlouisfed.org/fred/source/releases'
        self.releasedict = {}
        self.rurl = 'https://api.stlouisfed.org/fred/releases'
        # url for getting a FRED api_key
        self.kurl = 'https://fred.stlouisfed.org/docs/api/api_key.html'
        # probably a bad idea to put your real api_key in a report
        self.rapi_key = 'YOURAPIKEYGOESHERE'
        if 'FREDKEY' in os.environ:
            self.api_key = os.environ['FREDKEY']
        else:
            print('FRED api_key required: %s' % (self.kurl), file=sys.stderr)
            sys.exit()
        self.sid     = None
        self.rid     = None

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

    def reportreleases(self, ofp):
        """ reportreleases - report all sources collected
            ofp - file pointer to which to write
        """
        if not ofp: ofp=sys.stdout
        ha = []
        for id in self.releasedict.keys():
            ka = self.releasedict[id].keys()
            if len(ha) == 0:
                for f in ka:
                    ha.append("'%s'," % (f) )
                print(''.join(ha), file=ofp)
            ra=[]
            for k in ka:
                ra.append("'%s'," % (self.releasedict[id][k]) )
            print(''.join(ra), file=ofp)

    def getreleasedata(self, sid, rstr):
        """ getreleasedata - collect the data for a release
            rstr - response string for the api query
        """
        xroot = ET.fromstring(rstr)
        for child in xroot:
            id = child.attrib['id']
            ka = child.attrib.keys()
            self.releasedict[id] = {}
            self.releasedict[id]['source_id'] = sid
            self.releasedict[id]['sourcename'] = self.sourcedict[sid]['name']
            for k in ka:
                self.releasedict[id][k] = child.attrib[k]
            self.releasedict[id]['url'] =\
              '%s?release_id=%s&api_key=%s' % (self.rurl, id, self.rapi_key)

    def getreleasesforsid(self, sid):
        """ getreleaseforsid - collect the data for a release for a source_id
            sid - source_id
        """
        xroot = ET.fromstring(rstr)
        url = '%s?source_id=%s&api_key=%s' % (self.srurl, sid, self.api_key)
        resp=self.query(url)
        rstr = resp.read().decode('utf-8')
        self.getreleasedata(sid, rstr)

    def getreleases(self):
        """ getreleases - collect all releases for sources collected
            sid - source_id
        """
        xroot = ET.fromstring(rstr)
        for sid in self.sourcedict:
            url = '%s?source_id=%s&api_key=%s' % (self.srurl, sid, self.api_key)
            resp=self.query(url)
            rstr = resp.read().decode('utf-8')
            self.getreleasedata(sid, rstr)
            time.sleep(1)

    def reportsources(self, ofp):
        """reportreleases - report data on all Dreleases collected
           ofp - file pointer to which to write
        """
        if not ofp: ofp=sys.stdout
        ha = []
        for id in self.sourcedict.keys():
            ka =  self.sourcedict[id].keys()
            # header
            if len(ha) == 0:
                for k in ka:
                    ha.append("'%s'," % k)
                print(''.join(ha), file=ofp)
            # record
            ra    = []
            for k in ka:
                ra.append("'%s'," % self.sourcedict[id][k])
            print(''.join(ra), file=ofp)

    def getsourcedata(self, rstr):
        """ sourcedata - collect data on a FRED release
            rstr - response string for the api query
        """
        xroot = ET.fromstring(rstr)
        for child in xroot:
            id = child.attrib['id']
            ka = child.attrib.keys()
            self.sourcedict[id] = {}
            url = '%s?source_id=%s&api_key=%s' % (self.srurl, id, self.rapi_key)
            for k in ka:
                self.sourcedict[id][k] = child.attrib[k]
            self.sourcedict[id]['url'] = url
            if 'link' not in ka: self.sourcedict[id]['link'] = ''

    def getsources(self):
        """ getsources - collect all sources
        """
        url = '%s?api_key=%s' % (self.surl, self.api_key)
        resp = self.query(url)
        rstr = resp.read().decode('utf-8')
        #  print(rstr)
        self.getsourcedata(rstr)

def main():
    argp = argparse.ArgumentParser(description='collect and report stlouisfed.org  FRED sources and/or their releases')

    argp.add_argument('--sources', action='store_true', default=False,
       help='return sources')
    argp.add_argument('--releases', action='store_true', default=False,
       help='return releases for a source_id')

    argp.add_argument('--sourceid', required=False,
       help='a source_id identifies a FRED source')

    argp.add_argument('--file', help="path to an output filename\n\
            if just a filename and--directory is not provided\
            the file is created in the current directory")

    args=argp.parse_args()

    if not args.sources and not args.releases:
        argp.print_help()
        sys.exit(1)

    fp = sys.stdout

    if args.file:
        try:
            fp = open(args.file, 'w')
        except Exception as e:
            print('%s: %s' % (args.file, e) )
            sys.exit(1)

    fs = FREDreleases()

    if args.sources:
        fs.getsources()
        fs.reportsources(ofp=fp)
    elif args.releases and args.sourceid:
        fs.getreleasesforsid(sid = args.sourceid)
        fs.reportreleases(ofp=fp)
    elif args.releases:
        fs.getsources()
        fs.getreleases()
        fs.reportreleases(ofp=fp)

main()
