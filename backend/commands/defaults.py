from . import handlers
from .models import CommandSpec
from .registry import CommandRegistry


def build_default_registry() -> CommandRegistry:
    registry = CommandRegistry()
    registry.register(CommandSpec("goodbye", "Print a farewell message", handlers.cmd_goodbye))
    registry.register(CommandSpec("hello", "Print a greeting message", handlers.cmd_hello))
    registry.register(CommandSpec("ping", "Respond with pong", handlers.cmd_ping))
    registry.register(CommandSpec("status", "Show bot status", handlers.cmd_status))
    registry.register(CommandSpec("time", "Show the current UTC time", handlers.cmd_time))
    registry.register(CommandSpec("version", "Show version information", handlers.cmd_version))
    registry.register(
        CommandSpec(
            "help",
            "List all available commands",
            handlers.make_help_handler(registry),
        )
    )
    return registry


_DEFAULT_REGISTRY: CommandRegistry | None = None


def get_default_registry() -> CommandRegistry:
    global _DEFAULT_REGISTRY
    if _DEFAULT_REGISTRY is None:
        _DEFAULT_REGISTRY = build_default_registry()
    return _DEFAULT_REGISTRY
