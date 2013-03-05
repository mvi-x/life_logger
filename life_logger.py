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



def is_in_line(line, filter_by):
	if filter_by[0] and line.find(filter_by[0]) != -1:
		return True
	else:
		return False


def read_backwards(file, lines, *filter_by): # filter_by valid options now: tags, dates. Maybe in the future: since, up-to
	try: 
		br = BackwardsReader(open(file))
		out = []
		if lines == 'all':
			all_lines = []
			while 1:
			    line = br.readline()
			    if not line:
			        break
			    all_lines.append(line)
			if filter_by:
				for line in all_lines:
					if is_in_line(line, filter_by):
						out.append(line)
			else:
				out = all_lines

		else:
			i = 0
			if filter_by:			
				while i < lines:
					line = br.readline()
					if not line:
						break
					if is_in_line(line, filter_by):
						out.append(line)
						i += 1
			else:
				while i < lines:
					line = br.readline()
					if not line:
						break
					out.append(line)
					i += 1

		return out
	except IOError:
		return False;

def extract_action(r):
	action_start = r.find('"')
	action_end = r.find('"',action_start+1)
	action = r[action_start+1:action_end]
	return action

def extract_tags(r):
	tags_s_start = r.find('Tags: ')
	tags_s_last = r.rfind('@')
	if tags_s_last == -1:
		tags = '';
	else: 		
		tags_s_end = r.find(' ', tags_s_last)
		tags_s = r[tags_s_start+6:tags_s_end]
		tags = tags_s.split(', ')
	return tags

def extract_started(r):
	started_start = r.find('Started: ')
	started_end = r.find('|',started_start)
	started = datetime.datetime.strptime(r[started_start+9:started_end-2], '%Y-%m-%d %H:%M')
	return started

def extract_finished(r):
	finished_start = r.find('Finished: ')
	finished_end = r.find('|',finished_start)
	finished = datetime.datetime.strptime(r[finished_start+10:finished_end-1], '%Y-%m-%d %H:%M')
	return finished

def extract_prev_finished():
	new_start = None
	prev_entry = str(read_backwards('my_life.txt', 1))
	if prev_entry:
		new_start = extract_finished(prev_entry)
	return new_start

def entry_constructor(log):
	elapsed = log.end - log.start
	tags = ', '.join(log.tags)
	entry = '"' + log.action + '" | Started: ' + str(log.start)[:16] + ' | Finished: ' + str(log.end)[:16] + ' | Elapsed: ' + str(elapsed)[:4] + ' | Tags: ' + tags + ' |\n'
	return entry, elapsed


def append_to(file, entry): # Opens and appends an entry into a file
	try:
	    logfile = open(file, "a") # Opens the file in appending mode or creates it if unexisting
	    try:
	        logfile.write(entry)
	    finally:
	        logfile.close()
	except IOError:
	    pass

def log_writer(log_list): # a list of only one log is being passed
	assert len(log_list) == 1
	append_to('my_life.txt',str(entry_constructor(log_list[0])))

def log_displayer(log_list):
	total_elapsed = datetime.timedelta(hours = 0)
	for log in log_list:
		entry, elapsed = entry_constructor(log)
		total_elapsed += elapsed
		print entry
	print '-----------------\nTotal: '+str(int(total_elapsed.total_seconds()//3600))+'h '+str(int(total_elapsed.total_seconds()%3600//60))+'min.\n-----------------'




def log_maker(user_input): # Processes user input and extracts a log or returns an error.
	error = None
	log = None
	tags = []
	new_start = None

	if len(user_input) == 1:
		error = 'At the very least you need to enter one action. Please use the following syntax: \'python life_logger.py "Text to log" start:-5h ;; start:is an optional parameter\''
		
	elif len(user_input) == 2: #life_logger.py  + "Text"
		new_start = extract_prev_finished()
	
	else: #life_logger.py  + "Text" + any or all of the optional parameters
		assert len(user_input) >= 3
		new_start = extract_prev_finished()
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


def is_there_filter(user_input):
	filter_by = None;
	error = None;
	if len(user_input) > 3:
		error = "Please, revise your syntax. Only one additional parameter can be provided after "+user_input[2]
	elif len(user_input) == 3:
		filter_by = user_input[2]
	return filter_by, error


def log_reconstructor(user_input):
	if user_input[1] == '--view-all':
		lines = 'all'
		filter_by, error = is_there_filter(user_input)
	elif user_input[1][:7] == '--last-':
		lines = int(user_input[1][7:])
		filter_by, error = is_there_filter(user_input)

	else:
		error = "Please, revise your syntax. Use the --help option for some examples."

	if error:
		print error
	elif filter_by:
		results = read_backwards('my_life.txt', lines, filter_by)
	else:
		results = read_backwards('my_life.txt', lines)
	
	log_list = []
	for r in results:
		log = LogEntry(extract_action(r), extract_tags(r), extract_started(r), extract_finished(r))
		log_list.append(log)
		
	return log_list


def decision_maker(user_input): # Processes user input and determines whether s/he is entering a new log, asking for help, or asking to view the history
	if user_input[1][:2] == '--': # User is not trying to log a new item, s/he is asking something

		if user_input[1] == '--help': # if user inputs 'life_logger.py --help', print the help file
			print '<Pending>'
		else:
			log_displayer(log_reconstructor(user_input))

	else:
		maker_result = log_maker(user_input)
		if maker_result[1] != None: #if there was an error when running log_maker
			print maker_result[1] #print the error
		else: # if no error was found when running log_maker
			assert maker_result[0] != None
			log_list = []
			log_list.append(maker_result[0])
			log_displayer(log_list)
			log_writer(log_list)

decision_maker(sys.argv)



