from urllib.parse import urlparse

SUSPICIOUS_TLDS = {'.xyz', '.top', '.click', '.zip', '.work', '.tk', '.ml', '.ga', '.cf'}
SUSPICIOUS_KEYWORDS = {
    'login', 'verify', 'verification', 'secure', 'account', 'update',
    'confirm', 'password', 'signin', 'bank', 'wallet', 'payment'
}
SHORTENERS = {'bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'is.gd', 'ow.ly'}


def analyze_url(url):
    """Rule-based heuristic scanner. It is intentionally not ML or packet analysis."""
    original = url.strip()
    candidate = original if '://' in original else 'http://' + original
    parsed = urlparse(candidate)
    host = (parsed.hostname or '').lower()
    path_query = f'{parsed.path}?{parsed.query}'.lower()
    score = 0
    rules = []

    if parsed.scheme not in {'http', 'https'}:
        score += 3; rules.append('Unsupported or unusual URL scheme')
    if parsed.scheme == 'http':
        score += 2; rules.append('Uses HTTP instead of HTTPS')
    if len(original) > 100:
        score += 2; rules.append('Unusually long URL')
    if '@' in parsed.netloc:
        score += 3; rules.append('Contains @ symbol in network location')
    if host.startswith('xn--') or '.xn--' in host:
        score += 3; rules.append('Contains internationalized/punycode hostname')
    if any(host.endswith(tld) for tld in SUSPICIOUS_TLDS):
        score += 2; rules.append('Uses a commonly abused top-level domain')
    if host in SHORTENERS:
        score += 2; rules.append('Uses a URL shortening service')
    keyword_hits = sorted(k for k in SUSPICIOUS_KEYWORDS if k in host or k in path_query)
    if keyword_hits:
        score += min(3, len(keyword_hits))
        rules.append('Contains suspicious security/account keywords: ' + ', '.join(keyword_hits))
    if host.replace('.', '').isdigit():
        score += 3; rules.append('Uses an IP address instead of a domain name')
    if host.count('-') >= 3:
        score += 2; rules.append('Hostname contains many hyphens')
    if len(parsed.hostname or '') > 50:
        score += 2; rules.append('Unusually long hostname')

    result = 'phishing' if score >= 4 else 'safe'
    return {'result': result, 'score': min(score, 10), 'rules': rules}
