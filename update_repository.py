#!/usr/bin/env python3

import os
import shutil
#Compatible with Python 2 and 3
try:
	import urllib.request as urllib
except ImportError:
	import urllib2 as urllib
import xml.etree.ElementTree as ET

#URL
update_url = "https://vapp-updates.vmware.com/vai-catalog/valm/vmw/8d167796-34d5-4899-be0a-6daade4005a3/6.5.0.5100.latest"

#Location to download files
local_location = "/var/www/vc_update_repo"

#Remove old files and create new directories
manifest_dir = local_location + "/manifest"
package_dir = local_location + "/package-pool"

if os.path.exists(manifest_dir):
	shutil.rmtree(manifest_dir)
if os.path.exists(package_dir):
	shutil.rmtree(package_dir)

os.makedirs(manifest_dir)
os.makedirs(package_dir)

#donwload manifest files
manifest_files = ["manifest-latest.xml", "manifest-repo.xml.sign", "manifest-latest.xml.sign", "manifest-repo.xml"]

for manifest_file in manifest_files:
	url = update_url + "/manifest/" + manifest_file
	response = urllib.urlopen(url, timeout = 5)
	html = response.read()

	path = local_location + "/manifest/" + manifest_file
	with open(path, 'bw') as manifest:
		manifest.write(html)


#Reading manifest file to donwload all packages
tree = ET.parse('/var/www/vc_update_repo/manifest/manifest-latest.xml')
root = tree.getroot()

#the location tags contain the name of the packages
for child in root.iter('location'):		
	#Need to remove \n in some location lines (see xml file)
	n = child.text
	name = n.replace("\n", "")
	url_f = update_url + "/" + name
	response = urllib.urlopen(url_f)
	html = response.read()

	path = local_location + "/" + name
	with open(path, 'bw') as package:
		package.write(html)


#Download JSON file 
url = update_url + "/package-pool/rpm-manifest.json"
response = urllib.urlopen(url, timeout = 5)
html = response.read()
path = local_location + "/package-pool/rpm-manifest.json"
with open(path, 'bw') as json_file:
	json_file.write(html)





