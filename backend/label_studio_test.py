from label_studio_sdk.client import LabelStudio
from core.config import settings

ls = LabelStudio(base_url=settings.label_studio_url, api_key=settings.label_studio_api_key)

print("--- Projects ---")
projects = list(ls.projects.list())
for p in projects:
    print(p.id, p.title)

print("\n--- Tasks in first project ---")
if projects:
    project_id = projects[0].id
    tasks = list(ls.tasks.list(project=project_id))
    for t in tasks:
        print(t.id, t.data)
else:
    print("No projects found.")
