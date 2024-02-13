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
        """ FREDreleases

        collects categories, their releases, series for the release
        and observations(timeseries data) for the series
        """
        # fred releases
        self.rurl = 'https://api.stlouisfed.org/fred/releases'
        self.releasedict = {}
        # fred release tables
        self.rturl = 'https://api.stlouisfed.org/fred/release/tables'
        self.releasetabledict = {}
        # series for a release id
        self.rsurl = 'https://api.stlouisfed.org/fred/release/series'
        self.seriesdict = {}
        self.surl = 'https://api.stlouisfed.org/fred/series'
        # observations for a series id
        self.sourl = 'https://api.stlouisfed.org/fred/series/observations'
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
        self.npages  = 7
        self.rid     = None
        self.sid     = None
        self.pause = 2 # number of seconds to pause
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

    def reportobservations(self, odir):
        """ reportobservations(odir)

        report category timeseries
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
            for k in ka:
                obs[k] = adict[k]
            self.observationsdict[sid].append(obs)

    def getobservations(self):
        """ getobservations()

        time series data for all series collected
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
        """ reportseries(ofp)

        report all series collected
        ofp - file pointer to which to write
        """
        if not ofp: ofp=sys.stdout
        ha = []
        for id in self.seriesdict:
            ka = self.seriesdict[id].keys()
            if len(ha) == 0:
                for f in ka:
                    ha.append("'%s'," % (f) )
                print(''.join(ha), file=ofp)
            ra=[]
            for k in ka:
                ra.append("'%s'," % (self.seriesdict[id][k]) )
            print(''.join(ra), file=ofp)

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

    def getseriesforsid(self, sid):
        """ getseriesforsid(sid)

        get a series for a series_id
        sid - series_id - required
        """
        if not sid:
            print('getseriesforsid: sid required', file=stderr)
            sys.exit(1)
        url = '%s?series_id=%s&api_key=%s' % (self.surl, sid,
                                              self.api_key)
        resp = self.query(url)
        rstr = resp.read().decode('utf-8')
        self.getseriesdata(rstr)

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

        get all series for all releases collected
        """
        # a series is associated with a release
        for k in self.releasedict.keys():
            nurl = '%s?release_id=%s' % (self.rsurl, rid)
            if nurl not in self.seriesdict:
                url = '%s?release_id=%s&api_key=%s' % (self.rsurl,
                                               k, self.api_key)
                resp = self.query(url)
                rstr = resp.read().decode('utf-8')
                self.getseriesdata(rstr)
                # trying to avoid dups
                self.seriesdict[nurl] = 1
                time.sleep(1)

    # XXX nested organization - csv representation doesn't make sense
    # def reportreleasetables(self, ofp):

    # XXX nested organization - csv representation doesn't make sense
    # XXX finish me
#    def getreleasetabledata(self, rstr):
#        """ getreleasetabledata - collect data for a release table
#            NOT TESTED
#            rstr - response string for the api query
#
#        """
#        xroot = ET.fromstring(rstr)
#        rid = None
#        nm  = None
#        for child in xroot:
#            sid = None
#            eid = None
#            if child.tag == 'release_id':
#                rid = child.text
#                self.releasetabledict[rid]={}
#                continue
#            elif child.tag == 'name':
#                self.releasetabledict[rid]['name']=child.text
#                continue
#            elif child.tag == 'element_id':
#                self.releasetabledict[rid]['element_id']=child.text
#                continue
#            elif child.tag == 'element':
#                self.releasetabledict[rid]['elements']=[]
#                elementdict={}
#                for gchild in child:
#                    if gchild.tag == 'children':
#                        elementdict['children'] = []
#                        childdict = {}
#                        for ggchild in gchild:
#                            if ggchild.text != None:
#                                childdict[gchild.tag] = ggchild.text
#                                continue
#                        elementdict['children'].append(childdict)
#                    elif gchild.text != None:
#                        elementdict[gchild.tag] = gchild.text
#                        continue
#                self.releasetabledict[rid]['elements'].append(elementdict)
#            else:
#                if rid and nm: self.releasetabledict[rid]['name'] = nm
#                if rid and eid: self.releasetabledict[rid]['element_id'] = eid

    def getreleasetable(self, rid):
        """ getreleasetable(rid)

        get a release table fir a release_id
        rid - release_id
        """
        if not rid:
            print('getseriesforrid: rid required', file=stderr)
            sys.exit(1)
        url = '%s?release_id=%s&api_key=%s' % (self.rturl, rid, self.api_key)
        resp=self.query(url)
        rstr = resp.read().decode('utf-8')
        self.getreleasetabledata(rstr)

    def getreleasetables(self):
        """ getreleasetables()

        get release tables for all releases collected
        """
        for rid in self.releasedict.keys():
            self.getreleasetable(rid)

    def reportreleases(self, ofp):
        """reportreleases(ofp)

        report data on all Dreleases collected
        ofp - file pointer to which to write
        """
        if not ofp: ofp=sys.stdout
        ha = []
        for id in self.releasedict.keys():
            ka =  self.releasedict[id].keys()
            # header
            if len(ha) == 0:
                for k in ka:
                    ha.append("'%s'," % k)
                print(''.join(ha), file=ofp)
            # record
            ra    = []
            for k in ka:
                ra.append("'%s'," % self.releasedict[id][k])
            print(''.join(ra), file=ofp)

    def getreleasedata(self, rstr):
        """ getreleasedata(rstr)

        collect data on a FRED release
        rstr - xml response string for the api query
        """
        xroot = ET.fromstring(rstr)
        for child in xroot:
            id = child.attrib['id']
            ka = child.attrib.keys()
            self.releasedict[id] = {}
            url = '%s?release_id=%s&api_key=%s' % (self.rurl, id, self.rapi_key)
            for k in ka:
                self.releasedict[id][k] = child.attrib[k]
            self.releasedict[id]['url'] = url
            if 'link' not in ka: self.releasedict[id]['link'] = ''

    def getreleases(self):
        """ getreleases()

        collect all releases
        """
        url = '%s?api_key=%s' % (self.rurl, self.api_key)
        resp = self.query(url)
        rstr = resp.read().decode('utf-8')
        #  print(rstr)
        self.getreleasedata(rstr)

def main():
    argp = argparse.ArgumentParser(description='collect and report stlouisfed.org  FRED releases and/or their time series')

    argp.add_argument('--releases', action='store_true', default=False,
       help='return releases')
    argp.add_argument('--series', action='store_true', default=False,
       help='return series by series_id or by release_id')
    argp.add_argument('--observations', action='store_true', default=False,
       help='return timeseries for all series collected')

    argp.add_argument('--releaseid', required=False,
       help='a release_id identifies a FRED release')
    argp.add_argument('--seriesid', required=False,
       help='a series_id identifies a FRED series')

    argp.add_argument('--file', help="path to an output filename\n\
            if just a filename and--directory is not provided\
            the file is created in the current directory")
    argp.add_argument('--directory',
                    help="directory to write the output, if --observations\
                         filenames are autogenerated")

    args=argp.parse_args()

    if not args.releases and not args.series and not args.observations:
        argp.print_help()
        sys.exit(1)

    ofn=None
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

    fr = FREDreleases()

    if args.observations:
        if not args.directory:
            argp.print_help()
            sys.exit()
        if args.releaseid:
            fr.getseriesforrid(args.releaseid)
            fr.getandreportobservations(odir=args.directory)
        else:
            fr.getreleases()
            fr.getseries()
            fr.getandreportobservations(odir=args.directory)
    elif args.series and args.releaseid:
        fr.getseriesforrid(rid=args.releaseid)
        fr.reportseries(ofp=fp)
    elif args.series and args.seriesid:
        fr.getseriesforsid(sid=args.seriesid)
        fr.reportseries(ofp=fp)
    elif args.releases:
        fr.getreleases()
        fr.reportreleases(ofp=fp)

if __name__ == '__main__':
    main()
