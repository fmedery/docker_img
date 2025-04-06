# Random Color Hostname App

This simple Flask application displays the hostname of the machine it's running on with a random background color and approximate geolocation on each page load.

## Project Structure

```
.
├── .github/workflows/   # GitHub Actions workflows
│   └── docker-publish.yml
├── templates/
│   └── index.html       # HTML template
├── .gitignore           # Git ignore rules
├── .cursorrules         # Cursor AI rules (ignored by git)
├── app.py               # Main Flask application
├── Dockerfile           # Docker build instructions
├── README.md            # This file
└── requirements.txt     # Python dependencies
```

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd docker_test_image 
    ```

2.  **Create a virtual environment (recommended for local development):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies (for local development):**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up IPinfo Geolocation:**
    This application uses the [IPinfo](https://ipinfo.io/) service to determine the country based on the request's IP address.
    *   Sign up for a free IPinfo account at: [https://ipinfo.io/signup](https://ipinfo.io/signup)
    *   Get your API access token from your IPinfo dashboard.
    *   You will need to provide this token when running the application locally or via Docker (see below).

## Running Locally

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
    `http://localhost:9999`

## Stopping the Local Application

Press `Ctrl+C` in the terminal where the application is running.

## Dockerization

A `Dockerfile` is provided to containerize the application.

1.  **Build the Docker image:**
    ```bash
    docker build -t docker_test_image .
    ```
    *(Replace `docker_test_image` with your preferred image name if desired)*

2.  **Run the Docker container:**
    You need to pass the IPinfo token as an environment variable to the container.
    ```bash
    docker run -p 9999:9999 -e IPINFO_TOKEN='YOUR_API_TOKEN_HERE' docker_test_image
    ```
    *   `-p 9999:9999`: Maps port 9999 on your host to port 9999 in the container.
    *   `-e IPINFO_TOKEN='...'`: Sets the environment variable inside the container.

3.  **Run with Debug Mode:**
    To run the container with Flask debug mode enabled, override the default command:
    ```bash
    docker run -p 9999:9999 -e IPINFO_TOKEN='YOUR_API_TOKEN_HERE' docker_test_image python app.py --debug
    ```

4.  Access the application in your browser at `http://localhost:9999`.

## CI/CD (GitHub Actions)

This repository uses GitHub Actions for continuous integration and deployment.

*   **Workflow:** `.github/workflows/docker-publish.yml`
*   **Trigger:** Pushing a Git tag matching the pattern `v*` (e.g., `v1.0`, `v1.1.0`).
*   **Action:** Builds the Docker image using the `Dockerfile` and pushes it to the GitHub Container Registry (GHCR).
*   **Image Name:** `ghcr.io/<your-github-username>/docker_test_image:<tag>`

**Example (Publishing v1.0):**

```bash
# Make sure your code changes are committed
git tag v1.0
git push origin v1.0
```
This will trigger the GitHub Action, and if successful, the image `ghcr.io/<your-github-username>/docker_test_image:v1.0` will be available. 