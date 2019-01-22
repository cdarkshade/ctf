
'''
@Author: Captain Darkshade
Twitter: @cdarkshade
YouTube: Captain Darkshade
Disclaimer: I am not a security professional nor do I consider myself as an expert. 
I am nothing more than a security enthusiast and a beginner at best. Scanning and 
attacking networks and computers without express permission is illegal in many countries. 
Code samples are provided as is and without warranty. All demos conducted in my own isolated lab.
'''

from lxml import etree
from termcolor import colored
import os
import re
import subprocess

tree = etree.parse("openvas_export.xml")
root = tree.getroot()
results = root.xpath("//report/report/results/result")

for result in results:
    name  = result.find("name").text
    severity = result.find("severity").text
    nvt = result.find("nvt")
    cve = nvt.find("cve").text
    bulletin = re.findall("MS\d{2}-\d{3}", etree.tostring(nvt))
    if float(severity) >= 8:
        print("Vulnerabity: %s" % name)
        print(colored("Severity: %s" % severity, "red"))
        print(cve)
        with open(os.devnull, 'wb') as devnull:
            cveSearch = subprocess.check_output("searchsploit " + cve, shell=True, stderr=devnull)
        if "Exploits: No Result" not in cveSearch:
            print cveSearch
        if len(bulletin) > 0:
            with open(os.devnull, 'wb') as devnull:
                msSearch = subprocess.check_output("searchsploit " + bulletin[0], shell=True, stderr=devnull)
            if "Exploits: No Result" not in msSearch:
                print msSearch

        
