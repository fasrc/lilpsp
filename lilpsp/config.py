"""
basic configuration

DESCRIPTION
	Paremeters controlling how the site functions.
	
	This file is intended to be modified.  See comments below for details on 
	each option.  See the README for a higer-level overview.

REQUIREMENTS
	n/a

AUTHOR
	Copyright (c) 2011-2013
	Harvard FAS Research Computing
	John Brunelle <john_brunelle@harvard.edu>
	All right reserved.
"""

import os, re

#LOG_FILE -- the absolute path of the log file to use
#The apache user (or whatever user under which the web server is running) must 
#be able to write to it, or create if it does not exist (see also LOG_FILE_MODE 
#below).  This default is to take the name of the directory containing all the 
#psp, html, and the lilpsp python package, and use that as the base name of the 
#log file.  Note that any failures writing to this log are ignored.
LOG_FILE = '/var/tmp/%s.log' % os.path.basename(os.path.normpath(os.path.join(os.path.dirname(__file__),'..')))

#LOG_FILE_MODE -- the permissions of the log file, if this creates it
#This has no effect if the file already exists.
LOG_FILE_MODE = 0600

#DEBUG -- boolean for whether or not to include full details in Exceptions and log messages
#WARNING: True may cause tracebacks, shell command output, and other secrets to 
#be included in the Exceptions that are raised.  Only use True in production if 
#your log is secure and you're confident all calling code catches Exceptions.
DEBUG = True

#AUTH_TYPE -- what type of authentication to use
#choose one of:
#	'NONE' -- don't require anything
#	'HTTP' -- leave it to apache (i.e. rely on req.user)
#	'FORM' -- present a form to the user (login.psp) and authenticate creds using org.authenticateUser()
#If you choose 'FORM', you must implement org.authenticateUser().  Each psp 
#page must call sessionCheck() in order for this to be respected.  See the 
#README for full details.
AUTH_TYPE = 'NONE'

#RE_VALID_EMAIL_ADDRESS -- filter for allowable email addresses
#This is only applicable if you add code that calls core.sendEmail().  This 
#expression is lax by default, allowing just plain usernames (so that the 
#system emails the account); tighten if desired.  All email addresses are 
#properly quoted/escaped when passed to other programs, regardless of the 
#expression here.
RE_VALID_EMAIL_ADDRESS = re.compile('^[a-zA-Z0-9_\-.+%@]+$')
