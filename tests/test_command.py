import unittest

import mock

from clint.command import Command, run_command

class ErrorCommand(Command):
    def __init__(self, message=None, status=1):
        print 'message:', message, 'status:', status

        self.message = message
        self.status = status

    def run(self):
        raise self.CommandError(self.message, self.status)

class CommandTestCase(unittest.TestCase):
    @mock.patch('sys.exit')
    @mock.patch('sys.stderr')
    def test_command_error_no_args(self, stderr_mock, exit_mock):
        run_command('__main__', ErrorCommand)

        exit_mock.assert_called()
        stderr_mock.write.assert_not_called()

    @mock.patch('sys.exit')
    @mock.patch('sys.stderr')
    def test_command_error_one_arg(self, stderr_mock, exit_mock):
        run_command('__main__', ErrorCommand, 'message')

        exit_mock.assert_called_with(1)
        stderr_mock.write.assert_called_with('message\n')

    @mock.patch('sys.exit')
    @mock.patch('sys.stderr')
    def test_command_error_two_args(self, stderr_mock, exit_mock):
        run_command('__main__', ErrorCommand, 'message', 10)

        exit_mock.assert_called_with(10)
        stderr_mock.write.assert_called_with('message\n')

    @mock.patch('sys.exit')
    @mock.patch('sys.stderr')
    def test_command_error_status_only(self, stderr_mock, exit_mock):
        run_command('__main__', ErrorCommand, status=10)

        exit_mock.assert_called_with(10)
        stderr_mock.write.assert_not_called()

    def test_command_error_more_than_two_args(self):
        self.assertRaises(TypeError, Command.CommandError, 1, 2, 3)
