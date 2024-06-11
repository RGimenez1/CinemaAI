from fastapi import APIRouter, Query, HTTPException
from app.core.utils import get_system_prompt
from app.core.config import settings

router = APIRouter()


@router.get("/system-prompt")
async def get_prompt(
    version: int = Query(None, description="The version of the system prompt to fetch")
):
    """
    Endpoint to fetch the system prompt based on the provided version.
    If no version is provided, use the default version from the configuration.
    """
    try:
        # Use the provided version or fallback to the default version from the config
        prompt_version = (
            version if version is not None else int(settings.SYSTEM_PROMPT_VERSION)
        )
        prompt_content = get_system_prompt(prompt_version)

        return {"version": prompt_version, "content": prompt_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
