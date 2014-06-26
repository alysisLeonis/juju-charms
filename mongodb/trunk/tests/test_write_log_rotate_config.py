import mock
import os
import unittest
import tempfile
import sys
sys.path.append('hooks')
import hooks


class TestWriteLogrotateConfigFile(unittest.TestCase):

    def test_success(self):
        logpath = '/tmp/foo/foo.log'
        config_data = {
            'logpath': logpath,
            'logrotate-frequency': 'daily',
            'logrotate-maxsize': '5G',
            'logrotate-rotate': 5,
        }
        fd, temp_fn = tempfile.mkstemp()
        os.close(fd)
        with mock.patch('hooks.juju_log') as mock_juju_log:
            with mock.patch('hooks.open', create=True) as mock_open:
                mock_open.return_value = mock.MagicMock(spec=file)
                hooks.write_logrotate_config(config_data, temp_fn)
                os.unlink(temp_fn)
        mock_juju_log.assert_called_once_with('Writing {}.'.format(temp_fn))
        mock_open.assert_called_once_with(temp_fn, 'w')
        mock_file = mock_open().__enter__()
        call_args = mock_file.write.call_args[0][0]
        self.assertTrue(mock_file.write.called)
        self.assertIn(logpath, call_args)
        self.assertIn('daily', call_args)
        self.assertIn('maxsize 5G', call_args)
        self.assertIn('rotate 5', call_args)
