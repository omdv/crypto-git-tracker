import time
from unittest.runner import TextTestResult


class TimeLoggingTest(TextTestResult):

    def startTest(self, test):
        self._started_at = time.time()
        super().startTest(test)

    def addSuccess(self, test):
        elapsed = time.time() - self._started_at
        name = self.getDescription(test)
        self.stream.write(
            "\n{} ({:.03}s)".format(name, round(elapsed, 5)))
        super().addSuccess(test)
