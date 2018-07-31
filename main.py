import sys
from multiprocessing import Pool
from functools import reduce
from geolocation.main import GoogleMaps
import pandas as pd

google_maps = GoogleMaps(api_key='your_google_maps_key') 

key = 'Mailing Address'

def get_location_model(row):
    address = row[key]
    try:
        print('Searching address: ', address)
        return (row, google_maps.search(location=address).first())
    except Exception:
        print('Failed for: ', row['First Name'])

def to_df(lm):
    if lm is None:
        return pd.DataFrame()

    row, location = lm

    return pd.DataFrame({
        'Full name': [row['First Name'] + ' ' + row['Last Name']],
        'Address line 1': [location.street_number + ' ' + location.route],
        'City': [location.city],
        'State/Province': [location.country_shortcut],
        'ZIP/Postal Code': [location.postal_code],
        'Country': [location.country]
    })

def main():
    guest_list = pd.read_csv(sys.argv[1])
    existing = guest_list[key].notnull() 
    mailing_addresses = guest_list[existing]
    locations = map(lambda row: get_location_model(row[1]), mailing_addresses.iterrows())

    df = pd.DataFrame(columns=[
        'Full name',
        'Address line 1',
        'Address line 2',
        'City',
        'State/Province',
        'ZIP/Postal Code',
        'Country'
        ])

    things = map(to_df, locations)

    addrs = pd.concat(things)

    addrs.to_csv("test.csv")

if __name__ == "__main__":
    main()
