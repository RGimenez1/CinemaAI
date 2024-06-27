from fastapi import APIRouter, Query, HTTPException
from app.core.utils.system_prompts_utils import get_system_prompt, get_tool
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
    # Use the provided version or fallback to the default version from the config
    prompt_version = (
        version if version is not None else int(settings.SYSTEM_PROMPT_VERSION)
    )
    prompt_content = get_system_prompt(prompt_version)

    return {"version": prompt_version, "content": prompt_content}


@router.get("/tools")
async def get_tools(
    version: int = Query(None, description="The version of the tool to fetch")
):
    """
    Endpoint to fetch the tool information based on the provided version.
    If no version is provided, use the default version from the configuration.
    """
    # Use the provided version or fallback to the default version from the config
    tool_version = version if version is not None else int(settings.TOOL_VERSION)
    tool_content = get_tool(tool_version)

    if "error" in tool_content:
        raise HTTPException(status_code=404, detail=tool_content["error"])

    return {"version": tool_version, "content": tool_content}


@router.get("/tools")
async def get_tools(
    version: int = Query(None, description="The version of the tool to fetch")
):
    """
    Endpoint to fetch the tool information based on the provided version.
    If no version is provided, use the default version from the configuration.
    """
    try:
        # Use the provided version or fallback to the default version from the config
        tool_version = version if version is not None else int(settings.TOOL_VERSION)
        tool_content = get_tool(tool_version)

        if "error" in tool_content:
            raise HTTPException(status_code=404, detail=tool_content["error"])

        return {"version": tool_version, "content": tool_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
