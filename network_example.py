# Here's how to determine which request a QNetworkReply corresponds to when using QNetworkAccessManager in PySide6:
#
# Capture the QNetworkReply:
# When you make a request using QNetworkAccessManager (e.g., get(), post()), it returns a QNetworkReply object. Store this
# object.
#
# Use QNetworkReply.request():
# The QNetworkReply object has a request() method that returns the QNetworkRequest object associated with the reply.
#
# Identify the Request:
# You can identify the request using different strategies:
#
# Compare QNetworkRequest objects:
# If you have stored the original QNetworkRequest objects, you can compare them to the one obtained from the QNetworkReply
# using ==.
#
# Use custom attributes:
# Before making the request, set a custom attribute on the QNetworkRequest using setAttribute() with a unique identifier.
# Retrieve this attribute from the QNetworkReply using request().attribute().
#
# Use a dictionary:
# Store the QNetworkReply objects as values in a dictionary, with a unique identifier as the key. When the finished
# signal is emitted, you can look up the corresponding request using the identifier.
#
# class NetworkManager(QObject):
#     request_finished = Signal(int, QByteArray)
#
#     def __init__(self):
#         super().__init__()
#         self.nam = QNetworkAccessManager()
#         self.nam.finished.connect(self.handle_finished)
#         self.request_counter = 0
#
#     def make_request(self, url_string):
#         url = QUrl(url_string)
#         request = QNetworkRequest(url)
#         request.setAttribute(QNetworkRequest.Attribute.User, self.request_counter)
#         reply = self.nam.get(request)
#         self.request_counter += 1
#
#     def handle_finished(self, reply):
#         request_id = reply.request().attribute(QNetworkRequest.Attribute.User)
#         data = reply.readAll()
#         self.request_finished.emit(request_id, data)
#         reply.deleteLater()

import sys
from PySide6.QtCore import QUrl, QObject, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtWidgets import QApplication


class NetworkManager(QObject):
    finished = Signal(QNetworkReply)
    error = Signal(QNetworkReply.NetworkError)

    def __init__(self):
        super().__init__()
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.handle_finished)

    def get(self, url):
        request = QNetworkRequest(QUrl(url))
        self.manager.get(request)

    def post(self, url, data):
        request = QNetworkRequest(QUrl(url))
        self.manager.post(request, data)

    def put(self, url, data):
        request = QNetworkRequest(QUrl(url))
        self.manager.put(request, data)

    def delete(self, url):
        request = QNetworkRequest(QUrl(url))
        self.manager.deleteResource(request)

    def handle_finished(self, reply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            self.finished.emit(reply)
        else:
            self.error.emit(reply.error())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    network_manager = NetworkManager()


    # Example GET request
    def handle_get_finished(reply):
        print("GET Response:", reply.readAll().data().decode())
        reply.deleteLater()


    def handle_error(error):
        print("Error: ", error)


    network_manager.finished.connect(handle_get_finished)
    network_manager.error.connect(handle_error)
    network_manager.get("https://httpbin.org/get")


    # Example POST request
    def handle_post_finished(reply):
        print("POST Response:", reply.readAll().data().decode())
        reply.deleteLater()


    network_manager.finished.connect(handle_post_finished)
    network_manager.post("https://httpbin.org/post", b"name=John&age=30")


    # Example PUT request
    def handle_put_finished(reply):
        print("PUT Response:", reply.readAll().data().decode())
        reply.deleteLater()


    network_manager.finished.connect(handle_put_finished)
    network_manager.put("https://httpbin.org/put", b"name=Jane&age=25")


    # Example DELETE request
    def handle_delete_finished(reply):
        print("DELETE Response:", reply.readAll().data().decode())
        reply.deleteLater()


    network_manager.finished.connect(handle_delete_finished)
    network_manager.delete("https://httpbin.org/delete")

    app.exec()