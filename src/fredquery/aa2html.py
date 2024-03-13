
import os
import sys
import webbrowser


class _AA2HTML():
    def __init__(self):
        self.htmla = []

    def aa2html(self, aa, name):
       """ aa2html(aa, name)

       return html of array of arrays
       aa - python array of arrays  with keys in array[0]
       name - name of the dictionary
       """
       self.htmla.append('<html>')

       if name:
           self.htmla.append('<title>%s</title>' % (name) )
           self.htmla.append('<h1 style="text-align:center">%s</h1>' % (name) )

       # table
       self.htmla.append('<table border="1">')
       # table header
       hdra = aa[0]
       hdr = '</th><th>'.join(hdra)
       self.htmla.append('<tr><th>%s</th></tr>' % (hdr) )
       # table rows
       for i in range(1, len(aa) ):
           rowa = aa[i]
           row = '</td><td>'.join(rowa)
           self.htmla.append('<tr><td>%s</td></tr>' % (row) )

       # close
       self.htmla.append('</table></html>')
       return ''.join(self.htmla)


    def aashow(self, aa, name):
       """ aashow(as, name)

       generate html from dictionary with dict2html() and save it
       to a file named name.html
       fdict - python dictionary with only key:value pairs
       name - name of the dictionary
       """
       html = self.aa2html(aa, name)
       fn = name
       if len(name.split()) != 1:
           fn = ''.join(name.split() )
       fpath = '%s.html' % os.path.join('/tmp', fn)
       with open(fpath, 'w') as fp:
           fp.write(html)
       webbrowser.open('file://%s' % (fpath) )

