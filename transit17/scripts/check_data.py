import requests

def check_data():
    url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs'
    response = requests.get(url)
    print(f"Status code: {response.status_code}")
    print(f"Content type: {response.headers.get('content-type')}")
    print("\nFirst 1000 bytes of content:")
    print(response.content[:1000])

if __name__ == '__main__':
    check_data() 