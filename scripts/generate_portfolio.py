
import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

profile_path = ROOT / "profile.json"
index_path = ROOT / "index.html"

with profile_path.open("r", encoding="utf-8") as file:
    profile = json.load(file)

content = []

content.append("<section class='generated-profile'>")
content.append("<h2>Professional Profile</h2>")
content.append(f"<h3>{html.escape(profile.get('headline', ''))}</h3>")
content.append(f"<p>{html.escape(profile.get('summary', ''))}</p>")

content.append("<h2>Technical Skills</h2>")
for category, skills in profile.get("skills", {}).items():
    content.append("<div class='skill-group'>")
    content.append(f"<h3>{html.escape(category)}</h3>")
    content.append(
        f"<p>{html.escape(', '.join(skills))}</p>"
    )
    content.append("</div>")

content.append("<h2>Professional Experience</h2>")
for job in profile.get("experience_details", []):
    content.append("<article class='experience-item'>")
    content.append(f"<h3>{html.escape(job.get('company', ''))}</h3>")
    content.append(
        f"<p><strong>{html.escape(job.get('role', ''))}</strong> "
        f"| {html.escape(job.get('period', ''))}</p>"
    )

    for highlight in job.get("highlights", []):
        content.append(f"<p>• {html.escape(highlight)}</p>")

    content.append("</article>")

content.append("</section>")

generated_html = "\n".join(content)

html_content = index_path.read_text(encoding="utf-8")

start_marker = "<!-- GENERATED_PROFILE_START -->"
end_marker = "<!-- GENERATED_PROFILE_END -->"

if start_marker not in html_content or end_marker not in html_content:
    raise ValueError("Portfolio markers were not found in index.html")

start = html_content.index(start_marker) + len(start_marker)
end = html_content.index(end_marker)

if end < start:
    raise ValueError("Portfolio markers are in the wrong order")

updated_html = (
    html_content[:start]
    + "\n"
    + generated_html
    + "\n"
    + html_content[end:]
)

index_path.write_text(updated_html, encoding="utf-8")

print("Portfolio content generated successfully.")
