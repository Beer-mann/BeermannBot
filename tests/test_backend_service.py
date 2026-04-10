from backend.contract import CONTRACT_VERSION, SERVICE_NAME, build_service_contract
from backend.service import CommandService


def test_command_service_lists_known_commands():
    service = CommandService()

    names = [spec.name for spec in service.list_commands()]

    assert names == sorted(names)
    assert "hello" in names
    assert "help" in names


def test_command_service_execute_returns_structured_response():
    service = CommandService()

    result = service.execute("hello")

    assert result.command == "hello"
    assert result.ok is True
    assert result.output == "Hello, world!\n"
    assert result.exit_code == 0


def test_build_service_contract_exposes_mvp_contract_metadata():
    contract = build_service_contract()

    assert contract["service"] == SERVICE_NAME
    assert contract["contract_version"] == CONTRACT_VERSION
    assert any(endpoint["path"] == "/run" for endpoint in contract["endpoints"])
