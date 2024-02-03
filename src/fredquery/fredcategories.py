#! env python

# return information on categories
#
#

import os
import sys
import argparse
import html
from html.parser import HTMLParser
import re
import urllib.request
import xml
from xml.etree import ElementTree as ET

class FREDcategories():
    """
    collect and report stlouisfed.org FRED categories and/or their series.
    """
    def __init__(self):
        self.curl = 'https://fred.stlouisfed.org/categories'
        self.acurl = 'https://api.stlouisfed.org/fred/category'
        self.acsurl = 'https://api.stlouisfed.org/fred/category/series'
        self.asourl = 'https://api.stlouisfed.org/fred/series/observations'
        self.kurl = 'https://fred.stlouisfed.org/docs/api/api_key.html'
        self.rapi_key = 'YOURAPIKEYGOESHERE'
        if 'FREDKEY' in os.environ:
            self.api_key = os.environ['FAPI']
        else:
            print('FRED api_key required: %s' % (self.kurl), file=sys.stderr)
            sys.exit()
        self.npages  = 7
        self.catdict = {}
        self.seriesdict = {}
        self.seriesiddict = {}

    def query(self, url=None):
        """
         query - query an url
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

    def reportseries(self, ofp):
        """
        reportseries - report series data for categories
        rstr - decoded response of a urllib request
        """
        ha = []
        ka = self.seriesdict.keys()
        for k in ka:
            ra = []
            if len(ha) == 0:
                for k in self.seriesdict[k].keys():
                    ha.append("'%s'," % k)
                print(''.join(ha), file=ofp)
            ra=[]
            for rk in self.seriesdict[k].keys():
                ra.append("'%s'," % self.seriesdict[k][rk])
            print(''.join(ra), file=ofp)

    def getseriesdata(self, rstr):
        """
        getseriesdata - get series data for a category
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
            url='%s?series_id=%s&api_key=%s' % (self.asourl, adict['id'],
                self.rapi_key)
            self.seriesdict[id]['url'] = url
            for k in ka:
                self.seriesdict[id][k] = adict[k]

    def getseries(self):
        """
        getseries - collect series data for categories and report them
        """
        for cid in self.catdict.keys():
            url = '%s&api_key=%s' % (self.catdict[cid]['url'], self.api_key)
            resp=self.query(url)
            rstr = resp.read().decode('utf-8')
            self.getseriesdata(rstr)

    def reportcategories(self, ofp):
        """
        reportcategories - report links to data for categories
        """
        for k in self.catdict.keys():
            nm = self.catdict[k]['name']
            print("'%s','%s'" % (nm, k) )
            #url = '%s&api_key=%s' % (self.catdict[k]['url'], self.rapi_key)
            #print("'%s','%s'" % (nm, url), file=ofp )

    def getcategorydata(self, rstr):
        """
        parse the html to find relative link to tags complete the url
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
        self.catdict = parser.cdict

    def getcategories(self):
        """
        getcategories - collect all FRED categories
        """
        resp = self.query(self.curl)
        rstr = resp.read().decode('utf-8')
        # print(rstr, file=sys.stderr)
        self.getcategorydata(rstr)

def main():
    argp = argparse.ArgumentParser(description='collect and report stlouisfed.org FRED categories and/or series')
    argp.add_argument('--series', action='store_true', default=False,
                       help="report series urls for categories")
    argp.add_argument('--file', help="store the output in this file")
    args = argp.parse_args()

    fr = FREDcategories()
    if args.series:
        fp = sys.stdout
        if args.file:
            try:
                fp = open(args.file, 'w')
            except Exception as e:
                print('%s: %s' % (args.file, e) )
                sys.exit(1)
        fr.getcategories()
        fr.getseries()
        fr.reportseries(ofp=fp)
    else:
        if not args.file:
            fr.getcategories()
            fr.reportcategories(ofp=sys.stderr)
        else:
            with open(args.file, 'w') as fp:
                fr.getcategories()
                fr.reportcategories(ofp=fp)

main()
