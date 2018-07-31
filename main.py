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
        return

    row, location = lm

    street = location.formatted_address.split(",")[0]

    return pd.DataFrame({
        'Full name': [row['First Name'] + ' ' + row['Last Name']],
        'Address line 1': [street],
        'Address line 2': [None],
        'City': [str(location.city)],
        'State/Province': [str(location.country_shortcut)],
        'ZIP/Postal code': [str(location.postal_code)],
        'Country': [str(location.country)]
    })

def main():
    guest_list = pd.read_csv(sys.argv[1])
    existing = guest_list[key].notnull() 
    mailing_addresses = guest_list[existing]
    locations = map(lambda row: get_location_model(row[1]), mailing_addresses.iterrows())

    things = map(to_df, locations)

    addrs = pd.concat(things)

    addrs.to_csv(sys.argv[2], index=False)

if __name__ == "__main__":
    main()
