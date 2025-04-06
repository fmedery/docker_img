import os
import random
import ipinfo
import argparse
from flask import Flask, render_template, request

app = Flask(__name__)

# --- IPinfo Setup Function ---
# Moved setup into a function to be called after parsing args
def setup_ipinfo_handler(token=None):
    """Initializes the IPinfo handler using the provided token, env var, or no token."""
    # Prioritize provided token (from arg parser)
    if token:
        print("Using IPinfo token from command-line argument.")
        return ipinfo.getHandler(token)
    
    # Fallback to environment variable
    env_token = os.environ.get('IPINFO_TOKEN')
    if env_token:
        print("Using IPinfo token from environment variable.")
        return ipinfo.getHandler(env_token)
    
    # If no token provided, initialize without one (limited requests)
    print("WARNING: IPinfo token not provided via arg or env var. Geolocation might be limited or fail.")
    return ipinfo.getHandler()

ipinfo_handler = None # Initialize as None, will be set in main block
# ---------------------------

@app.route("/")
def index():
    hostname = os.uname().nodename
    # Generate a random hex color
    random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

    country_code = None
    country_name = None
    ip_address = request.remote_addr

    # Check for localhost/private IPs first to avoid unnecessary API calls
    is_local_ip = (not ip_address or
                   ip_address.startswith(('127.', '192.168.', '10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.2', '172.3')) or
                   ip_address == '::1')

    if is_local_ip:
        print(f"Local or private IP address detected: {ip_address}. Skipping IPinfo lookup.")
        country_name = "Localhost"
    elif not ipinfo_handler: # Check if handler was initialized
        print("ERROR: IPinfo handler not initialized.")
        country_name = "Error"
    else:
        try:
            details = ipinfo_handler.getDetails(ip_address)
            country_code = getattr(details, 'country', None) # Use getattr for safety
            country_name = getattr(details, 'country_name', None)
            if not country_code:
                 print(f"Could not determine country code for IP: {ip_address}")
            if not country_name:
                 print(f"Could not determine country name for IP: {ip_address}")

        except Exception as e:
            print(f"Error looking up IP {ip_address} with IPinfo: {e}")
            country_name = "Error"

    return render_template(
        "index.html",
        hostname=hostname,
        background_color=random_color,
        country_code=country_code,
        country_name=country_name
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the Random Color Hostname Flask app.')
    parser.add_argument('--ipinfo-token', type=str, default=None,
                        help='IPinfo API token. Overrides IPINFO_TOKEN environment variable.')
    parser.add_argument('--debug', action='store_true',
                        help='Enable Flask debug mode.')
    args = parser.parse_args()

    # Setup IPinfo handler using token from args (or env var as fallback)
    ipinfo_handler = setup_ipinfo_handler(args.ipinfo_token)

    # Pass debug flag to app.run
    app.run(host="0.0.0.0", port=9999, debug=args.debug)
    # No need to close reader anymore 