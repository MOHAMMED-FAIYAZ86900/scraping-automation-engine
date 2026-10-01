from scraper.proxy_manager import ProxyManager

def test_proxy_rotation():
    manager = ProxyManager(["http://a:1", "http://b:2"])
    assert manager.next() == "http://a:1"
    assert manager.next() == "http://b:2"
    assert manager.next() == "http://a:1"
