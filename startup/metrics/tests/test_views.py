import pytest

from rest_framework import status


@pytest.mark.django_db()
class TestPrometheus():
    def test_metrics(self, authenticated_client, user):
        r = authenticated_client.get("/metrics")
        assert r.status_code == status.HTTP_200_OK
