# GitHub Organization Repository Lister

This Python script lists all repositories in a specified GitHub organization and exports detailed information about each repository to a CSV file. The CSV includes repository name, owner, description, last updated date, main language, a breakdown of all detected languages, and the repository URL.

## Features
- Fetches all repositories for a GitHub organization (handles pagination)
- Outputs a CSV file with the following columns:
  - `name`: Repository name
  - `owner`: Owner's login (username)
  - `description`: Repository description
  - `updated_at`: Last updated date (YYYY-MM-DD)
  - `language`: Main programming language
  - `languages_breakdown`: All detected languages with byte counts
  - `html_url`: Repository URL
- Uses your GitHub personal access token for authentication
- Organization and token can be provided via environment variables or prompted interactively
- Prints progress messages while processing

## Requirements
- Python 3.7+
- [`requests`](https://pypi.org/project/requests/)

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Set Environment Variables (Recommended)
```bash
export GITHUB_ORG=your_org_name
export GITHUB_TOKEN=your_github_token
```

### 2. Run the Script
```bash
python list_github_org_repos.py
```

If you do not set the environment variables, the script will prompt you for the organization name and/or token.

### 3. Output
The script will create a CSV file named `<org>_repos_summary.csv` in the current directory, where `<org>` is the organization name.

#### Example CSV Output
| name      | owner   | description         | updated_at | language   | languages_breakdown         | html_url                        |
|-----------|---------|---------------------|------------|------------|-----------------------------|---------------------------------|
| example   | myorg   | Example repository  | 2024-06-07 | Python     | Python: 12345, HTML: 6789   | https://github.com/myorg/example|

## How to Get a GitHub Personal Access Token
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Select scopes: `repo` (for private repos) or `public_repo` (for public only)
4. Copy and save your token securely

## Notes
- The script makes one additional API call per repository to fetch the language breakdown.
- For large organizations, this may take a few minutes and use more API quota.
- The script prints progress messages so you know it is working.
