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
        self.tagdict = {}
        self.seriesdict = {}
        self.rapi_key = 'YOURAPIKEYGOESHERE'
        if 'FRED_API_KEY' in os.environ:
            self.api_key = os.environ['FRED_API_KEY']
        else:
            print('FRED api_key required: %s' % (self.kurl), file=sys.stderr)
            print('assign this key to FRED_API_KEY env variable',
                                  file=sys.stderr)
            sys.exit()
        self.pause = 2 # number of seconds to pause
        self.tid     = None
        self.sid     = None
        self.observationsdict = {}

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

    def reportobservations(self, odir):
        """
        reportobservations - report category timeseries
        rstr - decoded response of a urllib request
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


    def getseriesobservationdata(self, sid, rstr):
        """
        getseriesobservationdata - parse the observation xml
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
        """
        getobservations - time series data for all series collected
        """
        for sid in self.seriesdict:
            url = '%s?series_id=%s&api_key=%s' % (self.sourl, sid,
                   self.api_key)
            resp = self.query(url)
            rstr = resp.read().decode('utf-8')
            # observation data doesn't identify itself
            self.getseriesobservationdata(sid, rstr)
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
            time.sleep(1)

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

    def gettags(self):
        url = '%s?api_key=%s' % (self.turl, self.api_key)
        resp = self.query(url)
        rstr = resp.read().decode('utf-8')
        self.gettagdata(rstr)

def main():

    argp = argparse.ArgumentParser(description='collect and report stlouisfed.org FRED tags and/or their series')
    argp.add_argument('--tags', action='store_true', default=False,
       help='return tags')
    argp.add_argument('--series', action='store_true', default=False,
       help='return series for a tag_id or for a series_id')
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
                sys.exit()

    ft = FREDtags()

    if args.observations:
        if not args.directory:
            argp.print_help() 
            sys.exit()
        if args.tagname:
            ft.getseriesfortnm(tnm=args.tagname)
            ft.getandreportobservations(odir=args.directory)
        else:
            ft.gettags()
            ft.getseries()
            ft.getandreportobservations(odir=args.directory)
    elif args.series and args.tagname:
        ft.getseriesfortnm(tnm=args.tagname)
        ft.reportseries(ofp=fp)
    elif args.series and rgs.seriesid:
        ft.getseriesforsid(sid=args.seriesid)
        ft.reportseries(ofp=fp)
    elif args.tags:
        ft.gettags()
        ft.reporttags(ofp=fp)

if __name__ == '__main__':
    main()
