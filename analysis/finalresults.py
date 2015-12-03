#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import time
import sys
   
def get_wordCount(word, show=25):
    # Get count for the input word or all word counts. 
    # The output is restricted to the 'show' value.
    
    # Connect to database
    conn = psycopg2.connect(database="tcount", user="postgres")
    cur = conn.cursor()
    
    # Get total words counted in tweets
    sql = "SELECT count(*) FROM Tweetwordcount ;" 
    cur.execute(sql)
    total_words = cur.fetchall()
    conn.commit()
    
    # Get count for word or all words (depending on input)
    if word == None:
        sql = "SELECT * FROM Tweetwordcount ORDER BY word ASC LIMIT %d;"%(min(show,total_words[0][0]))        
    else:
        sql = "SELECT * FROM Tweetwordcount WHERE word='%s';" %(word)
    
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    conn.close()
    
    # Print results
    if word == None:
        print 'First %d word-counts (out of %d words):\n'%(min(show,total_words[0][0]),total_words[0][0])
        print "%12s  %s"%('Word','Count')
        for w,c in result:
            print "%12s  %d"%(w,c)
    else:
        print "Number of occurences of '%s':  %d"%(result[0][0], result[0][1]), "\t@", time.ctime(time.time())

# ===================================================================================
if __name__ == '__main__':
    '''
    To get the number of occurances of single word:
       python finalresults.py hello
    
    Get all the word counts, sorted alphabetically, one per line:
       python finalresults.py
    
    The default is to show only the first 25 words. 
    To increase the number of words shown, send any number as an input:
       python finalresults.py 2000
    '''    
    
    numToShow = 25
    word = None
    # Get input word if any
    if len(sys.argv) > 1:
        # Get target word
        if sys.argv[1].isdigit():
            numToShow = int(sys.argv[1])
        else:
            word = sys.argv[1]
    
    get_wordCount(word, numToShow)