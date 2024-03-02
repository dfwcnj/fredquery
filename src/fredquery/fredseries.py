
#! env python

# return information on series, their categories, releases, sources, etc
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

from fredquery import common

class FREDseries():
    """ FREDseries

    collect and report stlouisfed.org FRED series, and
    their observations(timeseries data)
    """
    def __init__(self):
        self.surl = 'https://fred.stlouisfed.org/series'
        self.ssurl = 'https://api.stlouisfed.org/fred/series'
        self.sourl = 'https://api.stlouisfed.org/fred/series/observations'
        self.scurl = 'https://api.stlouisfed.org/fred/series/categories'
        self.srurl = 'https://api.stlouisfed.org/fred/series/release'
        self.sturl = 'https://api.stlouisfed.org/fred/series/tags'
        self.suurl = 'https://api.stlouisfed.org/fred/series/updates'
        self.kurl = 'https://fred.stlouisfed.org/docs/api/api_key.html'
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
        self.retries = 5 # number of query retries
        self.seriesdict = {}
        self.observationsdict = {}
        self.categorydict = {}
        self.releasedict = {}
        self.sourcedict = {}
        self.tagdict = {}
        self.updatedict = {}

        self.uq = common._URLQuery()

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
        url = '%s?series_id=%s&api_key=%s' % (self.ssurl, sid,
                                              self.api_key)
        resp = self.uq.query(url)
        rstr = resp.read().decode('utf-8')
        self.getseriesdata(rstr)

    def reportdata(self, dict, ofp):
        """ reportdata(ofp)

        report data for a collection
        rstr - decoded response of a urllib request
        """
        if dict == None:
            print('nothing to report', file=sys.sterr)
            return
        ha = []
        ka = dict.keys()
        for id in ka:
            ra = []
            if len(ha) == 0:
                for k in dict[id].keys():
                    ha.append("'%s'," % k)
                print(''.join(ha), file=ofp)
            ra=[]
            for rk in dict[id].keys():
                ra.append("'%s'," % dict[id][rk])
            print(''.join(ra), file=ofp)

    def getfreddata(self, rstr, dict):
        """ getfreddata(rstr, dict)

        get data for the data of a series_id query
        rstr - decoded response of a urllib request
        dict - dictionary in which to store the data
        """
        xroot = ET.fromstring(rstr)
        for child in xroot:
            adict = child.attrib
            ka = adict.keys()
            key = None
            if 'id' in ka:
                key = adict['id']
                dict[key] ={}
            elif 'name' in ka:
                key = adict['name']
                dict[key] ={}
            for k in ka:
                dict[key][k] = adict[k]


    def reportcategories(self, ofp):
        self.reportdata(self.categorydict, ofp)

    def getcategoriesforsid(self, sid):
        """ getseriesforsid(sid)

        get a series for a series_id
        sid - series_id
        """
        url = '%s?series_id=%s&api_key=%s' % (self.scurl, sid,
                                              self.api_key)
        resp = self.uq.query(url)
        rstr = resp.read().decode('utf-8')
        self.getfreddata(rstr, self.categorydict)

    def reportreleases(self, ofp):
        self.reportdata(self.releasedict, ofp)

    def getreleasesforsid(self, sid):
        """ getreleasesforsid(sid)

        get releasєs for a series_id
        sid - series_id
        """
        url = '%s?series_id=%s&api_key=%s' % (self.srurl, sid,
                                              self.api_key)
        resp = self.uq.query(url)
        rstr = resp.read().decode('utf-8')
        self.getfreddata(rstr, self.releasedict)

    def reportsources(self, ofp):
        self.reportdata(self.sourcedict, ofp)

    def getsourcesforsid(self, sid):
        """ getsourcesforsid(sid)

        get sources for a series_id
        sid - series_id
        """
        url = '%s?series_id=%s&api_key=%s' % (self.ssurl, sid,
                                              self.api_key)
        resp = self.uq.query(url)
        rstr = resp.read().decode('utf-8')
        self.getfreddata(rstr, self.sourcedict)

    def reporttags(self, ofp):
        self.reportdata(self.tagdict, ofp)

    def gettagsforsid(self, sid):
        """ gettagsforsid(sid)

        get tags for a series_id
        sid - series_id
        """
        url = '%s?series_id=%s&api_key=%s' % (self.sturl, sid,
                                              self.api_key)
        resp = self.uq.query(url)
        rstr = resp.read().decode('utf-8')
        self.getfreddata(rstr, self.tagdict)

    def reportupdates(self, ofp):
        self.reportdata(self.updatedict, ofp)

    def getupdatesforsid(self, sid):
        """ getseriesforsid(sid)

        get updates for a series_id
        sid - series_id
        """
        url = '%s?series_id=%s&api_key=%s' % (self.suurl, sid,
                                              self.api_key)
        resp = self.uq.query(url)
        rstr = resp.read().decode('utf-8')
        self.getfreddata(rstr, self.updatedict)


def main():
    argp = argparse.ArgumentParser(description='collect and report stlouisfed.org FRED series')

    argp.add_argument('--series', action='store_true', default=False,
                       help="report series urls for categories collected")
    argp.add_argument('--observations', action='store_true', default=False,
                       help="report timeseries data for categories")

    argp.add_argument('--categories', action='store_true', default=False,
                       help="report categories for this series")
    argp.add_argument('--releases', action='store_true', default=False,
                       help="report categories for this series")
    argp.add_argument('--sources', action='store_true', default=False,
                       help="report sources for this series")
    argp.add_argument('--tags', action='store_true', default=False,
                       help="report tags for this series")
    argp.add_argument('--updates', action='store_true', default=False,
                       help="report updates for this series")

    argp.add_argument('--seriesid', required=True,
        help="series are identified by series_id")

    argp.add_argument('--file', help="path to an output filename\n\
            if just a filename and--directory is not provided\
            the file is created in the current directory")
    argp.add_argument('--directory',
                    help="directory to write the output use --directory for\n\
                         storing observations, filenames autogenerated")

    args = argp.parse_args()

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

    fc = FREDseries()
    if args.observations:
        if not args.directory:
            argp.print_help()
            sys.exit()
        else:
            fc.getseriesforsid(sid=args.seriesid)
            fc.getandreportobservations(odir=args.directory)
    elif args.series and args.seriesid:
        fc.getseriesforsid(sid=args.seriesid)
        fc.reportseries(ofp=fp)
    elif args.categories:
        fc.getcategoriesforsid(sid=args.seriesid)
        fc.reportcategories(ofp=fp)
    elif args.releases:
        fc.getreleasesforsid(sid=args.seriesid)
        fc.reportreleases(ofp=fp)
    elif args.sources:
        fc.getsourcesforsid(sid=args.seriesid)
        fc.reportsources(ofp=fp)
    elif args.tags:
        fc.gettagsforsid(sid=args.seriesid)
        fc.reporttags(ofp=fp)
    elif args.updates:
        fc.getupdatesforsid(sid=args.seriesid)
        fc.reportupdates(ofp=fp)

if __name__ == '__main__':
    main()
