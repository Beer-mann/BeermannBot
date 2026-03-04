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

if __name__ == '__main__':
    if len(sys.argv) > 1:
        handle_command(sys.argv[1])
    else:
        print('No command provided')

# Command-Registry + unknown-command fallback vorhanden
