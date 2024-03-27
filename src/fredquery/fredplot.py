#! env python

import os
import sys
import argparse
import webbrowser

try:
    from fredquery import fredcategories
    from fredquery import fredreleases
    from fredquery import fredseries
    from fredquery import fredplotseries
    from fredquery import fredsources
    from fredquery import fredtags
except ImportError as e:
    import fredcategories
    import fredreleases
    import fredseries
    import fredplotseries
    import fredsources
    import fredtags

class FREDPlot():

    def __init__(self):
        """ create a plot with a FRED list of some type
        """
        pass


    def plotseries(self, aa, directory):
        """ plotseries(aa, directory)

        generate an html page with plots and notes abơut the plots
        and show them on your browser
        aa - array of arrays containing series information
        directory - where to store the html page
        """
        ida = [aa[i][0] for i in range(1, len(aa))]
        idc = ','.join(ida)
        fp = fredplotseries.FREDPlotSeries()
        fp.getserieslist(idc)
        fp.getobservationlist(idc)
        fp.composeunitseriesplotwnotes()
        hfn = os.path.join(directory, 'plot.html')
        fp.saveplothtml(hfn)
        fp.showplothtml(hfn)

    def plotcategoryid(self, catid, directory):
        """ plotcategoryid(catid, directory)

        plot series for category_id catid, storing the html page
        in directory
        catid - category_id
        directory - where to store the html page
        """
        fc = fredcategories.FREDCategories()
        fc.getseriesforcid(catid)
        aa = fc.returnseriesforcid(catid)
        self.plotseries(aa, directory)

    def plotreleaseid(self, rid, directory):
        """ plotreleaseid(rid, directory)

        plot series for release_id rid, storing the html page
        in directory
        rid - release_id
        directory - where to store the html page
        """
        fr = fredreleases.FREDReleases()
        fr.getseriesforrid(rid)
        aa = fr.returnseriesforrid(catid)
        self.plotseries(aa, directory)

    def plotsourceid(self, sid, directory):
        """ plotsourceid(sid, directory)

        plot series for source_id sid, storing the html page
        in directory
        sid - source_id
        directory - where to store the html page
        """
        fs = fredsources.FREDSources()
        fs.getseriesforcid(sid)
        aa = fs.returnseriesforsid(sid)
        self.plotseries(aa, directory)

    def plottagname(self, tnm, directory):
        """ plottagname(tnm, directory)

        plot series for tag name tnm, storing the html page
        in directory
        tnm - tagname
        directory - where to store the html page
        """
        ft = fredtags.FREDTags()
        ft.getseriesfortnm(tnm)
        aa = self.fc.returnseriesfortnm(tnm)
        self.plotseries(aa, directory)

def main():
    argp = argparse.ArgumentParser(description='plot a set of St. Louis Fed FRED series')
    argp.add_argument('--categoryid', help="FRED category_id")
    argp.add_argument('--releaseid', help="FRED release_id")
    argp.add_argument('--sourceid', help="FRED source_id")
    argp.add_argument('--tagname', help="FRED tagname")
    argp.add_argument('--directory', default='/tmp',
        help="where to store html")

    args = argp.parse_args()

    PS = FREDPlot()

    if args.categoryid:
        PS.plotcategoryid(args.categoryid, args.directory)
    elif args.releaseid:
        PS.plotreleaseid(args.releaseid, args.directory)
    elif args.sourceid:
        PS.plotsourceid(args.sourceid, args.directory)
    elif args.tagname:
        PS.plottagname(args.tagname, args.directory)
    else:
        argp.print_help()


if __name__ == '__main__':
    main()
