
import os
import sys
import webbrowser


class Dict2HTML():
    def __init__(self):
        self.htmla = []

    def dict2html(self, fdict, name):
       """ show(fdict)

       create an html file of the dictionary that is assumed to
       consist of only key:value pairs. The key:value pairs are
       loaded into an html table return the resulting html file
       fdict - python dictionary with only key:value pairs
       name - name of the dictionary
       """
       self.htmla.append('<html>')
       if name:
           self.htmla.append('<h1 style="text-align:center">%s</h1>' % (name) )
       self.htmla.append('<table border="1">')
       hdr = []
       # row keys
       rka = []
       keys = []
       for k in fdict.keys():
           # table header
           row = fdict[k]
           if len(keys) == 0:
               keys = [k for k in sorted(row.keys() )]
           if len(hdr) == 0:
              hdr = keys
              hf = '</th><th>'.join(hdr)
              self.htmla.append('<tr><th>%s</th></tr>' % (hf) )
           # rows
           for i in range(len(keys) ):
               if keys[i] not in row:
                   row[keys[i]] = ''
               if row[keys[i]].startswith('http') and \
                   'FRED_API_KEY' not in row[keys[i]]:
                  ref = '<a href="%s">%s</a>' % (row[keys[i]],'link' )
                  row[keys[i]] = ref
           rowa = [row[k] for k in keys]
           rf = '</td><td>'.join(rowa)
           self.htmla.append('<tr><td>%s</td></tr>' % (rf) )
       self.htmla.append('</table>')
       self.htmla.append('</html>')
       return ''.join(self.htmla)

    def dictshow(self, fdict, name):
       """ dictshow(fdict, name)

       generate html from dictionary with dict2html() and save it
       to a file named name.html
       fdict - python dictionary with only key:value pairs
       name - name of the dictionary
       """
       html = self.dict2html(fdict, name)
       fn = name
       if len(name.split()) != 1:
           fn = ''.join(name.split() )
       fpath = '%s.html' % os.path.join('/tmp', fn)
       with open(fpath, 'w') as fp:
           fp.write(html)
       webbrowser.open('file://%s' % (fpath) )

