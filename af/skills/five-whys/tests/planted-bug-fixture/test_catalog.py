from catalog import skus_for


def test_catalog_lists_california_skus():
    assert skus_for("CA") == ["widget-std", "widget-pro"]
