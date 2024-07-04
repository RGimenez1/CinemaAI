from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.services.openapi_tool_caller import OpenAPIToolCaller

router = APIRouter()


class ToolCallRequest(BaseModel):
    openapi_spec: Dict[str, Any]
    operation_id: str
    params: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None


@router.post("/call-tool")
async def call_tool_endpoint(request: ToolCallRequest):
    try:
        tool_caller = OpenAPIToolCaller(request.openapi_spec)
        result = await tool_caller.call_tool(
            operation_id=request.operation_id,
            params=request.params or {},
            body=request.body or None,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
