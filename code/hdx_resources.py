## hdx_resources
#  This is where the resources are declared. For now,
#  they are declared as a Python list.

# defining the schemas.
# 4 resources are declared here.
resources = [
    {
        'resource_id': '3fb3f50e-6bb7-44af-8ac9-6e50db433f67',
        'path': PATH,  # check if the path continues the same
        'schema': {
            "fields": [
              { "id": "Ano", "type": "date" },
              { "id": "IDPs_historico", "type": "float" }
            ]
        },
    },
    {
        'resource_id': '9e69d499-0b2b-4da6-9c61-10e453a57504',
        'path': PATH,
        'schema': {
            "fields": [
              { "id": "CHD_Indicator_Code", "type": "text" },
              { "id": "Date", "type": "timestamp" }
            ]
        },
    },
    {
        'resource_id': '0f39852c-e4bd-4c41-b5a1-88f38564955f',
        'path': PATH,
        'schema': {
            "fields": [
              { "id": "CHD_Indicator_Code", "type": "text" },
              { "id": "Date", "type": "timestamp" }
            ]
        },
    },
    {
        'resource_id': '6b0175c6-1209-42ed-9026-8bbaca7ea310',
        'path': PATH,
        'schema': {
            "fields": [
              { "id": "Ano", "type": "date" },
              { "id": "IDPs_historico", "type": "float" }
            ]
        },
    }
]
