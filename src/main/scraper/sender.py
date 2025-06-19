import requests
import sys

from log import log_info, log_error

def notify(content):
    message = {
        "content": content
    }
    response = requests.post("http://127.0.0.1:5000/notify", json=message)
    log_info(response.json())

# sends a message specified from command line
# structure: python3 sender.py -t {message}
if __name__ == '__main__':
    if sys.argv[1] == '-t':
        notify(sys.argv[2])
    else:
        log_error('Manual message to Discord failed')
    
    log_info(f'Manual message to Discord: \"{sys.argv[2]}\"')