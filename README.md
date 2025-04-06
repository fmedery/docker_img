# Random Color Hostname & Geolocation App

This is a simple Flask web application that displays:
*   The hostname of the machine it's running on.
*   A randomly changing background color on each request.
*   The approximate country location based on the request's IP address (using IPinfo).

## Project Structure

```
.
├── .github/workflows/   # GitHub Actions workflows
│   └── docker-publish.yml
├── templates/
│   └── index.html       # HTML template for the web page
├── .gitignore           # Specifies intentionally untracked files that Git should ignore
├── .cursorrules         # Cursor AI helper rules (ignored by git)
├── app.py               # Main Flask application logic
├── Dockerfile           # Instructions to build the Docker image
├── README.md            # This file
└── requirements.txt     # Python dependencies
```

## Setup

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url> # Replace with your actual repo URL
    cd docker_test_image
    ```

2.  **Create and Activate Virtual Environment (Recommended for local development):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration: IPinfo Token

This application uses the [IPinfo](https://ipinfo.io/) service for geolocation. You need an API token.

1.  Sign up for a free IPinfo account at: [https://ipinfo.io/signup](https://ipinfo.io/signup)
2.  Get your API access token from your IPinfo dashboard.
3.  You must provide this token when running the application, either via an environment variable or a command-line argument.

## Running Locally

You can run the Flask development server directly.

1.  **Provide the IPinfo Token:** Choose one method:
    *   **Method A: Environment Variable (Recommended for secrets)**
        ```bash
        export IPINFO_TOKEN='YOUR_API_TOKEN_HERE'
        # Then run the app (see step 2)
        ```
        *(On Windows, use `set IPINFO_TOKEN=YOUR_API_TOKEN_HERE` in Command Prompt or `$env:IPINFO_TOKEN='YOUR_API_TOKEN_HERE'` in PowerShell)*

    *   **Method B: Command-Line Argument**
        You will pass this when running the app (see step 2).

2.  **Run the Application:**
    *   **Basic Run (using environment variable for token):**
        ```bash
        # Ensure IPINFO_TOKEN is set via export/set
        python app.py
        ```
    *   **Run with Command-Line Token:**
        ```bash
        python app.py --ipinfo-token='YOUR_API_TOKEN_HERE'
        ```
    *   **Run with Debug Mode Enabled:** Add the `--debug` flag (works with either token method):
        ```bash
        # Using env var token
        export IPINFO_TOKEN='YOUR_API_TOKEN_HERE'
        python app.py --debug
        
        # Using command-line token
        python app.py --ipinfo-token='YOUR_API_TOKEN_HERE' --debug
        ```
    *   **Run without Token (Limited Geolocation):**
        ```bash
        python app.py
        ```

3.  Open your web browser and navigate to `http://localhost:9999`.

4.  **Stop the application:** Press `Ctrl+C` in the terminal.

## Docker

A `Dockerfile` is provided to containerize the application.

1.  **Build the Image:**
    ```bash
    docker build -t docker_test_image .
    ```
    *(You can replace `docker_test_image` with a custom name/tag)*

2.  **Run the Container:**
    You **must** pass the IPinfo token as an environment variable to the container.
    ```bash
    docker run --rm -p 9999:9999 -e IPINFO_TOKEN='YOUR_API_TOKEN_HERE' docker_test_image
    ```
    *   `--rm`: Automatically removes the container when it exits.
    *   `-p 9999:9999`: Maps port 9999 on your host to port 9999 in the container.
    *   `-e IPINFO_TOKEN='...'`: Sets the required environment variable inside the container.

3.  **Run Container with Debug Mode:**
    Override the default command to add the `--debug` flag:
    ```bash
    docker run --rm -p 9999:9999 -e IPINFO_TOKEN='YOUR_API_TOKEN_HERE' docker_test_image python app.py --debug
    ```

4.  Access the application in your browser at `http://localhost:9999`.

## CI/CD (GitHub Actions)

This repository includes a GitHub Actions workflow to automatically build and publish the Docker image to the GitHub Container Registry (GHCR).

*   **Workflow File:** `.github/workflows/docker-publish.yml`
*   **Trigger:** Automatically runs when a Git tag matching the pattern `v*` (e.g., `v1.0`, `v2.1.0`) is pushed to the repository.
*   **Action:** Builds the Docker image defined in `Dockerfile`.
*   **Publish Target:** Pushes the built image to GHCR.
*   **Image Name:** `ghcr.io/<your-github-username>/docker_test_image:<tag>` (Replace `<your-github-username>` with your actual GitHub username or organization name).

**How to Publish a New Version:**

1.  Commit your code changes.
2.  Create a Git tag:
    ```bash
    git tag vX.Y.Z # e.g., git tag v1.0.0
    ```
3.  Push the tag to GitHub:
    ```bash
    git push origin vX.Y.Z # e.g., git push origin v1.0.0
    ```
This push will trigger the GitHub Action, which will build and publish the image `ghcr.io/<your-github-username>/docker_test_image:vX.Y.Z`.

## Using the Published Docker Image (from GHCR)

Once the CI/CD pipeline has successfully published an image version (e.g., `v1.0.0`), you can pull and run it directly from the GitHub Container Registry (GHCR).

1.  **Log in to GHCR:**
    You need to authenticate Docker with GHCR. The recommended way is using a Personal Access Token (PAT) with the `read:packages` scope.
    *   Create a PAT [here](https://github.com/settings/tokens) (select `read:packages` scope).
    *   Log in using the PAT:
        ```bash
        # Replace <USERNAME> with your GitHub username 
        # You will be prompted to enter your PAT as the password
        docker login ghcr.io -u <USERNAME>
        ```

2.  **Pull the Image:**
    Pull the specific version you want to use.
    ```bash
    # Replace <your-github-username> and <tag> (e.g., v1.0.0)
    docker pull ghcr.io/<your-github-username>/docker_test_image:<tag>
    ```

3.  **Run the Image:**
    Remember to provide the required `IPINFO_TOKEN` environment variable.
    ```bash
    # Replace <your-github-username> and <tag>
    docker run --rm -p 9999:9999 \
      -e IPINFO_TOKEN='YOUR_API_TOKEN_HERE' \
      ghcr.io/<your-github-username>/docker_test_image:<tag>
    ```

4.  Access the application in your browser at `http://localhost:9999`.

