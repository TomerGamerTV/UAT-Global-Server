import cv2
import os
from collections import OrderedDict

from bot.base.common import ImageMatchConfig


def env_bytes(name: str, default: int) -> int:
    try:
        v = os.getenv(name)
        if not v:
            return default
        vs = v.strip().lower()
        if vs.endswith("gb"):
            return int(float(vs[:-2]) * (1024 ** 3))
        if vs.endswith("mb"):
            return int(float(vs[:-2]) * (1024 ** 2))
        return int(v)
    except Exception:
        return default


class TemplateCache:
    def __init__(self, max_bytes: int):
        self.store = OrderedDict()
        self.max_bytes = int(max_bytes)
        self.total = 0

    @staticmethod
    def make_key(resource_path: str, template_name: str) -> str:
        return f"{resource_path}::{template_name.lower()}"

    def get(self, resource_path: str, template_name: str):
        key = self.make_key(resource_path, template_name)
        v = self.store.get(key)
        if v is not None:
            self.store.move_to_end(key)
            return v[0]
        return None

    def set(self, resource_path: str, template_name: str, img):
        key = self.make_key(resource_path, template_name)
        try:
            h, w = img.shape[:2]
            size = int(h) * int(w)
        except Exception:
            size = 0
        if key in self.store:
            _, old_size = self.store.pop(key)
            self.total -= int(old_size)
        self.store[key] = (img, size)
        self.total += int(size)
        self.store.move_to_end(key)
        self.evict()

    def evict(self):
        while self.total > self.max_bytes and self.store:
            _, (_, sz) = self.store.popitem(last=False)
            self.total -= int(sz)

    def clear(self):
        self.store.clear()
        self.total = 0


TEMPLATE_CACHE = TemplateCache(
    env_bytes("UAT_TEMPLATE_CACHE_LIMIT_BYTES", 2 * 1024 * 1024 * 1024)
)


class Template:
    template_name: str
    template_image: object
    resource_path: str
    image_match_config: ImageMatchConfig

    def __init__(self,
                 template_name: str,
                 resource_path: str,
                 image_match_config: ImageMatchConfig = ImageMatchConfig()):
        self.resource_path = resource_path
        self.template_name = template_name
        cached = TEMPLATE_CACHE.get(self.resource_path, template_name)
        if cached is None:
            img = cv2.imread("resource" + self.resource_path + "/" + template_name.lower() + ".png", 0)
            TEMPLATE_CACHE.set(self.resource_path, template_name, img)
            self.template_image = img
        else:
            self.template_image = cached
        self.image_match_config = image_match_config


class UI:
    ui_name = None
    check_exist_template_list: list[Template] = None
    check_non_exist_template_list: list[Template] = None

    def __init__(self, ui_name, check_exist_template_list: list[Template],
                 check_non_exist_template_list: list[Template]):
        self.ui_name = ui_name
        self.check_exist_template_list = check_exist_template_list
        self.check_non_exist_template_list = check_non_exist_template_list


def purge_template_cache():
    TEMPLATE_CACHE.clear()


NOT_FOUND_UI = UI("NOT_FOUND_UI", [], [])
