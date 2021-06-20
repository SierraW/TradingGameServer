from database import db_commands_ref
from .commandListener import command_listener


watchers = []


def listen():
    col_watch = db_commands_ref.on_snapshot(command_listener)
    watchers.append(col_watch)


def stop():
    for watcher in watchers:
        watcher.unsubscribe()
