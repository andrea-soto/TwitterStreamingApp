#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import time
import sys
   
def histogram(min_frq, max_frq, show):
        
    # Connect to database
    conn = psycopg2.connect(database="tcount", user="postgres")
    cur = conn.cursor()
    
    # Get total words with count within interval
    sql = "SELECT count(*) FROM Tweetwordcount WHERE count >= %d and count <= %d;"%(min_frq, max_frq)
    cur.execute(sql)
    total_words = cur.fetchall()
    conn.commit()
    
    # Get words with count within interval
    sql = "SELECT * FROM Tweetwordcount WHERE "
    sql += "count >= %d and count <= %d ORDER BY count ASC LIMIT %d;"%(min_frq, max_frq, show)
    
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    conn.close()
    
    # Print results
    print 'Reporting %d words (out of %d words):\n'%(min(show,total_words[0][0]),total_words[0][0])
    print "%12s  %s"%('Word','Count')
    for w,c in result:
        print "%12s  %d"%(w,c)

# ===================================================================================
if __name__ == '__main__':
    '''
    Get all the words with count between MIN and MAX value provided:
       python histogram.py 100 400
    
    The default is to show only the first 25 words. 
    To increase the number of words shown, send the number to show as a 3rd parameter:
       python histogram.py 100 400 50
    '''    
    
    numToShow = 25
    if len(sys.argv) < 3:
        print "Few inputs - MIN and MAX values for count interval are requiered"
    else:
        minVal = int(sys.argv[1])
        maxVal = int(sys.argv[2])
        if len(sys.argv) == 4:
            numToShow = int(sys.argv[3])
        if minVal > maxVal:
            print "min value provided is greater than max value. Values will be switched."
    
    histogram(minVal, maxVal, numToShow)