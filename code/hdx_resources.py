## hdx_resources
#  This is where the resources are declared. For now,
#  they are declared as a Python list.

# defining the schemas.
# 2 resources are declared here.
resources = [
    {
        'resource_id': '6b0175c6-1209-42ed-9026-8bbaca7ea310',
        'path': PATH,
        'schema': {
            "fields": [
              { "id": "Year", "type": "integer" },
              { "id": "Persons", "type": "float" }
            ]
        },
    },
    {
        'resource_id': '9e69d499-0b2b-4da6-9c61-10e453a57504',
        'path': PATH,
        'schema': {
            "fields": [
              { "id": "Month", "type": "date" },
              { "id": "Persons", "type": "float" }
            ]
        },
    }
]
