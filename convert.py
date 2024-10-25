import maxminddb
from netaddr import IPSet
from mmdb_writer import MMDBWriter
from urllib import request

url = 'https://github.com/aknife2019/ip/raw/refs/heads/master/src/data.mmdb'

request.urlretrieve(url,'tmp.mmdb')

writer = MMDBWriter(ip_version=6, ipv4_compatible=True, database_type="DBIP-City-Lite")

with maxminddb.open_database('tmp.mmdb') as reader:
    for network, record in reader:
        print(network)
        writer.insert_network(IPSet([str(network)]), {
            "city": {
                "names": {
                    "en": record['city']['en'],
                    "zh-CN": record['city']['zh-CN']
                }
            },
            "continent": {
                "code": record['continent']['code'],
                "names": {
                    "en": record['continent']['en'],
                    "zh-CN": record['continent']['zh-CN']
                }
            },
            "country": {
                "iso_code": record['country']['code'],
                "names": {
                    "en": record['country']['en'],
                    "zh-CN": record['country']['zh-CN']
                }
            },
            "subdivisions": [{
                "names": {
                    "en": record['region']['en'],
                    "zh-CN": record['region']['zh-CN']
                }
            }]
        })

writer.to_db_file('DBIP-City.mmdb')
