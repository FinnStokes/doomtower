class Event:
    def __init__(self):
        self.handlers = dict()

    def register(self, event, handler):
        if not event in self.handlers:
            self.handlers[event] = set()
        self.handlers[event].add(handler)
        return self

    def deregister(self, event, handler):
        if event in self.handlers:
            try:
                self.handlers.remove(handler)
            except:
                raise ValueError("Handler is not handling this event, so cannot deregister it.")
        else:
            raise ValueError("Event is not registered, so cannot deregister it.")
        return self

    def notify(self, event, *args, **kargs):
        if event in self.handlers:
            for handler in self.handlers[event]:
                handler(*args, **kargs)
