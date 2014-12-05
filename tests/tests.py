# Tests for the datastore component.
import requests
import json
import csv
import urllib
import sys
import os
import pandas as pd
import scraperwiki

print('------------------------------------------------')
print('Performing tests:')
print('------------------------------------------------')

resource_id = sys.argv[1]
api_key = sys.argv[2]

# Check if the id of the resource has changed.
def checkID(id, key):

	url = 'https://data.hdx.rwlabs.org/api/action/package_show?id=fts-ebola-coverage'
	h = {'Authorization': key}
	doc = requests.get(url, headers=h)
	data = doc.json()
	new_id = data["result"]["resources"][0]["id"]

	if new_id != id:
		print "ID Check: FAIL"

	else:
		print "ID Check: PASS"

# check if the dataset has one file
def checkNFiles(id, key):

	url = 'https://data.hdx.rwlabs.org/api/action/package_show?id=fts-ebola-coverage'
	h = {'Authorization': key}
	doc = requests.get(url, headers=h)
	data = doc.json()
	nfiles = len(data["result"]["resources"])

	if nfiles == 1:
		print "Number of Files Check: PASS"

	else:
		print "Numbe of Files Check: FAIL"

# check if the file has the right name
def checkFileName(id, key):

	url = 'https://data.hdx.rwlabs.org/api/action/package_show?id=fts-ebola-coverage'
	h = {'Authorization': key}
	doc = requests.get(url, headers=h)
	data = doc.json()
	file_name = data["result"]["resources"][0]["name"]

	if file_name == 'fts-ebola-coverage.csv':
		print "File Name Check: PASS"

	else:
		print "File Name Check: FAIL"


# check if the datastore is active
def checkDataStore(id, key):

	url = 'https://data.hdx.rwlabs.org/api/action/package_show?id=fts-ebola-coverage'
	h = {'Authorization': key}
	doc = requests.get(url, headers=h)
	data = doc.json()
	ds = data["result"]["resources"][0]["datastore_active"]

	if ds:
		print "DataStore Active Check: PASS"

	else:
		print "DataStore Active Check: FAIL"

# querying
def download():
    r = requests.get('https://data.hdx.rwlabs.org/api/action/resource_show?id=93b92803-f9fa-45f4-bf72-73a8ab1d8922')
    doc = r.json()
    fileUrl = doc["result"]["url"]

    # our download parameters
    fileUrl = doc["result"]["url"];
    filename = "tool/data/data.csv";
    urllib.urlretrieve(fileUrl, filename);

# check if the datastore has the same length of results
def checkRecords(key):

	# downloading file
	download()

	# reading file
	df = pd.read_csv('tool/data/data.csv')
	row_count = len(df)

	# getting data from datastore
	ds_query = 'https://data.hdx.rwlabs.org/api/action/datastore_search?resource_id=93b92803-f9fa-45f4-bf72-73a8ab1d8922&amp;limit=100'
	h = {'Authorization': key}
	doc = requests.get(ds_query, headers=h)
	data = doc.json()
	data_count = len(data["result"]["records"])

	if row_count == data_count:
		print "Same Number of Rows Check: PASS"

	else:
		print "Same Number of Rows Check: FAIL"
		print "CSV File: " + str(row_count) + " | " + "DataStore: " + str(data_count)


# check if a single query is the same
# as the datapoint of the original file
def checkValue(api_key):

	def read():
		# reading file
		df = pd.read_csv('tool/data/data.csv')
		file_value = df["Value"][5]
		return file_value

	def test(key):

		# download + read
		download()
		file_value = read()

		# getting data from datastore
		ds_query = 'https://data.hdx.rwlabs.org/api/action/datastore_search?resource_id=93b92803-f9fa-45f4-bf72-73a8ab1d8922&amp;limit=100'
		h = {'Authorization': key}
		doc = requests.get(ds_query, headers=h)
		data = doc.json()
		ds_value = data["result"]["records"][5]["Value"]

		if file_value == ds_value:
			print "Same Value: PASS"
			print('------------------------------------------------')

		else:
			print "Same Value: FAIL"
			print "File: " + str(file_value) + " | " + "DataStore: " + str(ds_value)
			print('------------------------------------------------')

	# calling test function
	test(api_key)


# running functions
def runAllTests():

	try:
		checkID(resource_id, api_key)
		checkFileName(resource_id, api_key)
		checkNFiles(resource_id, api_key)
		checkDataStore(resource_id, api_key)
		checkRecords(api_key)
		checkValue(api_key)

		# if everything ok
		print "All tests passed."
		scraperwiki.status('ok')

	except Exception as e:
		print e
		scraperwiki.status('error', 'Tests failed')
		os.system("mail -s 'DataStore FTS Coverage: tests failed.' luiscape@gmail.com")


runAllTests()


