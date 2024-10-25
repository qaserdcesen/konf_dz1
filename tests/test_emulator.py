import unittest
from emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.emulator = ShellEmulator('config.yaml')

    def test_ls(self):
        # Здесь будет тест для команды ls
        pass

    def test_cd(self):
        # Здесь будет тест для команды cd
        pass

    def test_exit(self):
        # Здесь будет тест для команды exit
        pass

if __name__ == "__main__":
    unittest.main()
