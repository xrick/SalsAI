import importlib
import os

from .services.base_service import BaseService

class ServiceManager:
    def __init__(self, service_directory="libs/services"):
        self.services = {}
        self._discover_services(service_directory)

    def _discover_services(self, service_directory):
        """動態發現並載入所有服務"""
        for service_name in os.listdir(service_directory):
            service_path = os.path.join(service_directory, service_name)
            if os.path.isdir(service_path) and service_name != "__pycache__":
                try:
                    # 動態導入 service.py 模組
                    module_path = f"libs.services.{service_name}.service"
                    service_module = importlib.import_module(module_path)

                    # 在模組中尋找繼承自 BaseService 的類別
                    for attr_name in dir(service_module):
                        attr = getattr(service_module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, BaseService) and attr is not BaseService:
                            self.services[service_name] = attr()
                            print(f"成功載入服務: {service_name}")
                            break
                except (ImportError, AttributeError, FileNotFoundError) as e:
                    print(f"無法載入服務 '{service_name}': {e}")

    def get_service(self, service_name: str) -> BaseService:
        """根據名稱獲取服務實例"""
        return self.services.get(service_name)

    def list_services(self) -> list:
        """返回所有已載入服務的名稱列表"""
        return list(self.services.keys())