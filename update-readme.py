import requests

username = "drona-gyawali"
headers = {
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'github-pr-tracker'
}

# 1. Get merged PRs authored by you
merged_url = f"https://api.github.com/search/issues?q=type:pr+author:{username}+is:merged&sort=updated&order=desc"
merged_response = requests.get(merged_url, headers=headers).json()
merged = merged_response.get("items", [])[:3]

# 2. Get open PRs authored by you
open_url = f"https://api.github.com/search/issues?q=type:pr+author:{username}+is:open&sort=updated&order=desc"
open_response = requests.get(open_url, headers=headers).json()
open_prs = open_response.get("items", [])[:3]

# 3. Update the README.md
with open("README.md", "r") as file:
    lines = file.readlines()

start = lines.index("<!-- RECENT_PRS_START -->\n")
end = lines.index("<!-- RECENT_PRS_END -->\n")

# Hosted SVG icons (raw.githubusercontent)
merge_icon = "https://raw.githubusercontent.com/drona-gyawali/drona-gyawali/main/.github/assets/icon/merge.svg"
open_icon = "https://raw.githubusercontent.com/drona-gyawali/drona-gyawali/main/.github/assets/icon/open.svg"

new_lines = ["<!-- RECENT_PRS_START -->\n"]
new_lines.append(f'\n<img src="{merge_icon}" width="20"/> **Merged**\n')
for pr in merged:
    new_lines.append(f"- [{pr['title']}]({pr['html_url']})\n")

new_lines.append(f'\n<img src="{open_icon}" width="20"/> **Open**\n')
for pr in open_prs:
    new_lines.append(f"- [{pr['title']}]({pr['html_url']})\n")

new_lines.append("<!-- RECENT_PRS_END -->\n")
lines[start:end+1] = new_lines

with open("README.md", "w") as file:
    file.writelines(lines)
