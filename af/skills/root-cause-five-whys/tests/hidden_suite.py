from invoice import total_for
from catalog import skus_for


def test_symptom_california():
    assert total_for(100.00, "CA") == 110.00


def test_same_class_new_york():
    assert total_for(100.00, "NY") == 109.00


def test_same_class_lowercase_feed():
    assert total_for(100.00, "ny") == 109.00


def test_no_regression_catalog():
    assert skus_for("CA") == ["widget-std", "widget-pro"]
