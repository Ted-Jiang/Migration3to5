import requests
from getpass import getpass



kylin4headers = {
    "Authorization": 'Basic a3lsaW5kZXY6SGFwcHkxMjMhMTIzMjAyMA==',
    "Accept": "application/vnd.apache.kylin-v4+json",
}

test_url = "xxx/kylin/api/query/history_queries?realization=&query_status=&submitter=&project=benchmark&limit=20&offset=0&start_time_from=&start_time_to=&latency_from=&latency_to=&server=&sql=yan"

 # ignore warning


if __name__ == '__main__':

    user = input("Username: ")
    pwd = getpass("Password (Bin + Yubikey): ")

    http_proxy_url = "http://"
    https_proxy_url = "https://"

    proxies = {
        "http": http_proxy_url,
        "https": https_proxy_url
    }

    requests.packages.urllib3.disable_warnings()
    with requests.Session() as s:
        s.proxies = proxies
        s.headers = kylin4headers
        r = s.get(test_url, headers=kylin4headers, verify=False)
        print(r.text)
        print(r.status_code)