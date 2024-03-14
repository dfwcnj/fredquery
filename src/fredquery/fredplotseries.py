#! env python

import os
import sys
import argparse

import plotly.express as px
import pandas as pd
import numpy as np

try:
    from fredquery import fredseries
except ImportError as e:
    import fredseries

class PlotSeries():
    def __init__(self):
        # settings
        pd.options.plotting.backend = "plotly"

        self.fs = fredseries.FREDseries()
        self.seriesdict={}
        self.observationsdict={}
        self.data = {}

        self.df = None
        self.fig = None

    def getobservation(self, sid):
        aa = self.fs.returnobservation(sid)
        self.observationsdict[sid] = aa

    def getseries(self, sid):
        aa = self.fs.returnseriesforsid(sid)
        self.seriesdict[sid] = aa

    def composedata(self):
        for k in self.seriesdict.keys():
            saa = self.seriesdict[k]
            assert saa[0][0] == 'id'
            assert saa[0][3] == 'title'
            assert saa[0][8] == 'units'
            sid    = saa[1][0]
            stitle = saa[1][3]
            units  = saa[1][8]

            oaa = self.observationsdict[k]

            if 'dates' not in self.data.keys():
                self.data['dates'] = dates
            if 'values' not in self.data.keys():
                self.data['values'] =[[oaa[i][3] for i in range(len(oaa) )]]
            else:
                self.data['values'].append( [oaa[i][3] for i in
                              range(len(oaa) )] )

            #dates = [oaa[i][2] for i in range(1, len(oaa) )]
            #vals = [oaa[i][3] for i in range(1, len(oaa) )]
            #if 'dates' not in self.data.keys():
                #self.data['dates'] = dates
            #self.data[sid] = vals

    def composeplot(self):
        self.df = pd.DataFrame(self.data)
        fig = None

        for k in self.seriesdict.keys():
            if not fig:
                fig = px.line(self.df, x=self.df['dates'], y=self.df[k])
            else:
                fig.add_scatter(x=self.df['dates'], y=self.df[k])

        fig.show()

def main():
    argp = argparse.ArgumentParser(description='plot a series list')
    argp.add_argument('--serieslist', required=True,
        help="comma separated list of FRED series_id's")
    args = argp.parse_args()

    PS = PlotSeries()

    sida = args.serieslist.split(',')
    for sid in sida:
        PS.getseries(sid)
        PS.getobservation(sid)
    PS.composedata()
    PS.composeplot()

if __name__ == '__main__':
    main()
