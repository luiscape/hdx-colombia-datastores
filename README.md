# HDX Colombia Page DataStores
Repository that gathers the scripts that manage HDX's Colombia page DataStores. In oposition to the [Ebola page](https://data.hdx.rwlabs.org/ebola), this repository decided to generalize the function to work with a list of CKAN `resource_ids`.

# Usage
The main function is `createDatastore()`. That function takes two parameters: `PATH` and `resources`.

# Shortcomings
Unfortunately, *at this point*, there are the following pending issues:

* The CKAN resources must be CSVs.
* The schema of each file must be clearly defined.

Hopefully in next versions the types of each columns would be guessed (correctly) and this function would not need that explicit declaration. In those cases, the function should take only a resource id.