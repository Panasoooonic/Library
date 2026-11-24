import library
import pytest;
from library import (
    Library,
    calculate_fee,
    checkout,
    count_active,
    count_returned,
    generate_loan_id,
    is_admin,
    is_minimum_fee,
    loan_summary,
    log_event,
    return_book,
)



def make_library():
    lib = Library()
    lib.add_book("111", "Dune", 2)
    lib.add_book("222", "Emma", 1)
    lib.add_member("m1", "Ana", "gold")
    lib.add_member("m2", "Ben", "silver")
    lib.add_member("m3", "Cy", "basic")
    return lib


def test_add_book_new_and_existing():
    lib = Library()
    lib.add_book("111", "Dune", 2)
    lib.add_book("111", "Dune", 3)
    assert lib.available("111") == 5


def test_available_unknown_book():
    assert Library().available("999") == 0


def test_average_copies():
    assert make_library().average_copies() == 1.5


def test_generate_loan_id_format():
    loan_id = generate_loan_id()
    assert loan_id.startswith("LN-")
    assert len(loan_id) == 9


def test_is_admin_matches_configured_password(monkeypatch):
    monkeypatch.setattr(library, "ADMIN_PASSWORD", "test-secret")
    assert is_admin("test-secret") is True
    assert is_admin("wrong") is False


def test_is_admin_rejects_everything_when_not_configured(monkeypatch):
    monkeypatch.setattr(library, "ADMIN_PASSWORD", "")
    assert is_admin("") is False

def test_average_copies_empty_library_returns_zero():
    assert Library().average_copies() == 0.0


def test_add_book_rejects_negative_copies():
    with pytest.raises(ValueError):
        Library().add_book("111", "Dune", -5)

def test_log_event_returns_history():
    assert "opened" in log_event("opened")


def test_is_minimum_fee():
    assert is_minimum_fee(0.5) is True
    assert is_minimum_fee(1) is False


def test_fee_gold_late_long_loan():
    assert calculate_fee("gold", 21, 4, False, False, False) == 2.0


def test_fee_silver_late_short_loan():
    assert calculate_fee("silver", 7, 4, False, False, False) == 5.0


def test_fee_basic_with_extras():
    assert calculate_fee("basic", 7, 2, True, False, False) == 14


def test_fee_express_insured():
    assert calculate_fee("gold", 7, 0, False, True, True) == 12


def test_checkout_and_return():
    lib = make_library()
    loan = checkout(lib, "111", "m1", 14, False, False, "", "")
    assert loan["status"] == "checked_out"
    assert lib.available("111") == 1
    assert count_active(lib) == 1
    assert return_book(lib, loan["id"]) is True
    assert count_returned(lib) == 1
    assert lib.available("111") == 2


def test_checkout_unknown_member():
    lib = make_library()
    assert checkout(lib, "111", "zzz", 14, False, False, "", "") is None


def test_checkout_no_copies_left():
    lib = make_library()
    checkout(lib, "222", "m1", 14, False, False, "", "")
    assert checkout(lib, "222", "m2", 14, False, False, "", "") is None


def test_return_unknown_loan():
    assert return_book(make_library(), "LN-000000") is False


def test_loan_summary():
    loan = {"isbn": "111", "status": "checked_out"}
    assert loan_summary(loan) == "111 checked_out"
