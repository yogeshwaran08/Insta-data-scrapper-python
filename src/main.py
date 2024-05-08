
from utils.ProfileScanner import ScanProfile
import json
import time
import os

user = "topchefcookingstudio"

scanner = ScanProfile(user)
scanner.login()
print("getting follower")
username = scanner.get_followers()
print("saving follower")
scanner.save_followers(username,filename="test.json")

# username_file_path = "data/temp/usernames.json"
# output_path = "data/temp/final_output_1.json"

# with open(username_file_path, 'r') as json_file:
#     username_dict = json.load(json_file)


# if(os.path.isfile(output_path)):
#     with open(output_path, 'r') as json_file:
#         report = json.load(json_file)
# else:
#     report = []

# print("lenght : ",len(report))
# c = 103
# for i in username_dict[c:]:
#     try:
#         temp = scanner.get_from_username(i["username"])
#         report.append(temp)
#         report_data = json.dumps(report, indent=2)
#         with open(output_path, 'w') as json_file:
#             json_file.write(report_data)
#             time.sleep(5)
#         print("counter ",c,end='\r')
#         c += 1
#     except Exception as e:
#         print("\n",e)
#         # input("Press Enter to continue")



