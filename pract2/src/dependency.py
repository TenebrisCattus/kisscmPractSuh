"""Module for fetching direct dependencies from npm registry."""

import json
import sys
import urllib.request
import urllib.error


def fetch_package_data(repo_url: str, package_name: str,
                       version: str) -> dict:
    """Fetch package metadata from npm registry for a given version."""
    base_url = repo_url.rstrip("/")
    url = f"{base_url}/{package_name}/{version}"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except urllib.error.HTTPError as err:
        print(f"HTTP error occurred: {err.code} {err.reason}",
              file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as err:
        print(f"URL error occurred: {err.reason}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON response.", file=sys.stderr)
        sys.exit(1)


def get_direct_dependencies(package_data: dict) -> dict:
    """Extract direct dependencies from package metadata."""
    if not isinstance(package_data, dict):
        return {}
    return package_data.get("dependencies", {})