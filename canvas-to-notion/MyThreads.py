from threading import Thread

class ErrorHandlingThread(Thread):
    def run(self):
        self.error = None

        try:
            Thread.run(self)
        except Exception as e:
            self.error = e


    def join(self):
        Thread.join(self)

        if self.error:
            raise self.error

class CallBackThread(Thread):
    def __init__(self, target, args, callback):
        super().__init__(target=target, args=args)
        self.callback = callback

    def run(self):
        Thread.run(self)
        self.callback()