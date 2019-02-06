
# Cruise Line Data Generator

CLDG is a data generation tool that attempts to emulate a dataset similar to what would be used by a Cruise Line.

```

Ships - A list of ships that make up a Cruise line's active fleet
Voyages - A Cruise Line has N number of voyages
Customers & Reservations - Each Voyage has N number of customers (i.e. 3,500). Each customer has a reservation.
Credits - Each Customer makes between X and Y purchases per voyage (i.e. 3 - 10)

```

## Running

### Setting up a virtual environment (optional, recommended)

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Running

```
python datagen.py <path to config>
```

### Configutation

Config informaiton is located in `config.json`. An example:

```
{
    "couchbaseAddress": "52.38.87.178",
    "couchbaseUser": "Administrator",
    "couchbasePassword": "password",
    "targetBucket": "commerce",
    "numVoyages" : 10,
    "customersPerVoyage": 3500,
    "voyagesFromDate": "2018-01-01",
    "minVoyageDays": 3,
    "maxVoyageDays": 14,
    "minCreditsPerCustomer": 1,
    "maxCreditsPerCustomer": 15
}
```

- `couchbaseAddress` - The IP address or hostname to your Couchbase instance
- `couchbaseUser` - Couchbase username
- `couchbasePassword` - Couchbase password
- `targetBucket` - The bucket where generated documents should be upserted
- `numVoyages` - The number of voyages to generate
- `customersPerVoyage` - The number of customers per voyage to generate
- `voyagesFromDate` - The date to start generating voyages from. Dates will be randomly generated.
- `minVoyageDays` -  The shortest duration that a voyage can be
- `maxVoyageDays` - The longest durtation that a voyage can be
- `minCreditsPerCustomer` - The minimum number of purchases a customer can make
- `maxCreditsPerCustomer` - The maximum number of purchases a customer can make


### Sources

- https://www.royalcaribbean.com/cruise-ships
- https://www.cruzely.com/heres-how-much-money-cruise-ships-make-off-every-passenger-infographic/
- https://www.statista.com/statistics/224257/number-of-royal-caribbean-cruise-passengers/