from utils.validation import esc


def test_esc_blocks_html():
    assert "<script>" not in esc("<script>alert(1)</script>")
    assert esc('<img src=x onerror=alert(1)>') == '&lt;img src=x onerror=alert(1)&gt;'
    assert esc(None) == ""
