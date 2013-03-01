#!/usr/bin/env python
# author: mvime -> mvime@mvi.me
# License: Haven't figured that out yet.
# file: life_logger.py

import sys, datetime
#Syntax: python life_logger.py "Text to log" start:-5h ;; start:is an optional parameter

# We set the timestamp
timestamp = datetime.datetime.now()

#default start_time (to be used when first action ever // later on when end_time over one day since last end_time)
default_start = timestamp - datetime.timedelta(hours = 1)

# We define the LogEntry class, which needs an action, an end_time (ts) and a start_time (set by user or default_start)
class LogEntry:
	def __init__(self, action, start_time = default_start, end_time = timestamp):
		self.action = action
		self.end = end_time
		self.start = start_time


def log_maker(user_input):
	error = None
	log = None

	if len(user_input) == 3:
		#user_input[2] is the optional argument where we set the start time
		time_amount = float(user_input[2][7:-1]) #syntax is "start:-XXu", "start:-" is 7 chars long, so the amount starts at the 8th
		#stime_unit = user_input[2][-1:] #units are set with only one character: s, h, d, y
		start_time = timestamp - datetime.timedelta(hours = time_amount)
		log = LogEntry(user_input[1],start_time)

	elif len(user_input) == 2:
		log = LogEntry(user_input[1])
	elif len(user_input) == 1:
		error = 'At the very least you need to enter an action. Please use the following syntax: \'python life_logger.py "Text to log" start:-5h ;; start:is an optional parameter\''
	else:
		error = 'Too many parameters'
	return log, error



def decision_maker(user_input):
	if user_input[1][:1] == '--help': # if user inputs 'life_logger.py --help', print the help file
		print '<Pending>'
	else:
		maker_result = log_maker(sys.argv)
		if maker_result[1] != None:
			print maker_result[1] #print the error
		else:
			assert maker_result[0] != None
			log = maker_result[0]
			print log.action, log.end, log.start


decision_maker(sys.argv)


