# import requests

from curl_cffi import requests

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.5",
    # "Connection":	"keep-alive",
    # "Content-Type"	:"application/x-www-form-urlencoded; charset=UTF-8",
    # "Origin":	"https://www.y2mate.com",
    "Referer": "https://www.y2mate.com/search/hello",
    # "Upgrade-Insecure-Requests":	"1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    # "X-Requested-With":	"XMLHttpRequest",
}

payload = {
    "k_query": "https://youtu.be/akEZeHBOyko?si=3p2WreYh6-3EoIpc",
    "k_page": "home",
    "hl": "en",
    "q_auto": "0",
}

session = requests.Session()
session.headers.update(headers)
session.cookies.update(
    {
        "cf_clearance": "0bKyUQFwyXTJ9IdaSCfUZ2_YsZtP9WpeCnjb2UXZZhs-1727812278-1.2.1.1-Almns7kQgsfC4S8oy08yZMvhZXZOa5M1kTxTMSunnnSoqT1qruuGUUzx0M_gnd2ps2qoJ0rOoL3k0TASKfA3dP4HPbFI11S9lNYvP0IjcieG3yFRqA5TSN0wVfJRkvYxMwPCUNVVTz9oAy9ARRGy_IyMNeQu2.NgSFUFJYD0h4v.DA0hwVwgrz4e2Kf5rjFp5ZCYZHMasuUZcnBMOVp9pQE63lBT6l7k0H902pFHvpqE7Y2Y19wHGeQq2FcywYSITB_QzyME2t1tLC1m53MvFrBnxfH5SQ2iIZF1hL7s4FihnPJQs32ik8kAm.TyewgT3MXs2xq1B_vIEAsvbSzQqjZ8scMrIeRppBwfL59JHvu23JkwwN_kqvK2mH1DhVQQ3FvWVbSerNqwjQjUll_iO5fBn00LzuScBep1aRLOHlI"
    }
)


def main():
    url = "https://www.y2mate.com/mates/en948/analyzeV2/ajax"
    resp = session.post(url, data=payload, impersonate="chrome")
    print(resp.status_code, resp.reason)


if __name__ == "__main__":
    main()
