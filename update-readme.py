import requests

username = "drona-gyawali"
repo = "drona-gyawali"


headers = {'Accept': 'application/vnd.github.v3+json'}
prs_url = f"https://api.github.com/repos/{username}/{repo}/pulls?state=all"
response = requests.get(prs_url, headers=headers)
all_prs = response.json()

merged = []
open_prs = []

for pr in all_prs:
    if pr["state"] == "open":
        open_prs.append(pr)
    elif pr["state"] == "closed" and pr.get("merged_at"):
        merged.append(pr)

merged = merged[:3]
open_prs = open_prs[:3]

with open("README.md", "r") as file:
    lines = file.readlines()

start = lines.index("<!-- RECENT_PRS_START -->\n")
end = lines.index("<!-- RECENT_PRS_END -->\n")

new_lines = ["<!-- RECENT_PRS_START -->\n"]
new_lines.append("✅ **Merged**\n")
for pr in merged:
    new_lines.append(f"- [✨ {pr['title']}]({pr['html_url']})\n")

new_lines.append("\n🚧 **Open**\n")
for pr in open_prs:
    new_lines.append(f"- [🚀 {pr['title']}]({pr['html_url']})\n")

new_lines.append("<!-- RECENT_PRS_END -->\n")
lines[start:end+1] = new_lines

with open("README.md", "w") as file:
    file.writelines(lines)
