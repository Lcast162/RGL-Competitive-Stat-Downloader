import requests, json



def get_logs_data(logs_url):
    logs_url = logs_url.replace("https://logs.tf/", "")
    logs_url = "http://logs.tf/json/" + logs_url

    log_json = json.loads(requests.get(logs_url).content)

    print(logs_url)
    return log_json







