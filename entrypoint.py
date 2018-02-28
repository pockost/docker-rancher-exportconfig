import requests, sys, json, argparse, os
from requests.exceptions import ConnectionError


def parse_api(url, access_key, secret_key):

    folder_path = '/data/'
    docker_compose_path = folder_path + 'docker-compose.yml'
    rancher_compose_path = folder_path + 'rancher-compose.yml'

    try:
        response = requests.post(
            url,
            auth=(
                access_key,
                secret_key
            ),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            params={
                'serviceIds': []
            }
        )
    except ConnectionError:
        print("Unable to contact this URL")
        sys.exit()

    if response.status_code == 401:
        print("401 Unauthorized, please check your credentials")
        sys.exit()
    elif response.status_code != 200:
        print("An error occurred")
        sys.exit()

    array_response = json.loads(response.text)

    if 'dockerComposeConfig' in array_response:
        docker_compose = open(docker_compose_path, 'w')
        docker_compose.write(array_response['dockerComposeConfig'])
        docker_compose.close()

    if 'rancherComposeConfig' in array_response:
        rancher_compose = open(rancher_compose_path, 'w')
        rancher_compose.write(array_response['rancherComposeConfig'])
        rancher_compose.close()

    if os.path.isfile(docker_compose_path) & os.path.isfile(rancher_compose_path):
        print("Success")
    elif os.path.isfile(docker_compose_path):
        print("We can't create rancher-compose.yml file")
    elif os.path.isfile(rancher_compose_path):
        print("We can't create docker-compose.yml file")
    else:
        print("We can't create files")


parser = argparse.ArgumentParser(description='Use Rancher API to create docker-compose and rancher-compose files')

parser.add_argument('--url', metavar='', type=str, required=True, dest='url',
                    help='Define url of rancher api export config action')
parser.add_argument('--access-key', metavar='', type=str, required=True, dest='access_key',
                    help='Define the access key of rancher api')
parser.add_argument('--secret-key', metavar='', type=str, required=True, dest='secret_key',
                    help='Define the secret key of rancher api')

args = parser.parse_args()

parse_api(args.url, args.access_key, args.secret_key)
