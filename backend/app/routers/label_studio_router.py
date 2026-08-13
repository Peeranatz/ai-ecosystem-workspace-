from fastapi import APIRouter, status, Query, Body
from typing import List, Dict, Any
from app.services.label_studio_service import LabelStudioService

router = APIRouter(prefix="/ls", tags=["6. Label Studio Component Domain"])

@router.get("/projects", response_model=List[Dict[str, Any]], summary="List Label Studio Projects", description="Fetch data annotation projects from Label Studio SDK")
async def list_ls_projects():
    """Retrieve active annotation projects from Label Studio."""
    return LabelStudioService.list_projects()

@router.post("/projects", status_code=status.HTTP_201_CREATED, summary="Create Annotation Project", description="Create a new Label Studio data labeling project")
async def create_ls_project(
    title: str = Body(..., description="Title of the annotation project"),
    description: str = Body("", description="Detailed description of data labeling goals")
):
    """Create a new project in Label Studio via SDK."""
    return LabelStudioService.create_project(title=title, description=description)

@router.post("/tasks/import", summary="Import Dataset Tasks", description="Import raw dataset files/links into Label Studio project for labeling")
async def import_ls_tasks(
    project_id: int = Query(..., description="Target Label Studio Project ID"),
    tasks: List[Dict[str, Any]] = Body(..., description="List of dataset task dictionaries")
):
    """Import raw data items into Label Studio project."""
    return LabelStudioService.import_tasks(project_id=project_id, tasks=tasks)

@router.get("/annotations/export", summary="Export Labeled Annotations", description="Export completed data annotations from Label Studio to PostgreSQL/MinIO")
async def export_ls_annotations(
    project_id: int = Query(..., description="Target Label Studio Project ID"),
    export_format: str = Query("JSON", description="Export format specification e.g. JSON, CSV, Pascal VOC")
):
    """Export annotations for downstream model training."""
    return LabelStudioService.export_annotations(project_id=project_id, export_format=export_format)
