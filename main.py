from apply_crawler import crawler
import save
import json

print("LIKELION 9TH RECRUITING CRAWLER")
print("created by da-in")

# admin.json
# { "ID" : "admin_id", "PW : "admin_pw" }

with open('admin.json') as json_file:
    admin = json.load(json_file)

id = admin["id"]
pw = admin["pw"]

print("run apply crawler")
result = crawler(id, pw)

print("save as csv file...")
save.save_results(result)

print("complete!")
