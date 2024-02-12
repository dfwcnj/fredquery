
#! env python

# return information on tags
#
# report tags, their releases, or their series
#

import argparse
import sys

from  fredquery import fredtags


def main():
    ft = fredtags.FREDtags()

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


    if args.observations:
        if not args.directory:
            argp.print_help() 
            sys.exit()
        if args.tagname:
            ft.getseriesfortnm(tnm=args.tagname)
            ft.getobservations()
            ft.reportobservations(odir=args.directory)
        else:
            ft.gettags()
            ft.getseries()
            ft.getobservations()
            ft.reportobservations(odir=args.directory)
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
