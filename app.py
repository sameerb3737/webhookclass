# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "shipping.cost":
        return {}
    result = req.get("result")
    sessionID = result.get("sessionId")
    contexts = result.get("contexts")
    contextName = contexts[0].get("name");
    #parameters = result.get("parameters")
    #zone = parameters.get("shipping-zone")

    cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}
    var5	="          \"type\": 0,	"
    var6	="          \"platform\": \"facebook\",	"
    var7	="          \"speech\": \"Question Text1\"	"
    speech = "HELLO"
    speech1 = var5 + var6  + var7

    print("Response:")
    print(speech)
     #"contextOut": [],
    emptyspace = ""
    return {
     "contexts": [
      {
        "name": "chapter1",
        "parameters": {
          "answer": "1",
          "answer.original": ""
        },
        "lifespan": 5
      },
      {
        "name": "q2",
        "parameters": {
          "answer": "1",
          "answer.original": ""
        },
        "lifespan": 5
      }
    ],
     
   "speech":"",
   "messages":[
      {
         "type":3,
         "platform":"facebook",
         "imageUrl":"http://charityrefresh.org/ella/asset.hello-ella.gif"
      },
      {
         "type":0,
         "platform":"facebook",
         "speech":"My First response "
      },
      {
         "type":0,
         "platform":"facebook",
         "speech":"My Second Responsedd "
      },
       {
          "type": 2,
          "platform": "facebook",
          "title": "What can I help you with",
          "replies": [
            "A",
            "B",
            "C"
          ]
     },
      {
         "type":4,
         "platform":"facebook",
         "payload":{
            "facebook":{
               "attachment":{
                  "type":"template",
                  "payload":{
                     "template_type":"button",
                     "text":"What can I help you with?",
                     "buttons":[
                        {
                           "type":"postback",
                           "title":"Answer A",
                           "payload":"A"
                        },
                        {
                           "type":"postback",
                           "title":"Answer B",
                           "payload":"B"
                        },
                        {
                           "type":"postback",
                           "title":"Answer C",
                           "payload":"C"
                        }
                     ]
                  }
               }
            }
         }
      }
   ]
}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
