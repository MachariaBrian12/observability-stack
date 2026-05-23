def test_order_id_format():
    assert f"ORD-{1:03d}" == "ORD-001"

def test_order_range():
    orders = [f"ORD-{i:03d}" for i in range(1, 11)]
    assert len(orders) == 10
    assert orders[-1] == "ORD-010"

def test_loki_payload():
    import time
    payload = {"streams": [{"stream": {"app": "my-devops-app"}, "values": [[str(int(time.time()*1e9)), "test"]]}]}
    assert "streams" in payload
