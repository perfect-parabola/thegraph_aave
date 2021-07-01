import requests, json, csv, os, datetime

# make data directory
if not os.path.exists('data'):
    os.mkdir('data')

# make api call
# get reserves allowed to use as collateral
url = "https://api.thegraph.com/subgraphs/name/aave/protocol-v2"
query = """{
    reserves (where: {
    usageAsCollateralEnabled: true
    }) {
        name
        symbol
    }
}
"""
r = requests.post(url, json={'query': query})
json_data = json.loads(r.text)

# write data file
filename = 'data/Reserves_{}.csv'.format(
    datetime.datetime.now().strftime('%Y.%m.%d_%H:%M:%S')
)
with open(filename, mode='w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['name', 'symbol'])
    for data in json_data.get('data').get('reserves'):
        csv_writer.writerow([data.get('name'), data.get('symbol')])