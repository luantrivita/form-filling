import pytest
from esf.evaluation.split_guard import ensure_split_allowed, TEST_UNLOCK_VALUE


def test_dev_is_allowed(monkeypatch):
    monkeypatch.delenv('ESF_UNLOCK_TEST', raising=False)
    ensure_split_allowed('dev')


def test_test_is_locked_by_default(monkeypatch):
    monkeypatch.delenv('ESF_UNLOCK_TEST', raising=False)
    with pytest.raises(RuntimeError):
        ensure_split_allowed('test')


def test_test_requires_explicit_unlock(monkeypatch):
    monkeypatch.setenv('ESF_UNLOCK_TEST', TEST_UNLOCK_VALUE)
    ensure_split_allowed('test')
