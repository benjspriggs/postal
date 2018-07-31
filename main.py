import sys
from geolocation.main import GoogleMaps
import pandas as pd

google_maps = GoogleMaps(api_key='your_google_maps_key') 


def get_location_model(address):
    print('Searching address: ', address)
    return google_maps.search(location=address)

key = 'Mailing Address'

def main():
    guest_list = pd.read_csv(sys.argv[1])
    existing = guest_list[key].notnull() 
    mailing_addresses = guest_list[existing]
    locations = map(lambda row: get_location_model(row[1][key]), mailing_addresses.iterrows())
    print(list(locations))

if __name__ == "__main__":
    main()
