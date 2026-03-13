import contextlib
import io
import json
import unittest

import app


class CommandTests(unittest.TestCase):
    def test_available_commands_are_sorted(self):
        self.assertEqual(app.available_commands(), ["goodbye", "hello"])

    def test_run_command_returns_output(self):
        self.assertEqual(app.run_command("hello"), "Hello, world!")
        self.assertEqual(app.run_command("GOODBYE"), "Goodbye, world!")

    def test_handle_command_reports_unknown_command(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            exit_code = app.handle_command("missing")

        self.assertEqual(exit_code, 1)
        self.assertEqual(stdout.getvalue(), "Unknown command: missing\n")


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.create_app().test_client()

    def test_index_renders_available_commands(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn("BeermannBot", body)
        self.assertIn("data-command=\"hello\"", body)
        self.assertIn("data-command=\"goodbye\"", body)

    def test_health_endpoint(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {"status": "ok", "commands": ["goodbye", "hello"]},
        )

    def test_execute_command_endpoint(self):
        response = self.client.get("/api/commands/hello")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {"command": "hello", "output": "Hello, world!"},
        )

    def test_unknown_command_endpoint(self):
        response = self.client.get("/api/commands/missing")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json(),
            {"error": "Unknown command: missing"},
        )


class MainTests(unittest.TestCase):
    def run_main(self, *args):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            exit_code = app.main(list(args))
        return exit_code, stdout.getvalue()

    def test_main_without_command_prints_message(self):
        exit_code, output = self.run_main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(output, "No command provided\n")

    def test_main_lists_commands_as_text(self):
        exit_code, output = self.run_main("--list")

        self.assertEqual(exit_code, 0)
        self.assertEqual(output, "goodbye\nhello\n")

    def test_main_lists_commands_as_json(self):
        exit_code, output = self.run_main("--list", "--json")

        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(output), {"commands": ["goodbye", "hello"]})

    def test_main_runs_command_as_json(self):
        exit_code, output = self.run_main("hello", "--json")

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            json.loads(output),
            {"command": "hello", "output": "Hello, world!"},
        )

    def test_main_reports_unknown_command_as_json(self):
        exit_code, output = self.run_main("missing", "--json")

        self.assertEqual(exit_code, 1)
        self.assertEqual(json.loads(output), {"error": "Unknown command: missing"})


if __name__ == "__main__":
    unittest.main()
