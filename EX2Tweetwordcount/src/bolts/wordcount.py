from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from redis import StrictRedis
from streamparse.bolt import Bolt

import psycopg2
import time

class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()
        self.redis = StrictRedis()

    def process(self, tup):
        word = tup.values[0]

        # Write codes to increment the word count in Postgres
        # Use psycopg to interact with Postgres
        # Database name: Tcount 
        # Table name: Tweetwordcount 
        
        # Connect to database
        conn = psycopg2.connect(database="tcount", user="postgres")
        cur = conn.cursor()
        
        # Increment the local count
        self.counts[word] += 1
        
        # Check if word is already in the table 
        # (to stop and restart stream process without overwriting current table or deleting it)
        sql = "SELECT * FROM Tweetwordcount WHERE word='%s';" %(word)
        cur.execute(sql)
        has_word = cur.fetchall()
        conn.commit()
        
        if len(has_word) == 0:
            # New word > INSERT INTO
            sql = "INSERT INTO Tweetwordcount (word,count) VALUES ('%s', %d);" %(unicode(word), self.counts[word])
        else:
            # Update word count > UPDATE
            sql = "UPDATE Tweetwordcount SET count=%d WHERE word='%s';" %(self.counts[word], unicode(word))

        cur.execute(sql)
        conn.commit()
        #self.emit([word, self.counts[word]])

        # Log the count - just to see the topology running
        self.log('%s: %d' % (word, self.counts[word]))