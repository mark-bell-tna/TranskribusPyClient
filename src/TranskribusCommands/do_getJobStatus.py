#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
    Get the status of a job

    JL Meunier - Dev 2016


    Copyright Xerox(C) 2016 H. Déjean, JL. Meunier

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    
    Developed  for the EU project READ. The READ project has received funding 
    from the European Union’s Horizon 2020 research and innovation programme 
    under grant agreement No 674943.

"""
from __future__ import absolute_import
from __future__ import  print_function
from __future__ import unicode_literals
#    TranskribusCommands/do_deleteJob.py <JOBID>


#optional: useful if you want to choose the logging level to something else than logging.WARN
import sys, os, logging
from optparse import OptionParser

try: #to ease the use without proper Python installation
    import TranskribusPyClient_version
except ImportError:
    sys.path.append( os.path.dirname(os.path.dirname( os.path.abspath(sys.argv[0]) )) )
    import TranskribusPyClient_version

from TranskribusCommands import _Trnskrbs_default_url, __Trnskrbs_basic_options, _Trnskrbs_description, __Trnskrbs_do_login_stuff, _exit
from TranskribusPyClient.client import TranskribusClient
from TranskribusPyClient.common.trace import traceln, trace

import json
DEBUG = 0

description = """Get the status of a Transkribus job.
""" + _Trnskrbs_description

usage = """%s <jobId> 
"""%sys.argv[0]

class DoDeleteJob(TranskribusClient):
    
    sDefaultServerUrl = _Trnskrbs_default_url
    
    #--- INIT -------------------------------------------------------------------------------------------------------------    
    def __init__(self, trnkbsServerUrl, sHttpProxy=None, loggingLevel=logging.WARN):
        TranskribusClient.__init__(self, sServerUrl=self.sDefaultServerUrl, proxies=sHttpProxy, loggingLevel=loggingLevel)
        
        

if __name__ == '__main__':
    version = "v.01"

    #prepare for the parsing of the command line
    parser = OptionParser(usage=usage, version=version)
    parser.description = description
    
    #"-s", "--server",  "-l", "--login" ,   "-p", "--pwd",   "--https_proxy"    OPTIONS
    __Trnskrbs_basic_options(parser, DoDeleteJob.sDefaultServerUrl)
        
    # ---   
    #parse the command line
    (options, args) = parser.parse_args()
    proxies = {} if not options.https_proxy else {'https_proxy':options.https_proxy}

    # --- 
    #source collection(s)
    try:
        jobid = int(args[0])
    except Exception as e:
        _exit(usage, 1, e)

    # --- 
    doer = DoDeleteJob(options.server, proxies, loggingLevel=logging.INFO)
    __Trnskrbs_do_login_stuff(doer, options, trace=trace, traceln=traceln)

    # --- 
    # do the job...
    try:
        resp = doer.getJobStatus(jobid)
    except Exception as e:  _exit("", 1, e)
    traceln( json.dumps(resp, sort_keys=True, indent=4, separators=(',', ': ')))
    
