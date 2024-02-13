
#! env python

# return information on sources and their releases
#

import os
import sys
import argparse
import re
import time
import urllib.request
import xml
from xml.etree import ElementTree as ET

class FREDsources():

    def __init__(self):
        """ FREDsources

        collects sources and their releases
        data
        """
        # fred sources
        self.surl = 'https://api.stlouisfed.org/fred/sources'
        self.osurl = 'https://api.stlouisfed.org/fred/source'
        self.sourcedict = {}
        # releases for a source_id
        self.srurl = 'https://api.stlouisfed.org/fred/source/releases'
        self.releasedict = {}
        self.rurl = 'https://api.stlouisfed.org/fred/releases'
        # series for a release id
        self.rsurl = 'https://api.stlouisfed.org/fred/release/series'
        self.seriesdict = {}
        # observations for a series id
        self.sourl = 'https://api.stlouisfed.org/fred/series/observations'
        self.observationsdict = {}
        # url for getting a FRED api_key
        self.kurl = 'https://fred.stlouisfed.org/docs/api/api_key.html'
        # probably a bad idea to put your real api_key in a report
        self.rapi_key = 'YOURAPIKEYGOESHERE'
        if 'FRED_API_KEY' in os.environ:
            self.api_key = os.environ['FRED_API_KEY']
        else:
            print('FRED api_key required: %s' % (self.kurl), file=sys.stderr)
            print('assign this key to FRED_API_KEY env variable',
                                  file=sys.stderr)
            sys.exit()
        self.pause = 2 # number of seconds to pause
        self.sid     = None
        self.rid     = None

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
        """query(url)

        query an url
        url - url to collect
        """
        try:
            req = urllib.request.Request(url)
            resp = urllib.request.urlopen(req)
            return resp
        except urllib.error.URLError as e:
            print("Error %s(%s): %s" % ('query', url, e.reason),
                  file=sys.stderr),
            sys.exit(1)

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

    def getseriesobservationdata(self, sid, units, rstr):
        """ getseriesobservationdata(sid, rstr)

        parse the observation xml
        sid - series id because the observation data doesn't have it
        rstr - decoded response of a urllib request
        """
        xroot = ET.fromstring(rstr)
        self.observationsdict[sid]=[]
        for child in xroot:
            adict = child.attrib
            #print(child.tag, child.attrib, file=sys.stderr)
            ka = adict.keys()
            obs={}
            obs['sid']   = sid
            obs['units'] = units
            for k in ka:
                obs[k] = adict[k]
            self.observationsdict[sid].append(obs)

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

    def getseriesdata(self, rstr):
        """ getseriesdata(rstr)

        collect the data for a series for a release
        rstr - response string for the api query
        """
        xroot = ET.fromstring(rstr)
        for child in xroot:
            id = child.attrib['id']
            ka = child.attrib.keys()
            self.seriesdict[id] = {}
            for k in ka:
                self.seriesdict[id][k] = child.attrib[k]
            self.seriesdict[id]['url'] =\
              '%s?series_id=%s&api_key=%s' % (self.sourl, id, self.rapi_key)

    def getseriesforrid(self, rid):
        """ getseriesforrid(rid)

        get all series for a release_id
        rid - release_id - required
        """
        if not rid:
            print('getseriesforrid: rid required', file=stderr)
            sys.exit(1)
        url = '%s?release_id=%s&api_key=%s' % (self.rsurl,
                                           rid, self.api_key)
        resp = self.query(url)
        rstr = resp.read().decode('utf-8')
        self.getseriesdata(rstr)

    def getseries(self):
        """ getseries()

        convenience function to get series data for a source
        """
        for rid in self.releasedict.keys():
            self.getseriesforrid(rid)
            time.sleep(1)


    def reportreleases(self, ofp):
        """ reportreleases(ofp)

        report all releases collected
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
        """ getreleasedata(sid, rstr)

        collect the data for a release
        sid - source_id
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

    def getreleases(self):
        """ getreleases()

        collect all releases for sources collected
        """
        for sid in self.sourcedict:
            url = '%s?source_id=%s&api_key=%s' % (self.srurl, sid, self.api_key)
            resp=self.query(url)
            rstr = resp.read().decode('utf-8')
            self.getreleasedata(sid, rstr)
            time.sleep(1)

    def reportsources(self, ofp):
        """reportsources(ofp)

        report data on all sources collected
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
        """ sourcedata(rstr)

        collect source data for a FRED source
        rstr - xml response string for the api query
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

    def getsource(self, sid):
        """ getsource(sid)

        collect FRED source for a source_id
        """
        url = '%s?source_id=%s&api_key=%s' % (self.osurl, sid, self.api_key)
        resp = self.query(url)
        rstr = resp.read().decode('utf-8')
        #  print(rstr)
        self.getsourcedata(rstr)

    def getsources(self):
        """ getsources()

        collect all FRED sources
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
    argp.add_argument('--observations', action='store_true', default=False,
       help='return observations for a source_id')

    argp.add_argument('--sourceid', required=False,
       help='a source_id identifies a FRED source')

    argp.add_argument('--file', help="path to an output filename\n\
            if just a filename and--directory is not provided\
            the file is created in the current directory")
    argp.add_argument('--directory',
                    help="directory to write the output, if --observations\
                         filenames are autogenerated")

    args=argp.parse_args()

    if not args.sources and not args.releases and not args.observations:
        argp.print_help()
        sys.exit(1)

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

    fs = FREDsources()

    if args.observations:
        if not args.directory:
            argp.print_help()
            sys.exit()
        if args.sourceid:
            fs.getsource(sid = args.sourceid)
            fs.getreleases()
            fs.getseries()
            fs.getandreportobservations(odir=args.directory)
        else:
            fs.getsource()
            fs.getreleases()
            fr.getseries()
            fs.getandreportobservations(odir=args.directory)
    elif args.sources:
        fs.getsources()
        fs.reportsources(ofp=fp)
    elif args.releases and args.sourceid:
        fs.getsource(sid = args.sourceid)
        fs.getreleases()
        fs.reportreleases(ofp=fp)
    elif args.sources and args.sourceid:
        fs.getsource(sid = args.sourceid)
        fs.reportsources(odir=args.directory)
    elif args.releases:
        fs.getsources()
        fs.getreleases()
        fs.reportreleases(ofp=fp)

if __name__ == '__main__':
    main()
