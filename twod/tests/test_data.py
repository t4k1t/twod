"""Tests for twod's main function."""

import mock
from requests import exceptions

from twod.twod import Twod, _Data


class TestData:
    """Test main function."""

    @mock.patch('twod.twod.Session.get')
    def test_get_rec_ip(self, mock_get, capsys, valid_config_path):
        """Test retrieval of recorded IP."""
        MyMock = mock.Mock(text=u'{"ip_address": "127.0.0.2"}')
        mock_get.return_value = MyMock
        cls = Twod(valid_config_path)
        data = _Data(cls.conf)

        assert cls.interval == 9000
        assert data.rec_ip == '127.0.0.2'

    def test_get_rec_ip_invalid_host(self, capsys, caplog,
                                     invalid_host_config_path):
        """Test config parsing with invalid host."""
        cls = Twod(invalid_host_config_path)
        data = _Data(cls.conf)

        assert data._get_rec_ip() is False
        assert cls.interval == 9001
        assert "error while fetching ip from twodns" in (
            caplog.text.lower())

    @mock.patch('twod.twod.Session.get')
    def test_get_ext_ip(self, mock_get, capsys, caplog,
                        valid_config_path):
        """Test retrieval of external IP."""
        MyMock = mock.Mock(text=u'{"ip_address": "127.0.0.2"}')
        MyMock2 = mock.Mock(text="127.0.0.3")
        mock_get.return_value = MyMock
        cls = Twod(valid_config_path)
        data = _Data(cls.conf)

        assert cls.interval == 9000
        assert data.rec_ip == '127.0.0.2'

        mock_get.return_value = MyMock2
        assert data._get_ext_ip() == '127.0.0.3'

    def test_get_ext_ip_invalid_host(self, capsys, caplog,
                                     invalid_host_config_path):
        """Test config parsing with invalid IP service URLs."""
        MyMock = mock.Mock(text=u'{"ip_address": "127.0.0.2"}')
        patcher = mock.patch('twod.twod.Session.get')
        my_mock = patcher.start()
        my_mock.return_value = MyMock
        cls = Twod(invalid_host_config_path)
        data = _Data(cls.conf)
        assert data.rec_ip == "127.0.0.2"

        patcher.stop()
        assert data._get_ext_ip() is False
        assert "error while fetching external ip" in (
            caplog.text.lower())

    @mock.patch('twod.twod.Session.get')
    def test_get_ext_ip_rr(self, mock_get, capsys, caplog,
                           valid_config_mode_rr_path):
        """Test round robin URL selection mode."""
        MyMock = mock.Mock(text=u'{"ip_address": "127.0.0.2"}')
        mock_get.return_value = MyMock
        cls = Twod(valid_config_mode_rr_path)
        data = _Data(cls.conf)

        # test round robin service URL selection
        assert data._get_service_url() == 'https://nr_one'
        assert data._get_service_url() == 'https://nr_two'
        assert data._get_service_url() == 'https://nr_three'
        assert data._get_service_url() == 'https://nr_one'
        assert data._get_service_url() == 'https://nr_two'
        assert data._get_service_url() == 'https://nr_three'
        assert data._get_service_url() == 'https://nr_one'

    @mock.patch('twod.twod.Session.get')
    def test_check(self, mock_get, capsys, caplog,
                   valid_config_path):
        """Test IP comparison."""
        MyMock = mock.Mock(text=u'{"ip_address": "127.0.0.2"}')
        MyMock2 = mock.Mock(text="127.0.0.3")
        MyMock3 = mock.Mock(text="127.0.0.2")
        mock_get.return_value = MyMock
        cls = Twod(valid_config_path)
        data = _Data(cls.conf)

        assert cls.interval == 9000
        assert data.rec_ip == '127.0.0.2'

        # external and recorded IP are different, return external IP
        mock_get.return_value = MyMock2
        assert data._get_ext_ip() == '127.0.0.3'
        assert data._check_ip() == '127.0.0.3'

        # external and recorded IP are the same, return False
        mock_get.return_value = MyMock3
        assert data._check_ip() is False

    @mock.patch('twod.twod.Session.get')
    @mock.patch('twod.twod.Session.put')
    def test_update(self, mock_put, mock_get, capsys, caplog,
                    valid_config_path):
        """Test IP update."""
        MyMock = mock.Mock(text=u'{"ip_address": "127.0.0.2"}')
        MyMock2 = mock.Mock(status_code=200)
        mock_get.return_value = MyMock
        mock_put.return_value = MyMock2
        cls = Twod(valid_config_path)
        data = _Data(cls.conf)

        data._update_ip('127.0.0.3')
        assert data.rec_ip == '127.0.0.3'

    @mock.patch('twod.twod.Session.get')
    @mock.patch('twod.twod.Session.put')
    def test_update_fail(self, mock_put, mock_get, capsys, caplog,
                         valid_config_path):
        """Test IP update failure."""
        MyMock = mock.Mock(text=u'{"ip_address": "127.0.0.2"}')

        def http_error(*args, **kwargs):
            raise exceptions.HTTPError("Service Unavailable")

        MyMock2 = mock.Mock(status_code=503, side_effect=http_error)
        mock_get.return_value = MyMock
        mock_put.side_effect = MyMock2
        cls = Twod(valid_config_path)
        data = _Data(cls.conf)

        data._update_ip('127.0.0.3')
        assert data.rec_ip == '127.0.0.2'
        assert "Error while updating IP" in caplog.text
