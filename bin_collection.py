from urllib.parse import urlencode
from urllib.request import Request, urlopen
from datetime import date, timedelta, datetime
import requests

# Find the id for the bin collection API traffic when you search your address at
# https://www.scambs.gov.uk/bins/find-your-bin-collection-day/
# If you inspect the network traffic using Chrome's inspector when searching for
# your address you will be able to see the API URL
collections_api = requests.get('https://refusecalendarapi.azurewebsites.net/collection/search/<id>/')

collection_data = collections_api.json()

today_date = date.today()

collection = collection_data['collections'][0]

collection_date = datetime.strptime(collection['date'], "%Y-%m-%dT%H:%M:%S").date()

if collection_date - today_date == timedelta(days=1):
    bins_to_be_collected = []
    if 'RECYCLE' in collection['roundTypes']:
        bins_to_be_collected.append('blue')
    if 'DOMESTIC' in collection['roundTypes']:
        bins_to_be_collected.append('black')
    if 'ORGANIC' in collection['roundTypes']:
        bins_to_be_collected.append('green')
    message = "The bins to be collected tomorrow are: %s" % ', '.join(bins_to_be_collected)

    # Documentation on this API: https://www.pushsafer.com/en/pushapi
    notification_post_fields = {
        "t" : "Remember to take out your bin",
        "m" : message,
        "s" : 33,  # This sound is a Man Saying Ooohhhweee
        "v" : 3,  # The device will vibrate 3 times,
        "i" : 136,  # The icon of a bin,
        "c" : '',  # iOS doesn't support colour,
        "d" : 15128,
        "u" : '',
        "ut" : '',
        "k" : '<secret>'  # Get your secret from your https://www.pushsafer.com user panel
        }
    request = Request('https://www.pushsafer.com/api', urlencode(notification_post_fields).encode())
    json = urlopen(request).read().decode()
    print(json)
else: 
    print("Tomorrow is not a collection day")
