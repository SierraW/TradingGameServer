import threading
import executers

callback_done = threading.Event()


def command_listener(doc_snapshot, changes, read_time):
    if len(doc_snapshot) > 0:
        doc = doc_snapshot[0]
        executers.execute(doc.to_dict())
        doc.reference.delete()
    callback_done.set()
