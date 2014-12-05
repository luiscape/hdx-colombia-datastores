# Simple script that manages the creation of
# datastores in CKAN / HDX.

# path to download
PATH = 'tool/data/temp_data.csv'

import os
import csv
import json
import scraperwiki
import ckanapi
import urllib
import requests
import sys
import hashlib
import hdx_resources

# Collecting configuration variables
remote = 'http://data.hdx.rwlabs.org'
apikey = sys.argv[1]

# ckan will be an instance of ckan api wrapper
ckan = None

# Function to download a resource from CKAN.
def downloadResource(filename):

    # querying
    url = 'https://data.hdx.rwlabs.org/api/action/resource_show?id=' + resource_id
    r = requests.get(url)
    doc = r.json()
    fileUrl = doc["result"]["url"]

    # downloading
    try:
        urllib.urlretrieve(fileUrl, filename)
    except:
        print 'There was an error downlaoding the file.'

# Function that checks for old SHA hash
# and stores as a SW variable the new hash
# if they differ. If this function returns true,
# then the datastore is created.
def checkHash(filename, first_run):
    hasher = hashlib.sha1()
    with open(filename, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
        new_hash = hasher.hexdigest()

    # checking if the files are identical or if
    # they have changed
    if first_run:
        scraperwiki.sqlite.save_var('hash', new_hash)
        new_data = False

    else:
        old_hash = scraperwiki.sqlite.get_var('hash')
        scraperwiki.sqlite.save_var('hash', new_hash)
        new_data = old_hash != new_hash

    # returning a boolean
    return new_data


def updateDatastore(filename):

    # Checking if there is new data
    update_data = checkHash(filename, first_run = False)
    if (update_data == False):
        print "\nDataStore Status: No new data. Not updating datastore."
        return

    print "DataStore Status: New data. Updating datastore."

    def upload_data_to_datastore(ckan_resource_id, resource):
        # let's delete any existing data before we upload again
        try:
            ckan.action.datastore_delete(resource_id=ckan_resource_id, force=True)
        except:
            pass

        ckan.action.datastore_create(
                resource_id=ckan_resource_id,
                force=True,
                fields=resource['schema']['fields'],
                primary_key=resource['schema'].get('primary_key'))

        reader = csv.DictReader(open(resource['path']))
        rows = [ row for row in reader ]
        chunksize = 10000
        offset = 0
        print('Uploading data for file: %s' % resource['path'])
        while offset < len(rows):
            rowset = rows[offset:offset+chunksize]
            ckan.action.datastore_upsert(
                    resource_id=ckan_resource_id,
                    force=True,
                    method='insert',
                    records=rowset)
            offset += chunksize
            print('Done: %s' % offset)

    if __name__ == '__main__':
        if len(sys.argv) <= 2:
            usage = '''python scripts/upload.py {resource-id} {api-key}

            e.g.

            python scripts/upload.py http://datahub.io/ RESOURCE_ID API_KEY
            '''
            print(usage)
            sys.exit(1)

        ckan = ckanapi.RemoteCKAN(remote, apikey=apikey)


# wrapper call for all functions
def runEverything(p):
    # iterating through the provided list of resources
    for i in len(resources):
        resource = resources[i]  # grabbing the resource
        upload_data_to_datastore(resource['resource_id'], resource)
        downloadResource(p)
        updateDatastore(p)


# Error handler for running the entire script
try:
    runEverything(PATH)
    # if everything ok
    print "ScraperWiki Status: Everything seems to be just fine."
    scraperwiki.status('ok')

except Exception as e:
    print e
    scraperwiki.status('error', 'Creating datastore failed')
    os.system("mail -s 'Ebola Case data: creating datastore failed.' luiscape@gmail.com")
