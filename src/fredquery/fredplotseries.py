#! env python

import os
import sys
import argparse
import webbrowser

import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go

try:
    from fredquery import fredseries
except ImportError as e:
    import fredseries

class FREDPlotSeries():
    def __init__(self):
        """ create a plot with a list of FRED series_id's
        """
        # settings

        self.fs = fredseries.FREDSeries()
        self.seriesdict={}
        self.observationsdict={}
        self.unitfreqseriesdict = {} # [units][freq][sid]
        self.html = None

        self.df = None
        self.fig = None

    def getobservation(self, sid):
        """ getobservation(sid)

        get time series observations data for a FRED serieѕ_id
        sid - FRED series_id
        """
        aa = self.fs.returnobservation(sid)
        self.observationsdict[sid] = aa

    def getobservationlist(self, slist):
        sa = slist.split(',')
        for sid in sa:
            self.getobservation(sid)

    def getseries(self, sid):
        """ getseries(sid)

        get descriptive data for a FRED series_id
        sid - FRED series_id
        """
        aa = self.fs.returnseriesforsid(sid)
        freq = aa[1][6]
        units = aa[1][8]

        if units not in self.unitfreqseriesdict.keys():
            self.unitfreqseriesdict[units]={}
        if freq not in self.unitfreqseriesdict[units]:
            self.unitfreqseriesdict[units][freq]={}
        self.unitfreqseriesdict[units][freq][sid] = aa

    def getserieslist(self, slist):
        """ getserieslist(slist)

        split comma separated slist into an array of series_id
        and get series data for each series
        """
        sa = slist.split(',')
        for sid in sa:
            self.getseries(sid)

    # https://plotly.com/python/multiple-axes/
    def composeunitfreqseriesplot(self, u, f, ptitle):
        """ composeunitfreqseriesplot(u, f)

        compose plotly figure for later display with the series_id as
        the legend
        u - units of the observations
        f - observationfrequency
        """
        #fig = go.Figure()
        fig  = make_subplots(shared_yaxes=True, shared_xaxes=True)

        issecond=False

        for sid in self.unitfreqseriesdict[u][f]:
            saa = self.unitfreqseriesdict[u][f][sid]
            sid    = saa[1][0]
            stitle = saa[1][3]
            freq   = saa[1][6]
            units  = saa[1][8]

            oaa = self.observationsdict[sid]

            dates = [oaa[i][2] for i in range(len(oaa) )]
            vals  = [oaa[i][3] for i in range(len(oaa) )]

            fig.add_trace( go.Scatter( x=dates, y=vals, name=sid) )
            #fig.add_trace( go.Scatter( x=dates, y=vals, name=sid),
            #                          secondary_x=issecond)
            issecond=True

        fig.update_layout(
            title=ptitle,
            yaxis_title=units,
            xaxis_title='dates',
        )
        return fig

    def composeunitfreqseriesplotwnotes(self, title):
        """ composeunitfreqseriesplotwnotes(title)

        compost plots with notes organized by units
        title - title for the web page
        """
        htmla = []
        htmla.append('<html>')
        if not title: title = 'FRED Series Plot'
        htmla.append('<head>')
        htmla.append('<title>%s</title>' % (title) )
        htmla.append('<script src="https://cdn.plot.ly/plotly-2.32.0.min.js" charset="utf-8"></script>')
        htmla.append('</head>')

        ua = [k for k in self.unitfreqseriesdict.keys()]
        for u in self.unitfreqseriesdict.keys():
            fa = [k for k in self.unitfreqseriesdict[u].keys()]
            for f in self.unitfreqseriesdict[u].keys():

                fig = self.composeunitfreqseriesplot(u, f, title)

                figjs = fig.to_json()
                htmla.append('<div id="fig%s%s">' % ( u, f) )
                htmla.append('<script>')
                htmla.append('var figobj = %s;\n' % figjs)
                htmla.append('Plotly.newPlot("fig%s%s", figobj.data, figobj.layout, {});' % (u,f) )
                htmla.append('</script>')
                htmla.append('</div>')

                for sid in self.unitfreqseriesdict[u][f].keys():
                    saa = self.unitfreqseriesdict[u][f][sid]
                    sid=saa[1][0]
                    stitle=saa[1][3]

                    htmla.append('<h3>%s:  %s</h3>' % (sid, stitle) )

                    # header
                    htmla.append('<table border="1">')
                    hrowa = [saa[0][i] for i in range(len(saa[0])-1) if i != 3]
                    hrow = '</th><th>'.join(hrowa)
                    htmla.append('<tr>%s</tr>' % (''.join(hrow)) )

                    # data
                    drowa = [saa[1][i] for i in range(len(saa[1])-1) if i != 3]
                    drow = '</td><td>'.join(drowa)
                    htmla.append('<tr>%s</tr>' % (''.join(drow)) )
                    htmla.append('</table>')

                    # notes
                    htmla.append('<p>')
                    htmla.append('%s: %s' % (saa[0][-1], saa[1][-1]) )
                    htmla.append('</p>')

        htmla.append('</html>')

        self.html = ''.join(htmla)
        return self.html

    def saveplothtml(self, fn):
        """ saveplothtml(fn)

        save the plot html
        fn - filename
        """
        with open(fn, 'w') as fp:
            fp.write(self.html)

    def showplothtml(self, fn):
        """ showplothtml(fn)

        show the html in your web browser
        fn - filename of the html file
        """
        webbrowser.open('file://%s' % (fn) )

    def showplotfig(self):
        self.fig.show()

def main():
    argp = argparse.ArgumentParser(description='plot a series list')
    argp.add_argument('--serieslist', required=True,
        help="comma separated list of FRED series_id's")
    argp.add_argument('--htmlfile', default='/tmp/p.html',
        help="path to file that will contain the plot")
    args = argp.parse_args()

    PS = PlotSeries()

    PS.getserieslist(args.serieslist)
    PS.getobservationlist(args.serieslist)

    PS.composeunitfreqseriesplotwnotes()

    PS.saveplothtml(args.htmlfile)
    PS.showplothtml(args.htmlfile)
    #PS.showplotfig()

if __name__ == '__main__':
    main()
