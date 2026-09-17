"""
One-time interactive Instagram login, meant to be run on your own machine
(needs a real terminal for the password/2FA prompt — will not work over a
non-interactive SSH/CI shell).

Saves a session cookie to ~/.config/instaloader/session-<username>
(Linux/Mac) or %LOCALAPPDATA%\\Instaloader\\session-<username> (Windows) so
future scrape runs on this machine don't need to log in again.

Run: python3 scripts/login_local.py
"""
import getpass
import instaloader

username = input("Instagram username: ").strip()
password = getpass.getpass("Instagram password: ")

L = instaloader.Instaloader(quiet=True)
try:
    L.login(username, password)
except instaloader.TwoFactorAuthRequiredException:
    code = input("2FA code: ").strip()
    L.two_factor_login(code)

L.save_session_to_file()
print(f"Logged in and saved session for {username}. "
      f"You can now run scrape_accounts.py with IG_LOGIN_USER={username}")
