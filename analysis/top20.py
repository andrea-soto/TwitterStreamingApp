#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import os
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
    
def bar_plot(names, values):    
    
    n = np.arange(len(values))
    plt.figure(figsize=(14,7))
    plt.title('Top-20 Words by Count\n', size=18)
    plt.ylabel("Occurrences (count)", size=14)
    plt.bar(n, values, color='#89C6DA')
    plt.xticks(n+0.5, names, rotation=0, size=12)
    
    plt.savefig(os.getcwd()+'/plot.png', format='png')
    
def top20():
        
    # Connect to database
    conn = psycopg2.connect(database="tcount", user="postgres")
    cur = conn.cursor()
    
    # Get total word count
    sql = "SELECT count(count) FROM Tweetwordcount;"
    cur.execute(sql)
    total_count = cur.fetchall()
    conn.commit()
    
    # Get top-20
    sql = "SELECT * FROM Tweetwordcount ORDER BY count DESC LIMIT 20;"
    
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    conn.close()
    
    # Print results
    print 'Top-20'
    print "%s %8s  %s"%('ID','Word','Count')
    rank = 1
    words = []
    counts = []
    for w,c in result:
        print "%2d  %8s  %d"%(rank,w,c)
        words.append(w)
        counts.append(c)
        rank += 1

    bar_plot(words, counts)

# ===================================================================================
if __name__ == '__main__':
    '''
    Get top-20 words by count
       python top20.py
    '''    
    top20()