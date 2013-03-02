#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: mvime -> mvime@mvi.me
# License: Haven't figured that out yet.
# file: life_logger.py
# BackwardsReader implementation: Copyright (c) Peter Astrand <astrand@cendio.se>, PSF License

import sys, datetime, os, string
#Syntax: python life_logger.py "Text to log" @tag start:-5h ;; start: and @tag are optional parameters

# We set the timestamp
timestamp = datetime.datetime.now()

#default start_time (to be used when first action ever // later on when end_time over one day since last end_time)
default_start = timestamp - datetime.timedelta(hours = 1)

# We define the LogEntry class, which needs an action, an end_time (timestamp) and a start_time (set by user or default_start)
class LogEntry:
	def __init__(self, action, tags, start_time = default_start, end_time = timestamp):
		self.action = action
		self.tags = tags
		self.end = end_time
		self.start = start_time

class BackwardsReader: 
    """Read a file line by line, backwards"""
    BLKSIZE = 4096

    def readline(self):
        while 1:
            newline_pos = string.rfind(self.buf, "\n")
            pos = self.file.tell()
            if newline_pos != -1:
                # Found a newline
                line = self.buf[newline_pos+1:]
                self.buf = self.buf[:newline_pos]
                if pos != 0 or newline_pos != 0 or self.trailing_newline:
                    line += "\n"
                return line
            else:
                if pos == 0:
                    # Start-of-file
                    return ""
                else:
                    # Need to fill buffer
                    toread = min(self.BLKSIZE, pos)
                    self.file.seek(-toread, 1)
                    self.buf = self.file.read(toread) + self.buf
                    self.file.seek(-toread, 1)
                    if pos - toread == 0:
                        self.buf = "\n" + self.buf

    def __init__(self, file):
        self.file = file
        self.buf = ""
        self.file.seek(-1, 2)
        self.trailing_newline = 0
        lastchar = self.file.read(1)
        if lastchar == "\n":
            self.trailing_newline = 1
            self.file.seek(-1, 2)


def append_to(file, entry): # Opens and appends an entry into a file
	try:
	    logfile = open(file, "a") # Opens the file in appending mode or creates it if unexisting
	    try:
	        logfile.write(entry)
	    finally:
	        logfile.close()
	except IOError:
	    pass

def read_backwards(file, lines, *args): # args[0]:since, args[1]:up-to
	try: 
		br = BackwardsReader(open(file))
		out = []
		if lines == 'all':
			while 1:
			    line = br.readline()
			    if not line:
			        break
			    out.append(line)
		else:
			i = 0
			while i < lines:
				line = br.readline()
				if not line:
					break
				out.append(line)
				i = i+1
		return out
	except IOError:
		return False;


def log_displayer(results):
	for r in results:
		print r[:-1] # The last two characters are stripped because they are "\n" and force a new line



def log_maker(user_input): # Processes user input and extracts a log or returns an error.
	error = None
	log = None
	tags = []
	new_start = None

	if len(user_input) == 1:
		error = 'At the very least you need to enter one action. Please use the following syntax: \'python life_logger.py "Text to log" start:-5h ;; start:is an optional parameter\''
		
	elif len(user_input) == 2: #life_logger.py  + "Text"
		prev_entry = str(read_backwards('my_life.txt', 1))
		if prev_entry:
			start_finished = prev_entry.find('Finished: ')
			end_finished = prev_entry.find(' |', start_finished)
			new_start = datetime.datetime.strptime(prev_entry[start_finished+10:end_finished], '%Y-%m-%d %H:%M')
	
	else: #life_logger.py  + "Text" + any or all of the optional parameters
		assert len(user_input) >= 3
		for i in user_input[2:]:
			if '@' in i:
				tags.append(i)
			if 'start:' in i:
				time_amount = float(i[7:-1]) #syntax is "start:-XXu", "start:-" is 7 chars long, so the amount starts at the 8th
				#stime_unit = i[-1:] #units are set with only one character: s, h, d, y
				new_start = timestamp - datetime.timedelta(hours = time_amount)			
		
	if new_start:
		log = LogEntry(user_input[1], tags, new_start)
	else:
		log = LogEntry(user_input[1], tags)

	
	return log, error


def decision_maker(user_input): # Processes user input and determines whether s/he is entering a new log, asking for help, or asking to view the history
	if user_input[1] == '--help': # if user inputs 'life_logger.py --help', print the help file
		print '<Pending>'
	elif user_input[1] == '--view-all':
		log_displayer(read_backwards('my_life.txt', 'all'))
	# elif user_input[1] == '--view-today':
	# 	read_backwards('my_life.txt', 'all', datetime.today())
	elif user_input[1][:7] == '--last-':
		lines = int(user_input[1][7:])
		log_displayer(read_backwards('my_life.txt', lines))

	else:
		maker_result = log_maker(user_input)
		if maker_result[1] != None:
			print maker_result[1] #print the error
		else:
			assert maker_result[0] != None
			log = maker_result[0]
			elapsed = log.end - log.start
			tags = ', '.join(log.tags)
			entry = '"' + log.action + '" | Started: ' + str(log.start)[:16] + ' | Finished: ' + str(log.end)[:16] + ' | Elapsed: ' + str(elapsed)[:4] + ' | Tags: ' + tags + ' |\n'
			append_to('my_life.txt', entry)
			print entry


decision_maker(sys.argv)



