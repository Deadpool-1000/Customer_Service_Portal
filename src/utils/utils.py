import logging

import shortuuid
from flask import has_request_context, request


def generate_new_request_id():
    return shortuuid.ShortUUID().random(10)


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.request_id = request.request_id
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)
