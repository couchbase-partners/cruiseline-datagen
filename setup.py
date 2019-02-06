
import json
from couchbase.admin import Admin
from couchbase.exceptions import HTTPError
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.analytics import AnalyticsQuery

# The terraform script will out put the IP address
ip_f = open('terraform/ip_address.txt')
ip = str(ip_f.read()).strip('\n')


print('Connecting to Couchbase instance at %s' % (ip))

adm = Admin('Administrator', 'password', host=ip, port=8091)

try:
    adm.bucket_create('commerce')
except HTTPError as err:
    v = err.__dict__['all_results'][None]
    if 'already exists' in v.value['errors']['name']:
        print('Bucket already exists, not creating.')
    

adm.wait_ready('commerce', timeout=10)



# connect w/ SDK
cluster = Cluster('couchbase://' + ip)
auth = PasswordAuthenticator('Administrator', 'password')
cluster.authenticate(auth)
cb = cluster.open_bucket('commerce')


# create anlytics indexes
queries = [
    'CREATE DATASET ships ON `commerce` WHERE `type` = "ship"',
    'CREATE DATASET voyages ON `commerce` WHERE `type` = "voyage"',
    'CREATE DATASET customers ON `commerce` WHERE `type` = "customer"',
    'CREATE DATASET reservations ON `commerce` WHERE `type` = "reservation"',
    'CREATE DATASET credits ON `commerce` WHERE `type` = "credit"',
    'CONNECT LINK Local'
    ]

for q in queries:
    try:
        resp = cb.analytics_query(AnalyticsQuery(q), ip)
        for row in resp:
            print(row)
    except Exception as err:
        print(err)




'''
# Load data
# credit.json
credit_j = json.loads(open('data/credit.json').read())
for doc in credit_j:
    pk = doc['commerce']['metaData']['simpleKey']
    cb.upsert(pk, doc)

# creditUsage.json
docs = json.loads(open('data/creditUsage.json').read())
for doc in docs:
    pk = str(doc['commerce']['passengerId'])
    cb.upsert(pk, doc)

# customer.json
docs = json.loads(open('data/customer.json').read())
for doc in docs:
    pk = doc['commerce']['metaData']['simpleKey']
    cb.upsert(pk, doc)

# reservation.json
docs = json.loads(open('data/reservation.json').read())
for doc in docs:
    pk = doc['commerce']['metaData']['simpleKey']
    cb.upsert(pk, doc)
'''