from typing import Any

CONTRACT_VERSION = "2026-04-09-mvp"
SERVICE_NAME = "beermannbot-backend"


def build_service_contract() -> dict[str, Any]:
    """Draft canonical API contract for BeermannBot backend MVP."""
    return {
        "service": SERVICE_NAME,
        "contract_version": CONTRACT_VERSION,
        "endpoints": [
            {
                "name": "health",
                "method": "GET",
                "path": "/health",
                "response": {"status": "ok"},
            },
            {
                "name": "list_commands",
                "method": "GET",
                "path": "/commands",
                "response_shape": {
                    "commands": ["hello", "goodbye", "help"],
                    "items": [{"name": "hello", "description": "Print a greeting message"}],
                },
            },
            {
                "name": "execute_command",
                "method": "POST",
                "path": "/run",
                "request_shape": {"command": "hello"},
                "response_shape": {
                    "command": "hello",
                    "ok": True,
                    "output": "Hello, world!\n",
                    "exit_code": 0,
                    "history": [
                        {
                            "command": "hello",
                            "ok": True,
                            "output": "Hello, world!\n",
                            "timestamp": "2026-04-09T00:00:00+00:00",
                        }
                    ],
                },
                "error_status_codes": [400, 404],
            },
            {
                "name": "history",
                "method": "GET",
                "path": "/history",
                "response_shape": {"items": []},
            },
            {
                "name": "clear_history",
                "method": "DELETE",
                "path": "/history/clear",
                "response_shape": {"status": "ok", "message": "History cleared"},
            },
        ],
    }
