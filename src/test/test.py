from sender import notify

def test_http_post_valid():
    notify('Hello')

if __name__ == '__main__':
    test_http_post_valid()