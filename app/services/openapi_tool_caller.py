import logging
from typing import Any, Dict
from pydantic import ValidationError
from app.repositories.openapi_repository import OpenAPIRepository


class OpenAPIToolCaller:
    def __init__(self, api_spec: Dict[str, Any]):
        self.api_spec = self.validate_openapi_spec(api_spec)
        self.operation_lookup = self.build_operation_lookup(self.api_spec)
        self.repository = OpenAPIRepository()

    def validate_openapi_spec(self, api_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the provided OpenAPI spec."""
        required_fields = ["openapi", "info", "paths", "servers"]
        for field in required_fields:
            if field not in api_spec:
                raise ValidationError(f"Missing required field: {field}")
        if not api_spec.get("servers"):
            raise ValidationError("No servers defined in the OpenAPI spec")
        return api_spec

    def build_operation_lookup(self, api_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Build a lookup table for operationId to (path, method)."""
        return {
            details["operationId"]: (path, method)
            for path, methods in api_spec["paths"].items()
            for method, details in methods.items()
            if "operationId" in details
        }

    def replace_path_parameters(self, path: str, params: Dict[str, Any]) -> str:
        """Replace path parameters with actual values."""
        for param_name, param_value in params.items():
            path = path.replace(f"{{{param_name}}}", str(param_value))
        return path

    async def call_tool(
        self, operation_id: str, params: Dict[str, Any] = {}, body: Any = None
    ) -> Any:
        """Call an API endpoint based on the operationId defined in the OpenAPI spec."""
        server_url = self.api_spec["servers"][0]["url"]
        if operation_id not in self.operation_lookup:
            raise ValueError(f"Operation {operation_id} not found in the API spec")

        path, method = self.operation_lookup[operation_id]
        path = self.replace_path_parameters(path, params)
        full_url = f"{server_url}{path}"
        headers = (
            {"Content-Type": "application/json"}
            if method in ["post", "put", "patch"]
            else {}
        )

        logging.info(
            f"Calling {operation_id} at {full_url} with params {params} and body {body}"
        )
        return await self.repository.make_request(
            method,
            full_url,
            headers,
            params=params if method == "get" else None,
            body=body if method in ["post", "put", "patch"] else None,
        )
