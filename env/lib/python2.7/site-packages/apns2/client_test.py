# coding: utf-8

from . import APNSClient, Notification, Payload, PayloadAlert


def test_ok():
    cli = APNSClient(mode="dev", client_cert="/tmp/test.pem")
    # alert = PayloadAlert(body="body!", title="title!")
    # payload = Payload(alert=alert, badge=5, content_available=True)
    payload = Payload(badge=0)  # for silent push
    n = Notification(payload=payload, priority=5)
    token = "91378cd97a7fb636363a8dd1916cb5ecb4bcb6f2ffc19c1d5424fa500e0a0520"
    response = cli.push(n=n, device_token=token)
    assert response.status_code == 200, response.reason
    assert response.apns_id == "foo"
