import instaloader
import json
import os
import time
import pickle
# from src.config.creds import USERNAME,PASSWORD
# from ..config.creds import USERNAME,PASSWORD
from instaloader.nodeiterator import NodeIterator
from instaloader.structures import Profile



class ScanProfile:
    def __init__(self, target_username):
        self.username = target_username
        # self.insta = instaloader_obj
        self.followers_data = []
        self.output_path = os.path.join("data", f"insta_data_{str(int(time.time()))}.json")
        self.state_file = os.path.join("data", "state.pkl")
        self.insta = instaloader.Instaloader()
        self.session_name = os.path.join("sessions", "aidens.session")
        # self.login()
        
    def login(self):
        if self.insta.context.is_logged_in:
            print("Already Logged in")
            return True
        else:
            try:
                self.insta.load_session_from_file("iam_.aiden_", filename=self.session_name)
                print("Session file found. Logging in")
                return True
            except FileNotFoundError:
                USERNAME = "iam_.aiden_"
                PASSWORD = "Master@08083"
                self.insta.context.login(USERNAME, PASSWORD)
                # self.insta.save_session_to_file(self.session_name)
                print("Loggin in with Username & password")
                return True
    
    def get_from_username(self, username):
        person = instaloader.Profile.from_username(self.insta.context, username)
        return {
                    "name" : person.username,
                    "biography" : person.biography,
                    "is_bussiness_account" : person.is_business_account,
                    "business_category" : person.business_category_name,
                    "external_url" : person.external_url,
                    "is_verified" : person.is_verified,
                    "profile_hashtags" : person.biography_hashtags,
                    "profile_mentions" : person.biography_mentions,
                    "url" : f"https://instagram.com/{person.username}",
                    "email" : person.get_email,
                    "phone_number" : person.get_phone,
                    "address" : person.bussiness_address,
                }


    def _save_state(self, counter, followers_data, time_taken):
        state_data = {
            "counter": counter,
            "followers_data": followers_data,
            "time_taken": time_taken,
        }
        with open(self.state_file, 'wb') as state_file:
            pickle.dump(state_data, state_file)
    
    def _load_state(self):
        if os.path.isfile(self.state_file):
            with open(self.state_file, 'rb') as state_file:
                state_data = pickle.load(state_file)
            return state_data
        return None
    
    def get_followers(self):
        profile = instaloader.Profile.from_username(self.insta.context, self.username)
        return profile.get_followers()

    def save_followers(self, followers : NodeIterator[Profile], filename):
        usernames = []
        for i in followers:
            print(i.username)
            usernames.append({"username" : i.username})
            report_data = json.dumps(usernames, indent=2)
            with open(filename, 'w') as json_file:
                json_file.write(report_data)
            time.sleep(10)
        
    def save_dict_to_file(self):
        report_data = json.dumps(self.followers_data, indent=2)
        if (not os.path.isdir("data")):
            os.mkdir("data")
        with open(self.output_path, 'w') as json_file:
            json_file.write(report_data)
    
    def _calculate_percentage(self, complete, total):
        return int((complete/total)*10)
    
    def _calculate_avg_time(self, iterations, time_taken):
        if(iterations != 0):
            return time_taken/iterations
        else:
            return 0
    
    def _manage_ui(self, len_profile : int, complete : int, time_taken : int):
        # print(f"Total profile to scrape : {len_profile}")
        no_done = self._calculate_percentage(complete, len_profile)
        print(f"Progress : [{'=' * no_done}{' ' * (10 - no_done)}] {complete}/{len_profile} \
              Avg : {self._calculate_avg_time(complete, time_taken)}",end="\r")
    
    #function only needs to called from outside
    def iter_followers(self):
        state = self._load_state()
        followers = self.get_followers()
        followers.freeze()
        if(state):
            counter = state["counter"]
            self.followers_data = state["followers_data"]
            time_taken = state["time_taken"]
        else:
            counter = 0
            time_taken = 0

        errors = 0
        for person in followers:
            self._manage_ui(len_profile=followers.count, complete=counter, time_taken=time_taken)
            start = time.time()
            try:
                userData = {
                    "name" : person.username,
                    "biography" : person.biography,
                    "is_bussiness_account" : person.is_business_account,
                    "business_category" : person.business_category_name,
                    "external_url" : person.external_url,
                    "is_verified" : person.is_verified,
                    "profile_hashtags" : person.biography_hashtags,
                    "profile_mentions" : person.biography_mentions,
                    "url" : f"https://instagram.com/{person.username}",
                    "email" : person.get_email,
                    "phone_number" : person.get_phone,
                    "address" : person.bussiness_address,
                }
                self.followers_data.append(userData)
            except instaloader.exceptions.AbortDownloadException as e:
                print("logged out")
                pass
            except Exception as e:
                print("[-] Error occured ",e)
                errors += 1

            self._save_state(counter, self.followers_data, time_taken)
            counter += 1
            end = time.time()-start
            time_taken += end
            # print("Sleeping")
            time.sleep(55)
        print("\n")

        self._save_dict_to_file()