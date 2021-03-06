import json

from anchore_engine.clients import catalog
from anchore_engine.clients import http
import anchore_engine.configuration.localconfig

localconfig = None
headers = {'Content-Type': 'application/json'}

def get_simplequeue_endpoint(userId):
    global localconfig, headers
    if localconfig == None:
        localconfig = anchore_engine.configuration.localconfig.get_config()

    base_url = ""
    try:
        service = None

        service_reports = catalog.get_service(userId, servicename='simplequeue')
        if service_reports:
            service = service_reports[0]

        if not service:
            raise Exception("cannot locate registered simplequeue service")

        endpoint = service['base_url']
        if endpoint:
            base_url = '/'.join([endpoint, 'v1', 'queues'])
        else:
            raise Exception("cannot load valid endpoint from service record")

    except Exception as err:
        raise Exception("could not find valid simplequeue endpoint - exception: " + str(err))

    return(base_url)

def get_queues(userId):
    global localconfig, headers
    if localconfig == None:
        localconfig = anchore_engine.configuration.localconfig.get_config()

    ret = []

    if type(userId) == tuple:
        userId, pw = userId
    else:
        pw = ""
    auth = (userId, pw)

    base_url = get_simplequeue_endpoint(auth)
    url = '/'.join([base_url])

    ret = http.anchy_get(url, auth=auth, headers=headers, verify=localconfig['internal_ssl_verify'])

    return(ret)

def qlen(userId, name):
    global localconfig, headers
    if localconfig == None:
        localconfig = anchore_engine.configuration.localconfig.get_config()

    ret = 0

    if type(userId) == tuple:
        userId, pw = userId
    else:
        pw = ""
    auth = (userId, pw)

    base_url = get_simplequeue_endpoint(auth)
    url = '/'.join([base_url, name, "qlen"])

    ret = http.anchy_get(url, auth=auth, headers=headers, verify=localconfig['internal_ssl_verify'])
    ret = int(ret)

    return(ret)
    
def enqueue(userId, name, inobj, qcount=0, forcefirst=False):
    global localconfig, headers
    if localconfig == None:
        localconfig = anchore_engine.configuration.localconfig.get_config()

    ret = False

    if type(userId) == tuple:
        userId, pw = userId
    else:
        pw = ""
    auth = (userId, pw)

    base_url = get_simplequeue_endpoint(auth)
    url = '/'.join([base_url, name])
    url = url + "?qcount="+str(qcount) + "&forcefirst=" + str(forcefirst)
    payload = inobj

    ret = http.anchy_post(url, data=json.dumps(payload), auth=auth, headers=headers, verify=localconfig['internal_ssl_verify'])

    return(ret)

def is_inqueue(userId, name, inobj):
    global localconfig, headers
    if localconfig == None:
        localconfig = anchore_engine.configuration.localconfig.get_config()

    ret = False

    if type(userId) == tuple:
        userId, pw = userId
    else:
        pw = ""
    auth = (userId, pw)

    base_url = get_simplequeue_endpoint(auth)
    url = '/'.join([base_url, name, 'is_inqueue'])
    payload = inobj

    ret = http.anchy_post(url, data=json.dumps(payload), auth=auth, headers=headers, verify=localconfig['internal_ssl_verify'])

    return(ret)

def dequeue(userId, name):
    global localconfig, headers
    if localconfig == None:
        localconfig = anchore_engine.configuration.localconfig.get_config()

    ret = {}

    if type(userId) == tuple:
        userId, pw = userId
    else:
        pw = ""
    auth = (userId, pw)
    base_url = get_simplequeue_endpoint(auth)
    url = '/'.join([base_url, name])
    ret = http.anchy_get(url, auth=auth, headers=headers, verify=localconfig['internal_ssl_verify'])

    return(ret)

