from firebase_admin import firestore

db = firestore.client()

public_server = 'R6U6M8yjm4VYJ9O9aMuoDpPFYVC2'

servers = 'servers'
notifications = 'notifications'
commands = 'commands'
environment_time = 'env/time'
environment_identifier_factory = 'env/id_fact'
environment = 'env'
time = 'time'
identifier_factory = 'id_fact'
financial_entities = 'financial_entities'
companies = 'companies'
stock_listings = 'stock_listings'
storages = 'storages'
countries = 'countries'
cities = 'cities'
markets = 'markets'
property_listings = 'property_listings'
market_listings = 'market_listings'
properties = 'properties'
products = 'products'
buffs = 'buffs'
user_profiles = 'user_profiles'
currencies = 'currencies'


def get_db(uid=None, options=None):
    if uid is None:
        if options is None:
            return db.document(f'servers/{public_server}')
        else:
            return db.collection(f'servers/{public_server}/{options}')
    else:
        if options is None:
            return db.document(f'servers/{uid}')
        else:
            return db.collection(f'servers/{uid}/{options}')


def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.to_dict()}')
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)


db_notification_ref = db.collection(notifications)
db_commands_ref = db.collection(commands)
db_time_ref = db.document(f'servers/{public_server}').collection('env').document('time')
db_identifier_factory_ref = db.document(f'servers/{public_server}').collection('env').document('id_fact')
db_financial_entities_ref = db.document(f'servers/{public_server}').collection(financial_entities)
db_storages_ref = db.document(f'servers/{public_server}').collection(storages)
db_countries_ref = db.document(f'servers/{public_server}').collection(countries)
db_cities_ref = db.document(f'servers/{public_server}').collection(cities)
db_property_listings_ref = db.document(f'servers/{public_server}').collection(property_listings)
db_market_listings_ref = db.document(f'servers/{public_server}').collection(market_listings)
db_properties_ref = db.document(f'servers/{public_server}').collection(properties)
db_buffs_ref = db.document(f'servers/{public_server}').collection(buffs)
