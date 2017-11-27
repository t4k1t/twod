"""Tests for twod's config parsing."""

import pytest
import mock

from twod.twod import Twod


class TestConfig:
    """Test config parsing."""

    @mock.patch('twod.twod._Data')
    def test_config_valid(self, mock_data, capsys, monkeypatch,
                          valid_config_path):
        """Test config parsing."""
        cls = Twod(valid_config_path)
        assert cls.interval == 9000

    @mock.patch('twod.twod._Data')
    def test_config_missing_username(self, mock_data, capsys, monkeypatch,
                                     missing_username_config_path):
        """Test config parsing with missing username."""
        with pytest.raises(SystemExit):
            Twod(missing_username_config_path)
        out, err = capsys.readouterr()
        assert "No option 'user'" in err

    @mock.patch('twod.twod._Data')
    def test_config_missing_section(self, mock_data, capsys, monkeypatch,
                                    missing_section_config_path):
        """Test config parsing with missing section."""
        with pytest.raises(SystemExit):
            Twod(missing_section_config_path)
        out, err = capsys.readouterr()
        assert "No section: 'ip_service'" in err

    @mock.patch('twod.twod._Data')
    def test_config_invalid_mode(self, mock_data, capsys, monkeypatch,
                                 invalid_mode_config_path):
        """Test config parsing with missing section."""
        with pytest.raises(SystemExit):
            Twod(invalid_mode_config_path)
        out, err = capsys.readouterr()
        assert "Invalid mode: 'invalid_mode'" in err

    @mock.patch('twod.twod._Data')
    def test_config_invalid_url(self, mock_data, capsys, monkeypatch,
                                invalid_url_config_path):
        """Test config parsing with missing section."""
        with pytest.raises(SystemExit):
            Twod(invalid_url_config_path)
        out, err = capsys.readouterr()
        assert "Invalid URL: 'invalid_url'" in err

#     @mock.patch('twod.twod._Data')
#     @mock.patch('twod.twod.SafeConfigParser.read', side_effect=Exception)
#     def test_config_unexpected(self, mock_data, capsys, caplog,
#                                valid_config_path):
#         """Test config parsing with unexpected error."""
#         with pytest.raises(SystemExit):
#             Twod(valid_config_path)
#         assert "Unexpected error while reading config" in caplog.text()
