import instaloader
from config.creds import USERNAME, PASSWORD
import os
from utils.ProfileScanner import ScanProfile

user = input("Enter the username : ")
session_name = os.path.join("sessions", "aidens.session")

insta = instaloader.Instaloader()

if insta.context.is_logged_in:
    print("Already logged in.")
    obj = ScanProfile(username=user, instaloader_obj=insta)
    obj.iter_followers()
else:
    try:
        insta.load_session_from_file(user,filename=session_name)
        print("Session file found")
        pass

    except FileNotFoundError:
        print("Session file not found. Logging in...")
        insta.context.login(USERNAME, PASSWORD)
        insta.save_session_to_file(session_name)

    finally:
        obj = ScanProfile(username=user, instaloader_obj=insta)
        obj.iter_followers()