import requests, json

logs_tf_api_key = "76561198013747901#743f3a5b51eb2da7"


def get_logs_data(logs_url):
    logs_url = logs_url.replace("https://logs.tf/", "")
    logs_url = "http://logs.tf/json/" + logs_url

    log_json = json.loads(requests.get(logs_url).content)

    print(logs_url)
    return log_json







