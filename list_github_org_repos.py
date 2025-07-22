import os
import requests
import getpass
import csv
from datetime import datetime


def list_org_repos():
    org = os.environ.get("GITHUB_ORG")
    if not org:
        org = input("Enter GitHub organization name: ").strip()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        token = getpass.getpass("Enter your GitHub personal access token: ").strip()
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    print(f"Fetching repositories for organization '{org}'...")
    repos = []
    page = 1
    per_page = 100
    while True:
        url = f"https://api.github.com/orgs/{org}/repos"
        params = {"per_page": per_page, "page": page}
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            print(f"Error: {resp.status_code} - {resp.text}")
            return
        data = resp.json()
        if not data:
            break
        repos.extend(data)
        if len(data) < per_page:
            break
        page += 1
    
    # Gather all repo data with language breakdowns
    repo_rows = []
    for repo in repos:
        print(f"Processing repo: {repo.get('name', '')}")
        languages_url = repo.get("languages_url")
        languages_breakdown = ""
        if languages_url:
            lang_resp = requests.get(languages_url, headers=headers)
            if lang_resp.status_code == 200:
                lang_data = lang_resp.json()
                if lang_data:
                    languages_breakdown = ", ".join(f"{lang}: {bytes}" for lang, bytes in lang_data.items())
        owner_login = repo.get("owner", {}).get("login", "")
        # Format updated_at as YYYY-MM-DD
        updated_at_raw = repo.get("updated_at", "")
        updated_at = ""
        if updated_at_raw:
            try:
                updated_at = datetime.strptime(updated_at_raw, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
            except Exception:
                updated_at = updated_at_raw
        repo_rows.append([
            repo.get("name", ""),
            owner_login,
            repo.get("description", ""),
            updated_at,
            repo.get("language", ""),
            languages_breakdown,
            repo.get("html_url", "")
        ])

    # Sort by repo name (case-insensitive)
    repo_rows.sort(key=lambda row: row[0].lower())

    # Write to CSV
    csv_filename = f"{org}_repos_summary.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "owner", "description", "updated_at", "language", "languages_breakdown", "html_url"])
        writer.writerows(repo_rows)
    print(f"\nCSV summary saved to: {csv_filename}")


if __name__ == "__main__":
    list_org_repos() 