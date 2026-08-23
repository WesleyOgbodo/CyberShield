import hashlib
import secrets
from datetime import datetime, timedelta, timezone

OTP_EXPIRY_MINUTES = 5


def generate_otp():
    return f'{secrets.randbelow(1_000_000):06d}'


def hash_otp(otp):
    return hashlib.sha256(otp.encode('utf-8')).hexdigest()


def expiry_time():
    return datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=OTP_EXPIRY_MINUTES)


def verify_otp_hash(otp, otp_hash):
    return secrets.compare_digest(hash_otp(otp), otp_hash)
