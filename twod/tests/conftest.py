"""Fixtures for twod."""

import pytest


### CONFIG FIXTURES ###

@pytest.fixture
def empty_config(tmpdir):
    """Invalid configuration."""
    f = tmpdir.join("twodrc")
    f.write("setting =")
    return tmpdir


@pytest.fixture
def valid_config(tmpdir):
    """Valid configuration."""
    f = tmpdir.join("twodrc")
    f.write("""
[general]
user     = username@example.com
token = token
host_url = https://api.twodns.de/hosts/example.dd-dns.de
interval = 9000
timeout = 9000

[ip_service]
mode     = random
ip_urls  = https://icanhazip.com https://ipinfo.io/ip

[logging]
level    = WARN
""")
    return tmpdir


@pytest.fixture
def valid_config_mode_rr(tmpdir):
    """Valid configuration."""
    f = tmpdir.join("twodrc")
    f.write("""
[general]
user     = username@example.com
token = token
host_url = https://api.twodns.de/hosts/example.dd-dns.de
interval = 9000
timeout = 9000

[ip_service]
mode     = round_robin
ip_urls  = https://nr_one https://nr_two https://nr_three

[logging]
level    = WARN
""")
    return tmpdir


@pytest.fixture
def invalid_host_config(tmpdir):
    """Invalid configuration."""
    f = tmpdir.join("twodrc")
    f.write("""
[general]
user     = username@example.com
token = token
host_url = https://127.0.0.1:57357
interval = 9001
timeout = 9000

[ip_service]
mode     = random
ip_urls  = https://127.0.0.2:57357

[logging]
level    = WARN
""")
    return tmpdir


@pytest.fixture
def invalid_url_config(tmpdir):
    """Invalid configuration."""
    f = tmpdir.join("twodrc")
    f.write("""
[general]
user     = username@example.com
token = token
host_url = invalid_url
interval = 9001
timeout = 9000

[ip_service]
mode     = random
ip_urls  = invalid_url

[logging]
level    = WARN
""")
    return tmpdir


@pytest.fixture
def invalid_mode_config(tmpdir):
    """Invalid configuration."""
    f = tmpdir.join("twodrc")
    f.write("""
[general]
user     = username@example.com
token = token
host_url = https://127.0.0.1:57357
interval = 9001
timeout = 9000

[ip_service]
mode     = invalid_mode
ip_urls  = https://127.0.0.2:57357

[logging]
level    = WARN
""")
    return tmpdir


@pytest.fixture
def missing_username_config(tmpdir):
    """Valid configuration."""
    f = tmpdir.join("twodrc")
    f.write("""
[general]
token = token
host_url = https://api.twodns.de/hosts/example.dd-dns.de
interval = 9000
timeout = 9000

[ip_service]
mode     = random
ip_urls  = https://icanhazip.com https://ipinfo.io/ip

[logging]
level    = WARN
""")
    return tmpdir


@pytest.fixture
def missing_section_config(tmpdir):
    """Valid configuration."""
    f = tmpdir.join("twodrc")
    f.write("""
[general]
user     = username@example.com
token = token
host_url = https://api.twodns.de/hosts/example.dd-dns.de
interval = 9000
timeout = 9000

[logging]
level    = WARN
""")
    return tmpdir


@pytest.fixture
def valid_config_path(valid_config):
    """Path to valid config."""
    pathstring = ('{dir}/{base}/twodrc'.format(dir=valid_config.dirname,
                                               base=valid_config.basename))
    return pathstring


@pytest.fixture
def valid_config_mode_rr_path(valid_config_mode_rr):
    """Path to valid config with mode set to ``round_robin``."""
    pathstring = ('{dir}/{base}/twodrc'.format(
        dir=valid_config_mode_rr.dirname, base=valid_config_mode_rr.basename))
    return pathstring


@pytest.fixture
def invalid_host_config_path(invalid_host_config):
    """Path to valid config with invalid host entry."""
    pathstring = ('{dir}/{base}/twodrc'.format(
        dir=invalid_host_config.dirname, base=invalid_host_config.basename))
    return pathstring


@pytest.fixture
def invalid_url_config_path(invalid_url_config):
    """Path to valid config with invalid url entry."""
    pathstring = ('{dir}/{base}/twodrc'.format(
        dir=invalid_url_config.dirname, base=invalid_url_config.basename))
    return pathstring


@pytest.fixture
def invalid_mode_config_path(invalid_mode_config):
    """Path to valid config with invalid mode entry."""
    pathstring = ('{dir}/{base}/twodrc'.format(
        dir=invalid_mode_config.dirname, base=invalid_mode_config.basename))
    return pathstring


@pytest.fixture
def missing_username_config_path(missing_username_config):
    """Path to config with missing username."""
    pathstring = ('{dir}/{base}/twodrc'.format(
        dir=missing_username_config.dirname,
        base=missing_username_config.basename))
    return pathstring


@pytest.fixture
def missing_section_config_path(missing_section_config):
    """Path to config without ip_service section."""
    pathstring = ('{dir}/{base}/twodrc'.format(
        dir=missing_section_config.dirname,
        base=missing_section_config.basename))
    return pathstring


### DATA FIXTURES ###

@pytest.fixture
def twodns_response():
    """TwoDNS response fixture."""
    response = (u'{"activate_wildcard":false,"ttl":60,'
                '"fqdn":"example.dd-dns.de","ip_address":"127.0.0.1",'
                '"url":"https://api.twodns.de/hosts/example.dd-dns.de"}')
    return response
