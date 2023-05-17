from urllib.request import urlretrieve
from typing import Callable
from requests import get
from os import PathLike
from json import loads


class MailruCloudDispatcherApiRequester:
    def __init__(self, api_version=2, email='mail@mail.ru', lifetime=86400):
        self.api_version, self.email, self.lifetime = api_version, email, lifetime
        self.request_link: str | None = None
        self.request_answer: dict | None = None

        self.generate_request_link()

    def generate_request_link(self):
        self.request_link = f'https://cloud.mail.ru/api/v2/dispatcher' \
                           f'?api={self.api_version}' \
                           f'&email={self.email}' \
                           f'&_={self.lifetime}'

        return self.request_link

    def send_request(self) -> dict[str, any] | None:
        request_answer_obj = get(self.request_link)
        
        self.request_answer = None if request_answer_obj.status_code != 200 else loads(request_answer_obj.text)

        return self.request_answer


class MailruCloudFileStreamLinkGenerator:
    def __init__(self, file_public_link: str, dispatcher_api_requester=MailruCloudDispatcherApiRequester()):
        self.dispatcher_api_requester = dispatcher_api_requester
        self.file_id = file_public_link[len('https://cloud.mail.ru/public/'):]
        self.file_stream_link: str | None = None

    @property
    def file_public_link(self):
        return 'https://cloud.mail.ru/public/' + self.file_id

    def generate_link(self) -> str | None:
        request_result = self.dispatcher_api_requester.send_request()

        self.file_stream_link = None if request_result is None or 'body' not in request_result else (
            request_result['body']['weblink_get'][0]['url'] + '/' + self.file_id
        )

        return self.file_stream_link

    def download(
            self,
            filename: str | bytes | PathLike[str] | PathLike[bytes] = None,
            reporthook: Callable[[int, int, int], object] = None
    ):
        if self.file_stream_link is None:
            self.generate_link()

        if self.file_stream_link is None:
            return None

        return urlretrieve(self.file_stream_link, filename, reporthook)


__all__ = 'MailruCloudDispatcherApiRequester', 'MailruCloudFileStreamLinkGenerator'
