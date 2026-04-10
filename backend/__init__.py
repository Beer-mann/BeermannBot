"""Backend MVP module surface for BeermannBot."""

from .contract import build_service_contract
from .models import CommandDescriptor, CommandExecutionResponse
from .service import CommandService

__all__ = [
    "CommandDescriptor",
    "CommandExecutionResponse",
    "CommandService",
    "build_service_contract",
]
