from utils.phishing import analyze_url


def test_safe_url():
    result = analyze_url('https://www.example.com')
    assert result['result'] == 'safe'


def test_suspicious_url():
    result = analyze_url('http://192.168.1.10/login/verify-account')
    assert result['result'] == 'phishing'
    assert result['score'] >= 4
