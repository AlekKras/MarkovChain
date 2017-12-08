'''
Implementation:
1) Use it to work with websites
2) Catches all errors, in case you found a program crashed, pull requests @github/alekkras
Work to improve:
1) Forbidden websites - error 403
2) Some of the context hasn't changed as we implement the algorithm only inbetween <p>...</p> tags
3) Once we read the data from the website, we don't completely copy the website as there are internal
files (css, js and php) which we can't download. It's possible to download CSS and JS, but we can't
download PHP files as it's almost never displayed within html code
'''

import urllib.request
import re
import urllib
import random
from Markov import Markov

def makeWordModel(filename):
    '''creates a Morkov model from the words in the file with filename.
    pre: The file with name filename exists.
    post: A Markov chain from the text in the file is returned. '''
    # creates a Markov model from words in filename
    infile = open(filename)
    tmpmodel = Markov()
    for line in infile:
        words = line.split()
        for w in words:
            tmpmodel.add(w)
    infile.close()
    # Add a sentinel at the end of the text
    tmpmodel.add(None)
    tmpmodel.reset()
    return tmpmodel

def generateWordChain(markov, n):
    ''' generates up to n words on output from the model "markov"
    pre: markov is a valid Markov chain where the length is longer than "n"
    post: a string of n words will be returned using the Markov chain.'''
    # generates up to n words of output from a model
    words = []
    for i in range(n):
        next = markov.randomNext()
        if next is None:
            break  # got to a final state
        words.append(next)
    return " ".join(words)


def calc():
    try:
        url = input("What is the website?\n")
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        respData = resp.read()
        paragraphs = re.findall(r'<p>(.*?)</p>',str(respData))
        html_file = open("website.html", "w")
        txt = []
        html_start = '''

<!doctype html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, height=device-height, user-scalable=no, initial-scale=1.0"/>
        <title>Even Better Motherfucking Website</title>
        <meta name="description" content="It's even more fucking perfect than the others motherfucking websites."/>
        <link rel="canonical" href="http://evenbettermotherfucking.website"/>
        <style>
            body {margin: 5% auto; background: #f2f2f2; color: #444444; font-family: -apple-system, BlinkMacSystemFont, “Segoe UI”, Roboto, Helvetica, Arial, sans-serif; font-size: 16px; line-height: 1.8; text-shadow: 0 1px 0 #ffffff; max-width: 73%;}
            code {background: white;}
            a {border-bottom: 1px solid #444444; color: #444444; text-decoration: none;}
            a:hover {border-bottom: 0;}
        </style>
    </head>
    <body>
        '''
        html_end = '''
        </body>
        </html>
        '''

        response = urllib.request.urlopen(url)
        webContent = response.read()

        f = open('website_test.html', 'w')
        f.write(str(webContent))

        for eachP in paragraphs:
            txt.append(eachP)
        print(txt)
        html_file.write(html_start)
        html_file.write(str(txt))
        html_file.write(html_end)
        f.write(str(webContent))
        html_file.close()

        try:
            fname = "website.html"
            m = makeWordModel(fname)
            print(generateWordChain(m, random.randrange(10, 1000, 10)))
        except: #debugging
            print("Something went wrong here")
        f.close()

    except Exception as e:
        print("There has happened a ", e)
calc()