import os
from typing import Any
from datetime import date, datetime, time
from django.conf import settings
import logging
import re

from django.core.exceptions import PermissionDenied
from rest_framework import response

request_logger = logging.getLogger("request_logger")
message_logger = logging.getLogger("message_logger")


class RequestLoggingMiddleware:

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request) -> Any:

        request_logger.info(f"{datetime.now()}-User:{request.user}-Path:{request.path}")
        response = self.get_response(request)

        return response


class RestrictAccessByTimeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request) -> Any:

        now = datetime.now().time()
        start = time(18, 0)
        end = time(21, 0)

        # if start <= now <= end:
        #     raise PermissionDenied()
        # else:
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request) -> Any:

        log_file_path = settings.BASE_DIR / "chat_messages.log"
        remote_address = request.META.get("REMOTE_ADDR")
        request_path = request.path

        if request_path == "/conversations/1/messages/":

            with open(log_file_path, "r", encoding="utf-8") as file:

                total_index = len([index for index, line in enumerate(file.readline())])

                if total_index > 0:
                    file.seek(0)
                    matches = re.findall(remote_address, file.read())
                    if len(matches) >= 5:
                        file.seek(0)
                        for line in file.readlines():
                            match = re.search(remote_address, line)
                            if match:
                                date_string = (
                                    line.split("|")[-1].split("\n")[0].split(".")[0]
                                )
                                date_format_string = "%H:%M:%S"
                                datetime_object = datetime.strptime(
                                    date_string, date_format_string
                                )
                                minute_difference = datetime.now() - datetime_object
                                total_minute = (
                                    minute_difference.total_seconds() % 3600
                                ) // 60

                                if total_minute < 1:
                                    raise PermissionDenied()
                                else:
                                    file.seek(0)
                                    new_lines = []
                                    for line in file.readlines():
                                        if not re.search(remote_address, line):
                                            new_lines.append(line)

                                    with open(log_file_path, "w") as f:
                                        f.writelines(new_lines)

        message_logger.info(f"{request.path}|{remote_address}|{datetime.now().time()}")
        response = self.get_response(request)
        return response


class RolepermissionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not (request.user.is_admin or request.user.is_superuser or request.is_staff):
            if request.path == "/admin/":
                raise PermissionDenied()

        response = self.get_response(request)

        return response
