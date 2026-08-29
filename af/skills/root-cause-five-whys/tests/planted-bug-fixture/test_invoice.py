from invoice import total_for


def test_california_order_totals_110():
    assert total_for(100.00, "CA") == 110.00
