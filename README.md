# Random Color Hostname App

This simple Flask application displays the hostname of the machine it's running on with a random background color on each page load.

## Setup

1.  **Clone the repository (if applicable) or ensure you have the files:**
    *   `app.py`
    *   `requirements.txt`
    *   `templates/index.html`

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up IPinfo Geolocation:**
    This application uses the [IPinfo](https://ipinfo.io/) service to determine the country based on the request's IP address.
    *   Sign up for a free IPinfo account at: [https://ipinfo.io/signup](https://ipinfo.io/signup)
    *   Get your API access token from your IPinfo dashboard.
    *   Set the `IPINFO_TOKEN` environment variable before running the application:
        ```bash
        export IPINFO_TOKEN='YOUR_API_TOKEN_HERE'
        ```
        *(On Windows, use `set IPINFO_TOKEN=YOUR_API_TOKEN_HERE` in Command Prompt or `$env:IPINFO_TOKEN='YOUR_API_TOKEN_HERE'` in PowerShell)*
    *   Alternatively, you can provide the token directly using the `--ipinfo-token` command-line argument when running the script (see below). The command-line argument takes precedence over the environment variable.
    *   Note: Without a token provided via either method, the service will work but with stricter rate limits.

## Running the Application

1.  **Set the IPinfo token (choose one method):**
    *   **Environment Variable (Recommended for secrets):**
        ```bash
        export IPINFO_TOKEN='YOUR_API_TOKEN_HERE' 
        python app.py
        ```
    *   **Command-Line Argument:**
        ```bash
        python app.py --ipinfo-token='YOUR_API_TOKEN_HERE'
        ```
    *   **No Token (Limited Functionality):**
        ```bash
        python app.py 
        ```

2.  **Run the Flask app (if not combined with token setting above):**
    ```bash
    # If token was set via environment variable separately
    python app.py
    ```

    You can also enable Flask's debug mode by adding the `--debug` flag:
    ```bash
    # Example with command-line token and debug mode
    python app.py --ipinfo-token='YOUR_API_TOKEN_HERE' --debug

    # Example with environment variable token and debug mode
    export IPINFO_TOKEN='YOUR_API_TOKEN_HERE'
    python app.py --debug

    # Example with no token and debug mode
    python app.py --debug
    ```

3.  Open your web browser and navigate to:
    `http://localhost:9999` or `http://<your-machine-ip>:9999`

    Each time you refresh the page, the background color will change randomly, and the hostname will be displayed.

## Stopping the Application

Press `Ctrl+C` in the terminal where the application is running. 