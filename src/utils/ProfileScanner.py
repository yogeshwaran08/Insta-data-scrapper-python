import instaloader
import json
import os
import time

class ScanProfile:
    def __init__(self, username, instaloader_obj, csv=False):
        self.username = username
        self.insta = instaloader_obj
        self.followers_data = []
        self.output_path = os.path.join("data", f"insta_data_{str(int(time.time()))}.json")
    
    def _get_followers(self):
        profile = instaloader.Profile.from_username(self.insta.context, self.username)
        return profile.get_followers()
    
    def _save_dict_to_file(self):
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
        followers = self._get_followers()
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
            except Exception as e:
                print("[-] Error occured ",e)
                errors += 1

            counter += 1
            end = time.time()-start
            time_taken += end
        print("\n")

        self._save_dict_to_file()