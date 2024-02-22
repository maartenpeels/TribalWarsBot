import json
import logging
import random
import re
import time

import requests

from src.core.file_manager import FileManager
from src.core.input import Input

logger = logging.getLogger("WebWrapper")


class WebWrapper:
    last_h = None
    base_headers = {
        "Upgrade-Insecure-Requests": "1",
    }

    def __init__(self, config):
        self.config = config
        self.web = requests.session()
        self.base_url = f"https://{self.config.get('web.server')}.{self.config.get('web.domain')}"

        self.base_headers.update({
            "User-Agent": self.config.get("web.user-agent"),
        })

        self.load_cookies()

    def is_cookie_valid(self):
        response = self.get_screen("overview")
        if "game.php" in response.url:
            return True

        logger.error("Current session cache not valid")
        self.refresh_cookies()
        return False

    def load_cookies(self):
        cookies_data = FileManager.load_json_file("data/cookies.json")

        if cookies_data:
            cookies = json.loads(cookies_data)
        else:
            cookies = self.ask_for_cookies()

        self.web.cookies.update(cookies)
        if not self.is_cookie_valid():
            self.refresh_cookies()

        FileManager.save_json_file("data/cookies.json", json.dumps(cookies))

    def refresh_cookies(self):
        cookies = self.ask_for_cookies()
        self.web.cookies.update(cookies)

        if not self.is_cookie_valid():
            self.refresh_cookies()

        FileManager.save_json_file("data/cookies.json", json.dumps(cookies))

    @staticmethod
    def ask_for_cookies():
        cookie_str = Input.ask_string("Enter cookie string", example="cookie1=value1; cookie2=value2")
        cookies = {}

        for cookie in cookie_str.split(';'):
            cookie = cookie.strip()
            key, value = cookie.split('=')
            cookies[key] = value

        return cookies

    def get_base_headers(self):
        headers = self.base_headers.copy()
        headers.update({
            "Origin": f"{self.base_url}/game.php",
        })

        return headers

    def update_after_request(self, response):
        csrf_token = re.search('<meta content="(.+?)" name="csrf-token"', response.text)
        if csrf_token:
            self.base_headers.update({
                "X-CSRF-Token": csrf_token.group(1),
            })
        elif "X-CSRF-Token" in self.base_headers:
            del self.base_headers["X-CSRF-Token"]

        self.base_headers.update({
            "Referer": response.url,
        })

        new_h = re.search(r'&h=(\w+)', response.text)
        if new_h:
            logger.debug(f"Updating last_h to {new_h.group(1)}")
            self.last_h = new_h.group(1)

    @staticmethod
    def check_captcha(response):
        if 'data-bot-protect="forced"' in response.text:
            logger.warning("Captcha detected, press any key when captcha is solved")
            Input.wait_for_input()
            return True
        return False

    def request(self, method, url, **kwargs):
        logger.debug(f"Requesting {method} {url} with {kwargs}")

        response = self.web.request(method, url, **kwargs)

        if response.status_code != 200:
            logger.error(f"Request failed with status code {response.status_code}")
            return None

        if "session_expired=1" in response.url:
            logger.error("Session expired, please refresh cookies")
            self.refresh_cookies()
            self.request(method, url, **kwargs)

        return response

    def get_url(self, url, headers=None):
        full_url = f"{self.base_url}/{url}"
        base_headers = self.get_base_headers()

        if headers:
            base_headers.update(headers)

        response = self.request("GET", full_url, headers=base_headers)
        self.update_after_request(response)
        was_captcha = self.check_captcha(response)

        if was_captcha:
            return self.get_url(url, headers)

        return response

    def get_screen(self, screen):
        response = self.get_url(f"game.php?screen={screen}")

        sleep_min = self.config.get("bot.delays.request.min")
        sleep_max = self.config.get("bot.delays.request.max")
        sleep = random.uniform(sleep_min, sleep_max)
        logger.debug(f"Sleeping for {sleep} seconds")
        time.sleep(sleep)

        return response
