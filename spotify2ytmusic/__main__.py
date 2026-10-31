#!/usr/bin/env python3

from . import cli
import sys
import inspect

def list_commands(module):
    # I build the command list from the functions actually sitting in cli
    # instead of keeping a typed list here. A typed list drifts: I add a
    # function to cli, forget this file, and the help text lies. This way
    # the usage message and the check below can only name commands that
    # exist right now.
    # Only functions defined in the module itself count. A function the
    # module merely imported would otherwise show up here as a command
    # it never meant to offer.
    commands = [
        name
        for name, obj in inspect.getmembers(module)
        if inspect.isfunction(obj) and obj.__module__ == module.__name__
    ]
    return commands

available_commands = list_commands(cli)

if len(sys.argv) < 2:
    print(f"usage: spotify2ytmusic [COMMAND] <ARGUMENTS>")
    print("Available commands:", ", ".join(available_commands))
    print("       For example, try 'spotify2ytmusic list_playlists'")
    sys.exit(1)

# I test membership in the function list instead of using hasattr on the
# module. hasattr would also accept names that are not commands at all,
# like a module cli happened to import, and then the call below would try
# to run something that was never a command. The error names the bad
# command because "unknown command" alone does not tell me what I typed.
if sys.argv[1] not in available_commands:
    print(
        f"ERROR: Unknown command '{sys.argv[1]}', see https://github.com/linsomniac/spotify_to_ytmusic"
    )
    print("Available commands: ", ", ".join(available_commands))
    sys.exit(1)

fn = getattr(cli, sys.argv[1])
sys.argv = sys.argv[1:]
fn()
