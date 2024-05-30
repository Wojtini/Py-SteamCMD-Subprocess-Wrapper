import requests_mock

from interactive_steamcmd_wrapper.steam_downloader.downloader_requests import DownloadRequests


class TestDownloadRequester:
    def test_get_content(self) -> None:
        url = "http://test.com"
        content = b"resp"
        requester = DownloadRequests()

        with requests_mock.Mocker() as m:
            m.get(url, content=content)
            assert requester.get_content(url) == content
