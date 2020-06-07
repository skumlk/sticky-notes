# Thanks to
# https://stackoverflow.com/questions/16311396/pyqt-prevent-multiple-instances-of-an-application-popping-up-the-same-dialog
#

from PyQt5.Qt import QSharedMemory

class MemoryCondition:

    def __init__(self, key='memory_condition_key'):
        self._shm = QSharedMemory(key)
        if not self._shm.attach():
            if not self._shm.create(1):
                raise RuntimeError('error creating shared memory: %s' %
                                   self._shm.errorString())
        self.condition = False

    def __enter__(self):
        self._shm.lock()
        if self._shm.data()[0] == b'\x00':
            self.condition = True
            self._shm.data()[0] = b'\x01'
        self._shm.unlock()
        return self.condition

    def __exit__(self, exc_type, exc_value, traceback):
        if self.condition:
            self._shm.lock()
            self._shm.data()[0] = b'\x00'
            self._shm.unlock()
