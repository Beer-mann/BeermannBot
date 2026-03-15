import sys

commands = {
    'hello': lambda: print('Hello, world!'),
    'goodbye': lambda: print('Goodbye, world!')
}

def handle_command(command):
    if command in commands:
        commands[command]()
    else:
        print(f'Unknown command: {command}')
        return False
    return True

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ok = handle_command(sys.argv[1])
        sys.exit(0 if ok else 1)
    else:
        print(f'Usage: app.py <command>')
        print(f'Available commands: {", ".join(sorted(commands))}')
        sys.exit(1)
