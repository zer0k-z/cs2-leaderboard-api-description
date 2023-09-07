import matplotlib.pyplot as plt
import requests
import numpy as np
import scipy
import scipy.optimize as optimize
import json
 
f = open('data.json')
 
friends_data = json.load(f)

total = friends_data["leaderboard_entry_count"]
friends_entries = friends_data["entries"]
friends_data = ([(entry['rating'], 1-entry['rank']/total) for entry in friends_entries])

fig, axs = plt.subplots(2, 1, sharex='all', figsize=(8,8))
url = "https://api.steampowered.com/ICSGOServers_730/GetLeaderboardEntries/v1?format=json&lbname=official_leaderboard_premier_season1"

response = requests.get(url)
player_data = []
if response.status_code == 200:
	count = response.json()['result']['data']
	entries = response.json()['result']['entries']
	player_data = [(entry['score'] >> 15, 1-entry['rank']/count) for entry in entries]
	player_data += friends_data
else:
	print("Failed to get data.")
	exit()

values = np.array([data[0] for data in player_data])
cdf_values = np.array([1-data[1] for data in player_data])
axs[0].scatter(values, cdf_values)
axs[0].plot(values, cdf_values, label='Observed Distribution', color='blue')

# Use curve_fit to estimate the parameters
f = lambda x,mu,sigma: scipy.stats.norm(mu,sigma).sf(x)
mu,sigma = optimize.curve_fit(f,values,cdf_values, p0=(9500, 2500))[0]
x = np.linspace(0, 35000, 1000)
sf_values = scipy.stats.norm(mu, sigma).sf(x)
axs[0].plot(x, sf_values, label='Estimated Normal Distribution', color='red')


pdf_values = scipy.stats.norm(mu, sigma).pdf(x)
axs[1].plot(x, pdf_values, label='Estimated Normal Distribution', color='red')


print("Estimated Mean (mu):", mu)
print("Estimated Standard Deviation (sigma):", sigma)

axs[0].set_yticks(np.arange(0, 1.1, 0.25))
axs[0].set_yticks(np.arange(0, 1.1, 0.05), minor=True)
axs[0].set_title('CS Rating CDF')
axs[0].legend()
axs[0].grid()

axs[1].set_title('CS Rating PDF')
axs[1].set_xticks(np.arange(0, 35000, 5000))
axs[1].grid()

plt.title(f"Estimated Mean (mu): {mu} \nEstimated Standard Deviation (sigma): {sigma}")
plt.tight_layout()
plt.show()