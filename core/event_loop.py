class EventLoop:
    def __init__(self):
        self.events = []
        self._event_loop = self.start()

    def add_event(self, event):
        self.events.append(event)

    def clear(self):
        self.events.clear()

    def update_events(self):
        next(self._event_loop)

    def start(self):
        """Updates the state of all DYNAMIC EVENTS"""
        while True:
            active_events = []
            for event in self.events:
                try:
                    next(event)
                # coroutine is exhausted
                except StopIteration:
                    continue
                active_events.append(event)
            self.events = active_events
            yield None


event_loop = EventLoop()
