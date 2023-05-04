import ipinfo
import sys

# get the ip address from command line

try:
    ip_address = sys.argv[1]
except IndexError:
    ip_address = None

# access token for ipinfo.io
access_token = 'Insert your ipinfo.io token here'

#Create a client object with token
handler = ipinfo.getHandler(access_token)

# Get the IP info
details = handler.getDetails(ip_address)

# Print the Information we found

for key, value in details.all.items():
    print(f"{key}: {value}")

