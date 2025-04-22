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

new_lines = ["<!-- RECENT_PRS_START -->\n"]
new_lines.append("\n **Merged**\n")
for pr in merged:
    new_lines.append(f"- [{pr['title']}]({pr['html_url']})\n")

new_lines.append("\n **Open**\n")
for pr in open_prs:
    new_lines.append(f"- [{pr['title']}]({pr['html_url']})\n")

new_lines.append("<!-- RECENT_PRS_END -->\n")
lines[start:end+1] = new_lines

with open("README.md", "w") as file:
    file.writelines(lines)
