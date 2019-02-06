import json
import sys
from datetime import datetime
from datetime import timedelta
from random import randint, getrandbits, choice
from faker import Faker
from faker.providers import date_time, person, address
from dateutil import parser
from couchbase.exceptions import HTTPError
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator


'''
1. Voyages - create n cruises
    voyageId
    startDate
    endDate
    shipId

2. Customers and Reservations - create (num cruises * 5000)
    Resrvation:
        reservationId
        reservationDate
        voyageId
    Customer:
        custId
        name
        gender
        citizenship
        reservationId

3. Credit - create (num reservations * 10)
    creditId
    amount
    type
    reservationId
    transactionDate

# create 10 cruises
'''

fake = Faker()
fake.add_provider(date_time)
fake.add_provider(person)
fake.add_provider(address)



# load config
config = json.loads(open(sys.argv[1]).read())

shipNames = ['Empress of the Seas', 'Majesty of the Seas', 'Grandeur of the Seas', 'Rhapsody of the Seas', 'Enchantment of the Seas', 'Vision of the Seas', 'Voyager of the Seas', 'Explorer of the Seas', 'Adventure of the Seas', 'Navigator of the Seas', 'Mariner of the Seas', 'Radiance of the Seas', 'Brilliance of the Seas', 'Serenade of the Seas', 'Jewel of the Seas', 'Freedom of the Seas', 'Liberty of the Seas', 'Independence of the Seas','Oasis of the Seas', 'Allure of the Seas', 'Harmony of the Seas', 'Symphony of the Seas', 'Quantum of the Seas', 'Anthem of the Seas', 'Ovation of the Seas']
creditAmounts = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400]
creditTypes = ['AAAA', 'AAAB', 'AAAC', 'AAAD', 'AAAE', 'AAAF']
reservationTypes = ['I', 'I', 'G'] # ~2/1 ratio of Is to Gs
reservationStatuses = ['BK', 'CX'] # 1/1 ratio

def dateconverter(o):
    return str(o)


# Couchbase
cluster = Cluster('couchbase://' + config['couchbaseAddress'])
auth = PasswordAuthenticator(config['couchbaseUser'], config['couchbasePassword'])
cluster.authenticate(auth)
cb = cluster.open_bucket(config['targetBucket'])

voyageIds = []
shipIds = []

# create ships
for s in shipNames:
    ship = {}
    ship['type'] = 'ship'
    ship['name'] = s
    ship['shipId'] = 'ship:' + s.replace(' ', '-')
    shipIds.append(ship['shipId'])
    cb.upsert(ship['shipId'], ship)


print("Generating records for %d voyages" % (config['numVoyages']))

for i in range(config['numVoyages']):
    voyage = {}
    voyage['type'] = 'voyage'
    voyage['voyageId'] = 'voyage:' + str(i)
    voyageIds.append(voyage['voyageId'])

    # start and end date
    start_dt = fake.date_between_dates(date_start=parser.parse(config['voyagesFromDate']), date_end=None)
    #cruises are 3-14 days long, pick a random int between there
    num_days = randint(config['minVoyageDays'], config['maxVoyageDays'])
    # add days to get the end date
    end_dt = start_dt + timedelta(days=num_days)
    voyage['startDate'] = start_dt
    voyage['endDate'] = end_dt
    voyage['shipId'] = choice(shipIds) # pretend RCCL has 50 ships

    # save voyage
    doc = json.dumps(voyage, default=dateconverter)
    cb.upsert(voyage['voyageId'], json.loads(doc))

    # for each voyage, create 5k customers and reservations
    customerIds = []
    reservationIds = []
    #for voyageId in voyageIds:
    for i in range(config['customersPerVoyage']):
        '''
        Customer:
            customerId
            firstName
            lastName
            gender
            citizenship
            reservationId
        '''
        customer = {}
        customer['type'] = 'customer'

        is_male = bool(getrandbits(1))
        if is_male:
            customer['fistName'] = fake.first_name_male()
            customer['lastName'] = fake.last_name_male()
            customer['gender'] = 'M'
        else:
            customer['firstName'] = fake.first_name_female()
            customer['lastName'] = fake.last_name_female()
            customer['gender'] = 'F'

        customer['customerId'] = 'cust:' + voyage['voyageId'] + ':' + str(i)
        customer['citizenship'] = fake.country()

        # save customer
        doc = json.dumps(customer, default=dateconverter)
        cb.upsert(customer['customerId'], json.loads(doc))

        # Now create their reservation
        '''
        reservationId
        reservationDate
        voyageId        
        '''
        reservation = {}
        reservation['type'] = 'reservation'
        reservation['reservationId'] = 'res:' + customer['customerId']
        reservation['reservationType'] = choice(reservationTypes)
        reservation['status'] = choice(reservationStatuses)
        # make sure the reservation is not after the voyage's start date
        # booking dates should be within 400 days of voyage start date
        book_from_dt = voyage['startDate'] - timedelta(days=400)
        reservation['bookingDate'] = fake.date_between_dates(date_start=book_from_dt, date_end=voyage['startDate'])
        reservation['voyageId'] = voyage['voyageId']        

        # save reservation
        doc = json.dumps(reservation, default=dateconverter)
        cb.upsert(reservation['reservationId'], json.loads(doc))

        '''
        3. Credit - create (num reservations * 10)
        creditId
        amount
        type
        reservationId
        transactionDate
        '''
        numCredits = randint(config['minCreditsPerCustomer'], config['maxCreditsPerCustomer']) # 1 - 15 credits
        for c in range(numCredits):
            credit = {}
            credit['type'] = 'credit'
            credit['creditId'] = 'credit:' + customer['customerId'] + ':' + str(c)
            credit['amount'] = choice(creditAmounts)
            credit['creditType'] = choice(creditTypes)
            credit['reservationId'] = reservation['reservationId']
            # transaction date must be during the voyage
            credit['transactionDate'] = fake.date_between_dates(date_start=voyage['startDate'], date_end=voyage['endDate'])
                    # save reservation
            doc = json.dumps(credit, default=dateconverter)
            cb.upsert(credit['creditId'], json.loads(doc))

    print('Completed generated records for voyageId %s' % (voyage['voyageId']))
            
            






