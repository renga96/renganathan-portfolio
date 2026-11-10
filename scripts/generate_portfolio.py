
import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "profile.json"
INDEX_PATH = ROOT / "index.html"
NL = chr(10)


def safe(value):
    return html.escape(str(value or ""), quote=True)


def replace_between(document, start_marker, end_marker, new_content):
    if start_marker not in document or end_marker not in document:
        raise ValueError(f"Missing marker: {start_marker} or {end_marker}")

    start = document.index(start_marker) + len(start_marker)
    end = document.index(end_marker)

    if end < start:
        raise ValueError(f"Markers are in the wrong order: {start_marker}")

    return document[:start] + NL + new_content + NL + document[end:]


def build_skills(skills):
    output = []

    for category, items in skills.items():
        if not isinstance(items, list):
            raise ValueError(f"Skills for '{category}' must be a JSON array.")

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

    return NL.join(output)


def build_highlights(highlights):
    if not highlights:
        return ""

    items = NL.join(
        f"<li>{safe(item)}</li>" for item in highlights
    )
    return f"<ul>{NL}{items}{NL}</ul>"


def build_experience(experience_details):
    output = []

    for job in experience_details:
        output.append('<article class="job">')
        output.append(
            '<div class="jobtop">'
            f'<div><h3>{safe(job.get("company"))}</h3>'
            f'<div class="meta">{safe(job.get("role"))}</div></div>'
            f'<div class="date">{safe(job.get("period"))}</div>'
            '</div>'
        )

        projects = job.get("projects")

        if projects:
            for project in projects:
                client = project.get("client", "")
                if client:
                    output.append(
                        f'<div class="client">{safe(client)}</div>'
                    )
                output.append(
                    build_highlights(project.get("highlights", []))
                )
        else:
            client = job.get("client", "")
            if client:
                output.append(
                    f'<div class="client">{safe(client)}</div>'
                )
            output.append(
                build_highlights(job.get("highlights", []))
            )

        output.append("</article>")

    return NL.join(output)


def main():
    with PROFILE_PATH.open("r", encoding="utf-8") as file:
        profile = json.load(file)

    html_content = INDEX_PATH.read_text(encoding="utf-8")

    summary = safe(profile.get("summary", ""))
    skills = build_skills(profile.get("skills", {}))
    experience = build_experience(
        profile.get("experience_details", [])
    )

    html_content = replace_between(
        html_content,
        "<!-- HERO_SUMMARY_START -->",
        "<!-- HERO_SUMMARY_END -->",
        summary
    )

    html_content = replace_between(
        html_content,
        "<!-- SKILLS_START -->",
        "<!-- SKILLS_END -->",
        skills
    )

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
