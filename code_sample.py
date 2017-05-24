
""" Please fill in the body of the functions in this script.
"""

#
# Feel free to ask questions about any of this: matt@giantotter.com
#
# You will be querying data from a MySQL database on AWS, with these credentials:
#      Host:  demo.cdpfkoxivmj6.us-east-1.rds.amazonaws.com
#      User:  giantotter
#  Password:  demopassword
#  Database:  caidb
#
# The database contains two tables, with the following structure.
#
# Table name:  logs
# +-------+-------------+------+-----+---------+----------------+
# | Field | Type        | Null | Key | Default | Extra          |
# +-------+-------------+------+-----+---------+----------------+
# | id    | int(11)     | NO   | PRI | NULL    | auto_increment |  <-- unique ID for each log.
# | name  | varchar(64) | YES  |     | NULL    |                |  <-- log filename.
# +-------+-------------+------+-----+---------+----------------+
#
# Table name:  log_data
# +--------+---------------+------+-----+---------+----------------+
# | Field  | Type          | Null | Key | Default | Extra          |
# +--------+---------------+------+-----+---------+----------------+
# | id     | int(11)       | NO   | PRI | NULL    | auto_increment |  <-- unique ID for each row of data in a log.
# | log_id | int(11)       | YES  | MUL | NULL    |                |  <-- refers to id in the logs table.
# | line   | int(11)       | YES  |     | NULL    |                |  <-- line number in a log, starting at 1.
# | time   | int(11)       | YES  |     | NULL    |                |  <-- timestamp for a log row.
# | data   | varchar(1024) | YES  |     | NULL    |                |  <-- json encoded data for log row.
# +--------+---------------+------+-----+---------+----------------+
#
# This datbase contains data from 10 logfiles recorded from The Restaurant Game.  Each log has many rows of log_data.
# Your programming task will require you to extract information from utterances stored in log_data rows.
#
# Data for each row of log_data is encoded in a json 'LogData' data structure.
# Inside of a LogData json object, there is an 'obs' data structure (of type 'Observation').
# Each obs data structure has a 'type' member, which is set to either: 'physical', 'spatial', or 'speech'.
# The Observations of type 'speech' have a member named 'utterance'.   <--- these are the focus of this exercise!
#

import json
import MySQLdb
import re
import editdistance

cnx= {
  'host': 'demo.cdpfkoxivmj6.us-east-1.rds.amazonaws.com',
  'username': 'giantotter',
  'password': 'demopassword',
  'db': 'caidb'}

# ------------------------------------------------------------------------------

def report_utterance_word_counts(filepath):
    """
    Write text file that reports word counts for utterances in the demo database.
    :param filepath: output file path.
    """
    # establish database connection
    db = MySQLdb.connect(cnx['host'],cnx['username'],cnx['password'], cnx['db'])
    cur = db.cursor()

    # SQL query to select all rows except the first
    sql = 'SELECT * FROM log_data LIMIT 1, 18446744073709551615'
    cur.execute(sql)

    # We initialize a dictionary to keep track of unique words. We iterate over each row of the table "log_data". If the row's type
    # is "speech", we proceed to split the utterance sentence into separate words in a list. We iterate over each word in the
    # sentence, if it already exists in our dictionary, we add 1 to the value at that keyword; if it does not yet exist, then
    # we initialize the keyword to 1.

    dictionary = {}
    regex = re.compile('[^a-zA-Z]')

    for row in cur.fetchall() :
        obj = json.loads(row[4])
        if obj["obs"]["type"] == "speech":
            words = obj["obs"]["utterance"].split()
            for word in words:
                cleansed = regex.sub('', word)
                if len(cleansed)>0 and len(cleansed)<20:
                    if cleansed in dictionary:
                        dictionary[cleansed] += 1
                    else:
                        dictionary[cleansed] = 1

    # Close connection to database
    db.close()

    # We write to a file with the filepath argument as its name.

    with open(filepath, 'w') as f:
        for key in dictionary:
            f.write(key + ": " + str(dictionary[key]) + "\n")

    # Write the dictionary as JSON to another file for frontend task

    with open('./frontend/data.json', 'w') as outfile:
        json.dump(dictionary, outfile)


    # Fetch all of the log data from the database.
    # Ignore log_data rows that are not of type 'speech'.
    # Compute a total count (across all logs) for each unique word found in the data.
    # Write the count for each word to a text file.

    print "Your code goes here!"


# ------------------------------------------------------------------------------

def find_most_similar_utterance(utterance_to_match):
    """
    Write text file that reports word counts for utterances in the demo database.
    :param utterance_to_match: arbitrary string of words
    :returns most similar utterance from the database
    """

    db = MySQLdb.connect(cnx['host'],cnx['username'],cnx['password'], cnx['db'])
    cur = db.cursor()

    sql = 'SELECT * FROM log_data LIMIT 1, 18446744073709551615'
    cur.execute(sql)

    # I will use Levenshtein Distance as an approximation of the similarity between two utterances. Levenshtein Distance between
    # two strings is the minimal number of characters required to change one to the other. So the idea is that as I iterate over
    # each row in the table, I get the distance between the current utterance and the argument utterance. I continually keep track
    # of the smallest distance and the corresponding utterance as I iterate through the table.

    smallestDiff = 18446744073709551615
    bestMatch = None

    for row in cur.fetchall() :
        obj = json.loads(row[4])
        if obj["obs"]["type"] == "speech":
            sentence = obj["obs"]["utterance"]
            diff = editdistance.eval(utterance_to_match, sentence)
            if diff < smallestDiff:
                smallestDiff = diff
                bestMatch = sentence

    db.close()

    return bestMatch

    # Fetch all of the log data from the database.
    # Ignore log_data rows that are not of type 'speech'.
    # Find and return the utterance that is the closest match to the input.
    # Matching should be case-insensitive.

    return "Your code goes here!"


# ------------------------------------------------------------------------------

if __name__ == '__main__':

    # Write file with counts of words in utterances.
    report_utterance_word_counts('output.txt')

    # Find the most similar utterance in the database to these inputs.
    print find_most_similar_utterance("Please sit wherever you like")
    print find_most_similar_utterance("Can I get Salad and a Beer please")
    print find_most_similar_utterance("Do you want anything else?")
    print find_most_similar_utterance("I'm ready to pay. I'm finished")

# ------------------------------------------------------------------------------
