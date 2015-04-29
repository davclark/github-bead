import github_comments as gh
import json

sensor_group = gh.GitHubComments('glass-bead-labs', 'sensor-group')


# Creates a list of all the data to be stored in a JSON file. 
data = []
for i in range(len(sensor_group.get_all_creators())):
    creator = sensor_group.get_all_creators()[i]
    data.append({'creator': creator, 'comments': sensor_group.get_comments_creator(creator)})


# Creates the JSON file. 
with open ('github_comments.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)