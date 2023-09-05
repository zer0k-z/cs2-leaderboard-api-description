import matplotlib.pyplot as plt
import requests
import numpy as np
import scipy
import scipy.optimize as optimize

fig, axs = plt.subplots(2, 1, sharex='all', figsize=(8,8))
url = "https://api.steampowered.com/ICSGOServers_730/GetLeaderboardEntries/v1?format=json&lbname=official_leaderboard_premier_season1"

response = requests.get(url)
player_data = []
if response.status_code == 200:
	count = response.json()['result']['data']
	entries = response.json()['result']['entries']
	player_data = [(entry['score'] >> 15, 1-entry['rank']/count) for entry in entries]
	player_data += [(18400, 0.98), (14991, 0.91), (13698, 0.85), (13584, 0.84), (13466, 0.83),
				(13282, 0.82), (12861, 0.79), (12709, 0.78), (12321, 0.75), (12112, 0.74), (10642, 0.6),
				(10315, 0.56), (9090, 0.44), (8999, 0.44), (8000, 0.33), (7815, 0.31), (7786, 0.31), (7115, 0.24), (6684, 0.2), (6540, 0.18)]
else:
	print("uh oh")
	exit()
axs[0].scatter([data[0] for data in player_data], [1-data[1] for data in player_data])
major_ticks = np.arange(0, 1.1, 0.25)
minor_ticks = np.arange(0, 1.1, 0.05)
# Example data: an array of values and their CDF values
values = np.array([data[0] for data in player_data])
cdf_values = np.array([1-data[1] for data in player_data])
# Use curve_fit to estimate the parameters
f = lambda x,mu,sigma: scipy.stats.norm(mu,sigma).sf(x)
print(values, cdf_values)
mu,sigma = optimize.curve_fit(f,values,cdf_values, p0=(9000, 2500))[0]
x = np.linspace(0, 35000, 1000)
sf_values = scipy.stats.norm(mu, sigma).sf(x)
axs[0].plot(x, sf_values, label='Estimated Normal Distribution', color='red')


pdf_values = scipy.stats.norm(mu, sigma).pdf(x)
axs[1].plot(x, pdf_values, label='Estimated Normal Distribution', color='red')


print("Estimated Mean (mu):", mu)
print("Estimated Standard Deviation (sigma):", sigma)

axs[0].set_yticks(major_ticks)
axs[0].set_yticks(minor_ticks, minor=True)
axs[0].legend()
axs[0].grid()

plt.tight_layout()
plt.show()