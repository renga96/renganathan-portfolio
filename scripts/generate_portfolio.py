
import json
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
PROFILE_FILE = ROOT / "profile.json"
HTML_FILE = ROOT / "index.html"

profile = json.loads(PROFILE_FILE.read_text(encoding="utf-8"))
html = HTML_FILE.read_text(encoding="utf-8")

def safe(value):
    return escape(str(value), quote=True)

# Build a portfolio content section from approved profile data.
skills_html = ""
for category, skills in profile["skills"].items():
    skills_html += f"""
    <div class="skill-group">
      <h3>{safe(category)}</h3>
      <p>{safe(" • ".join(skills))}</p>
    </div>
    """

experience_html = ""
for job in profile["experience_details"]:
    highlights = "".join(
        f"<li>{safe(item)}</li>" for item in job["highlights"]
    )
    experience_html += f"""
    <article class="experience-item">
      <h3>{safe(job["company"])}</h3>
      <p><strong>{safe(job["role"])}</strong> |
      {safe(job["period"])}</p>
      <ul>{highlights}</ul>
    </article>
    """

new_content = f"""
<section id="generated-profile">
  <h2>Professional Profile</h2>
  <h3>{safe(profile["headline"])}</h3>
  <p>{safe(profile["summary"])}</p>

  <h2>Skills</h2>
  {skills_html}

  <h2>Professional Experience</h2>
  {experience_html}
</section>
"""

start_marker = "<!-- GENERATED_PROFILE_START -->"
end_marker = "<!-- GENERATED_PROFILE_END -->"

if start_marker not in html or end_marker not in html:
    raise RuntimeError(
        "Portfolio markers are missing. Add them before enabling generation."
    )

before, remainder = html.split(start_marker, 1)
_, after = remainder.split(end_marker, 1)

updated_html = (
    before + start_marker + new_content + end_marker + after
)

HTML_FILE.write_text(updated_html, encoding="utf-8")

print("Portfolio generated successfully.")
