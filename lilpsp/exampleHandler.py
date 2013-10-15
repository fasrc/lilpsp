"""
exampleHandler.py -- example for how to generate dynamic non-html content

DESCRIPTION
	This defines a function that will generate an http response consisting of a png file.
	See the README for how to configure apache to use it.

REQUIREMENTS
	n/a

AUTHOR
	John Brunelle <john_brunelle@harvard.edu>
	Harvard FAS Research Computing
"""

import os
import core


#--- handlers

def dynamicPNG(req):
	"""serve a png image"""


	#--- BEGIN TEMPLATE CODE...
	
	try:
		from mod_python import apache, util, Session
		
		session = Session.Session(req)
		form = util.FieldStorage(req, keep_blank_values=1)
		
		req.add_common_vars()

		base_url_dir = os.path.dirname(req.subprocess_env['REQUEST_URI'].split('?',1)[0])  #e.g. /PATH, of 'https://SERVER/PATH?FOO=BAR'
		base_fs_dir  = os.path.dirname(req.subprocess_env['SCRIPT_FILENAME'])
		
		msg = "request from ip [%s] from user [%s]" % (req.subprocess_env['REMOTE_ADDR'], core.getUsername(session, req))
		core.log(msg, session, req)
		
		core.sessionCheck(session, req)

		#--- ...END TEMPLATE CODE



		#these are of bytes of a little plus sign png (in practice it could of course be a truly dynamically created image)
		bytes = '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x0f\x00\x00\x00\x0f\x08\x06\x00\x00\x00;\xd6\x95J\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x06bKGD\x00\xff\x00\xff\x00\xff\xa0\xbd\xa7\x93\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xdb\x03\x0e\x03\x19 \xb1z|&\x00\x00\x00\x19tEXtComment\x00Created with GIMPW\x81\x0e\x17\x00\x00\x01\\IDAT(\xcf\x95\x92=K\x03A\x10\x86\x9f\x9d\xbb\x13\xd1B\x02I\x11\xf0JI\x1f\x1b\xff\x83\xd8\xe4\x07\xd8\xa4\xb1\x11\x1b\x0b\x11\xc4N,D\xf0\xabK\x94(\xd6j\x17\xc4?\x10\xd0\xa4\x14b:\x95\x84\x88\x12lB>n\xc7"\xe4 \xf1\x848\xcd\xb2\xb3\xf3,\xef\xbc3FU\x95\x888\xbb;\xa5R+\x93\x8c%\xd9Y\xdde\xca\x9d\xfaU\xe3F\x81\x97\xf7\x05.\x8ay\xfaA\x1f\x80v\xb7\xcd\xc1\xda\xe1dp\xe3\xab\x8e#\x0e\x00\xd6Z\x9a\xadfT\x19\x12\x99\x94\xd1\xb4#29\xec\xb9\xde\xd8gN$lTU/\xef\x0b4\xbe\xea\x88\x08\x9e\xebQz.\xf1\xf2^EUQU\xe2sq\x96\x97V\xe8\xf6:(\xe0\x8a\xc3zf\x03sz{\xa2\x17\xc5|\xd8#\x80U\xcbp\x08\xaa\x8a1\xe6\xd7{za\x11\xb7R+\x87\xaeFJ3\x06\x80\xc0\x06#\xf9\xa7\xea#n2\x96\x0c]\x1d\x07\x86\xe7P\xfe0\x14\xc5O\xf8\x98N\xaf\xa3\xdb\xb9-\x9a\xad&\x8e\x08"\x0eo\x1f\xaf|~\x7f\x86\xe0\xcc\xf4,\xa9\xf9\x14\x81\xed\xa3\xaa\x88\x08{\xd9\xfd\x81a\xe3R\x8fo\x8e\xb8~\xb8"\xb0\x01\xd6\x0e\xfa\xcbm\x9eO6\xaan\xaf3r\x0fl\x7f\xf29\x8fK\xf9c\xfd\xa3aW\x1c\xac\xda\xd0\x1c\xf9\xcf\x86\xadg6H/,\x02\xe0\'|\xf6\xb2\xfb\x91\xf0\x0f\xef\xf5\x9a\xd8\xfc\x04i\x03\x00\x00\x00\x00IEND\xaeB`\x82'
		req.headers_out.add('Content-Type', 'image/png')
		req.write(bytes)

		#almost all Exceptions should be allowed to just bubble up to the general catch-all
		#if instead you want specific explanations presented to the user, you must redirect



		#--- BEGIN TEMPLATE CODE...

		return apache.OK
	except apache.SERVER_RETURN:
		##if it's re-raised, sessions start over; passing seems wrong but it's the only way I know of to make sessions persist across redirect
		#raise
		raise
	except Exception, e:
		if not ( 'core' in globals() and 'session' in locals() and 'base_url_dir' in locals() ):
			raise  #just bailout and let the server handle it (if configured with PythonDebug On, the traceback will be shown to the user)
		else:
			msg = "ERROR: exception when handling user [%s]: %s" % (core.getUsername(session, req), e)
			core.log(msg, session, req, e)
			req.internal_redirect(os.path.join(base_url_dir, 'exampleHandlerFailure.psp'))
			return apache.OK  #(not sure if this does anything)
	
	#--- ...END TEMPLATE CODE
