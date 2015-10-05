"""Tests for the CLI of twod."""

import pytest
import mock

from twod.twod import main
from twod._version import __version__


class TestCLI:

    """Test CLI."""

    def test_cli(self, capsys, monkeypatch):
        """Test CLI."""
        monkeypatch.setattr('sys.argv', ['twod.py', '-h'])
        with pytest.raises(SystemExit):
            main()
        out, err = capsys.readouterr()
        assert "usage:" in out

    def test_config_argument_no_sections(self, capsys, monkeypatch,
                                         empty_config):
        """Test CLI with --config argument and no sections."""
        monkeypatch.setattr('sys.argv', ['twod.py', '-c',
                            '{dir}/{base}/twodrc'.format(
                                dir=empty_config.dirname,
                                base=empty_config.basename)])
        with pytest.raises(SystemExit):
            main()
        out, err = capsys.readouterr()
        assert "File contains no section headers" in err

    def test_invalid_config_path(self, capsys, monkeypatch):
        """Test CLI with --config argument and invalid config path."""
        monkeypatch.setattr('sys.argv', ['twod.py', '-c', 'invalid_path'])
        with pytest.raises(SystemExit):
            main()
        out, err = capsys.readouterr()
        assert "'invalid_path' is not a file" in err

    # Exit with message ``DAEMON`` if daemonisation is attempted.
    @mock.patch('twod.twod.DaemonContext', side_effect=SystemExit("DAEMON"))
    @mock.patch('twod.twod._Data')
    @mock.patch('twod.twod.Session.get')
    # If we reach the ``sleep`` statement we already completed one update
    # cycle so we can exit there.
    @mock.patch('twod.twod.sleep', side_effect=SystemExit("TEST DONE"))
    def test_no_detach(self, mock_sleep, mock_get, mock_data, mock_daemon,
                       capsys, caplog, monkeypatch, valid_config_path):
        """Test --no-detach argument."""
        monkeypatch.setattr('sys.argv', ['twod.py', '-D', '-c',
                            valid_config_path])
        MyMock = mock.Mock(text=u'{"ip_address": "127.0.0.1"}')
        mock_get.return_value = MyMock

        with pytest.raises(SystemExit) as e:
            main()
        assert "TEST DONE" in str(e)

    def test_version(self, capsys, monkeypatch):
        """Test CLI."""
        monkeypatch.setattr('sys.argv', ['twod.py', '-V'])
        with pytest.raises(SystemExit):
            main()
        out, err = capsys.readouterr()
        assert "twod {}".format(__version__) in err
