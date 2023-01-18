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