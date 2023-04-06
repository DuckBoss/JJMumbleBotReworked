import pathlib
from unittest.mock import patch

import pytest

from src.constants import DEFAULT_PATH_CONFIG_FILE
from src.exceptions import ConfigReadError
from src.services.init_services.cfg_init_service import ConfigInitService


class TestCfgInitService:
    @pytest.fixture(autouse=True)
    def get_cfg_service(self):
        yield ConfigInitService({})

    @pytest.fixture(autouse=True)
    def valid_cfg_path(self) -> str:
        return "tests/data/config/test_valid_config.toml"

    @pytest.fixture(autouse=True)
    def invalid_cfg_path(self) -> str:
        return "invalid/path/to/config/test_invalid_config.toml"

    @patch("src.settings.MumimoSettings.get_mumimo_config")
    def test_initialize_mumimo_config_valid_cfg_path(self, mock_get_cfg, valid_cfg_path: str, get_cfg_service: ConfigInitService) -> None:
        mock_get_cfg.return_value = None
        _cfg_instance = get_cfg_service.initialize_config(valid_cfg_path)
        assert _cfg_instance._config_file_path == pathlib.Path.cwd() / valid_cfg_path

    @patch("src.settings.MumimoSettings.get_mumimo_config")
    def test_initialize_mumimo_config_invalid_cfg_path(self, mock_get_cfg, invalid_cfg_path: str, get_cfg_service: ConfigInitService) -> None:
        mock_get_cfg.return_value = None
        with pytest.raises(ConfigReadError, match="^Unable to open config file to read"):
            _ = get_cfg_service.initialize_config(invalid_cfg_path)

    @patch("src.settings.MumimoSettings.set_mumimo_config")
    @patch("src.settings.MumimoSettings.get_mumimo_config")
    def test_initialization_mumimo_config_no_cfg_path_uses_default_path(
        self, mock_get_cfg, mock_set_cfg, get_cfg_service: ConfigInitService, caplog
    ) -> None:
        mock_set_cfg.return_value = None
        mock_get_cfg.return_value = None
        _cfg_instance = get_cfg_service.initialize_config(None)
        assert "Mumimo config file path not provided." in caplog.text
        assert _cfg_instance is not None
        assert _cfg_instance._config_file_path == pathlib.Path.cwd() / DEFAULT_PATH_CONFIG_FILE