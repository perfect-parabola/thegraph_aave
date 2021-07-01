import requests, json, sys, csv, os, datetime
from utils import toUnixtime, toString

# make data directory
if not os.path.exists('data'):
    os.mkdir('data')

# get system var
token_symbol = sys.argv[1]


# make api call
#get token reserve id
url = "https://api.thegraph.com/subgraphs/name/aave/protocol-v2"
query = """{
    reserves(
    first:1
    symbol: %s
    ) {
        id
    }
}
""" %(token_symbol)
r = requests.post(url, json={'query': query})
json_data = json.loads(r.text)
reserve_id = json_data.get('data').get('reserves')[0].get('id')
print(reserve_id)

query = """{
    flashLoans(
        orderBy: timestamp,
        orderDirection: desc,
        where:{
            reserve: "%s"
        }
    ) {
        id
        amount
        totalFee
        timestamp
    }
}
""" %(reserve_id)
r = requests.post(url, json={'query': query})
json_data = json.loads(r.text)

# write data file
filename = 'data/ReserveFlashLoanData_{}_{}.csv'.format(
    token_symbol,
    datetime.datetime.now().strftime('%Y.%m.%d_%H:%M:%S')
)
with open(filename, mode='w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['datetime', 'amount', 'totalfee'])
    for data in json_data.get('data').get('flashLoans'):
        csv_writer.writerow([
            toString(data.get('timestamp')), data.get('amount'), data.get('totalFee')
        ])
