import schedule
import time
import whois
from concurrent.futures import ThreadPoolExecutor
import requests

file_path="domains.txt"

topic = "domains_alerts"  # Use your actual, secret topic name
url = f"https://ntfy.sh/domains_alerts"


def get_time() -> str:
    r'''Get current time and date and return as string.'''
    return time.strftime('%X (%d/%m/%y)')
    

def check_domains():
    print("I am working...", get_time())
    try:
        with open(file_path, 'r') as file:
            domain = file.readlines()
            # print(content)
            with ThreadPoolExecutor(max_workers=30) as executor:
                executor.map(check_single_domain, domain)
                
    except FileNotFoundError:
        print("File is not available")

    

def check_single_domain(domain):
    domain = domain.strip()
    try:
        w = whois.whois(domain)
        print(f"{domain} is Taken")
    except OSError:
        print(f"{domain} is struggling")
    except Exception:
        print(f"{domain} is not taken")
        try:                               
            message = f"{domain} is Successfully available for purchase"
            response = requests.post(url, data=message.encode(encoding='utf-8')) # Send the message
            response.raise_for_status() # Raise an exception for bad status codes (4XX or 5XX)
            message = f"You can check the domain price at: https://namecheap.com/domains/registration/results/?domain={domain}"
            print(f"Notification sent to topic '{topic}'")
    
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")


schedule.every(10).seconds.do(check_domains)

while True:
    schedule.run_pending()
    time.sleep(2)




