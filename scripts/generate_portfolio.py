
import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "profile.json"
INDEX_PATH = ROOT / "index.html"


def safe(value):
    """Escape text before inserting it into HTML."""
    return html.escape(str(value or ""), quote=True)


def replace_between(document, start_marker, end_marker, new_content):
    """Replace only the content between two existing HTML markers."""
    if start_marker not in document or end_marker not in document:
        raise ValueError(
            f"Missing marker: {start_marker} or {end_marker}"
        )

    start = document.index(start_marker) + len(start_marker)
    end = document.index(end_marker)

    if end < start:
        raise ValueError(f"Markers are in the wrong order: {start_marker}")

    return document[:start] + "\n" + new_content + "\n" + document[end:]


def build_skills(skills):
    output = []

    for category, items in skills.items():
        if not isinstance(items, list):
            raise ValueError(
                f"Skills for '{category}' must be a JSON array."
            )

        tags = "".join(
            f'<span class="tag">{safe(item)}</span>'
            for item in items
        )

        output.append(
            '<div class="skill">'
            f'<h3>{safe(category)}</h3>'
            f'<div class="tags">{tags}</div>'
            '</div>'
        )

    return "\n".join(output)


def build_experience(experience_details):
    output = []

    for job in experience_details:
        company = safe(job.get("company"))
        role = safe(job.get("role"))
        period = safe(job.get("period"))

        output.append('<article class="job">')
        output.append(
            '<div class="jobtop">'
            f'<div><h3>{company}</h3>'
            f'<div class="meta">{role}</div></div>'
            f'<div class="date">{period}</div>'
            '</div>'
        )

        clients = job.get("clients", [])
        if isinstance(clients, str):
            clients = [clients]

        if not clients and job.get("client"):
            clients = [job["client"]]

        if clients:
            output.append(
                f'<div class="client">{safe(" · ".join(clients))}</div>'
            )

        highlights = job.get("highlights", [])

        if highlights:
            output.append("<ul>")
            for highlight in highlights:
                output.append(f"<li>{safe(highlight)}</li>")
            output.append("</ul>")

        output.append("</article>")

    return "\n".join(output)


def main():
    with PROFILE_PATH.open("r", encoding="utf-8") as file:
        profile = json.load(file)

    html_content = INDEX_PATH.read_text(encoding="utf-8")

    summary = safe(profile.get("summary", ""))
    skills = build_skills(profile.get("skills", {}))
    experience = build_experience(
        profile.get("experience_details", [])
    )

    # Update the existing hero summary.
    html_content = replace_between(
        html_content,
        "<!-- HERO_SUMMARY_START -->",
        "<!-- HERO_SUMMARY_END -->",
        summary
    )

    # Update the existing About summary.
    html_content = replace_between(
        html_content,
        "<!-- ABOUT_SUMMARY_START -->",
        "<!-- ABOUT_SUMMARY_END -->",
        summary
    )

    # Update the existing skills grid.
    html_content = replace_between(
        html_content,
        "<!-- SKILLS_START -->",
        "<!-- SKILLS_END -->",
        skills
    )

    # Update the existing experience timeline.
    html_content = replace_between(
        html_content,
        "<!-- EXPERIENCE_START -->",
        "<!-- EXPERIENCE_END -->",
        experience
    )

    INDEX_PATH.write_text(html_content, encoding="utf-8")

    print("Portfolio sections updated successfully.")


if __name__ == "__main__":
    main()
