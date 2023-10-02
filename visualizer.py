import matplotlib.pyplot as plt
import requests
import numpy as np
import scipy
import scipy.optimize as optimize
import json
import datetime
import typing as T
import os
import detailData_pb2

MAPS = ['Ancient', 'Nuke', 'Overpass', 'Vertigo', 'Mirage', 'Inferno', 'Anubis']

REGIONS_SUFFIXES = ['_northamerica', '_southamerica', '_europe', '_asia', '_australia', '_africa', '_china']

REGIONS_TITLES = ["North America", "South America", "Europe", "Asia", "Australia", "Africa", "China"]

def get_region_name(value: int):
    match value:
        case 1:    
            return "North America"
        case 2:    
            return "South America"
        case 3:    
            return "Europe"
        case 4:    
            return "Asia"
        case 5:    
            return "Australia"
        case 7:    
            return "Africa"
        case 9:    
            return "China"
        case _:    
            return f"Unknown {value}"

def get_map_stats(value: int):
    result = {}
    # Convert to binary and pad with zeros for 7 maps (4 bits each)
    binary_str = bin(value)[2:].zfill(28)
    
    # Split into 4-bit segments
    segments = [binary_str[i:i+4] for i in range(0, 28, 4)]
    
    # Convert each 4-bit segment back to an integer
    map_stats = [int(segment, 2) for segment in segments]
    for i, map in enumerate(MAPS):
        result[map] = map_stats[i]
    return result

def generate_estimation(player_data: T.List[int]):
    values = np.array([data[0] for data in player_data])
    cdf_values = np.array([1-data[1] for data in player_data])

    _, axs = plt.subplots(2, 1, sharex='all', figsize=(12,8))
    axs[0].scatter(values, cdf_values)
    axs[0].plot(values, cdf_values, label='Observed Distribution', color='blue')

    # Use curve_fit to estimate the parameters
    f = lambda x,mu,sigma: scipy.stats.norm(mu,sigma).sf(x)
    mu,sigma = optimize.curve_fit(f,values,cdf_values, p0=(9500, 2500))[0]
    x = np.linspace(1000, 35000, 1000)
    sf_values = scipy.stats.norm(mu, sigma).sf(x)
    axs[0].plot(x, sf_values, label='Estimated Normal Distribution', color='red')

    pdf_values = scipy.stats.norm(mu, sigma).pdf(x)
    axs[1].plot(x, pdf_values,label='Estimated Normal Distribution', color='red')
    samples = np.random.normal(mu, sigma, 600000)
    samples = np.maximum(samples, 1000)
    samples = np.minimum(samples, 20000)
    axs[1].hist(samples, bins=20, density=True, alpha=0.5, color='b', edgecolor='black')

    axs[0].set_yticks(np.arange(0, 1.1, 0.25))
    axs[0].set_yticks(np.arange(0, 1.1, 0.05), minor=True)
    axs[0].set_title('CS Rating CDF')
    axs[0].legend()
    axs[0].grid()

    axs[1].set_title('CS Rating PDF')
    axs[1].set_xticks(np.arange(0, 35000, 5000))
    axs[1].grid()

    plt.suptitle(f"CS Rating Estimated Distribution (Global)\nEstimated Mean (mu): {int(mu)} \nEstimated Standard Deviation (sigma): {int(sigma)}")
    plt.tight_layout()
    plt.savefig(f"estimated_global_dist.png", dpi = 500)

def sanitize_name_md(name):
    # Make names with | not break the table.
    return name.replace('|', r'\|')

def make_markdown_table(region_name, array):

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    markdown = f"# {region_name} Leaderboard ({now})\n"
    markdown += "\n" + str("| ")

    for e in array[0]:
        to_add = " " + str(e) + str(" |")
        markdown += to_add
    markdown += "\n"

    markdown += '|'
    for _ in range(len(array[0])):
        markdown += str("-------------- | ")
    markdown += "\n"

    for entry in array[1:]:
        markdown += str("| ")
        for e in entry:
            to_add = str(e) + str(" | ")
            markdown += to_add
        markdown += "\n"

    return markdown + "\n"

class PlayerData:
    def __init__(self, data):
        # Basic data
        self.name = data['name']
        self.rank = data['rank']
        self.score = data['score'] >> 15
        
        # Data extracted from detailData field
        self.wins = 0
        self.ties = 0
        self.losses = 0
        self.map_details = {}
        self.time_achieved = ""
        self.region = "Unknown"
        
        detail_data = detailData_pb2.ScoreLeaderboardData()
        # Convert the hex string into bytes object.
        detail_data_bytes = bytes.fromhex(data['detailData'])
        # The first byte of the object is the size of the real protobuf data.
        detail_data_size = detail_data_bytes[0] + 1
        detail_data.ParseFromString(detail_data_bytes[1:detail_data_size])

        for entry in detail_data.matchentries:
            match entry.tag:
                case 16:
                    self.wins = entry.val
                case 17:
                    self.ties = entry.val
                case 18:
                    self.losses = entry.val
                case 19:
                    self.map_details = get_map_stats(entry.val)
                case 20:
                    self.time_achieved = str(datetime.datetime.fromtimestamp(entry.val))
                case 21:
                    self.region = get_region_name(entry.val)
                case _:
                    print(f"Unknown field {entry.tag}!")

def create_leaderboard_md(region: str, data: T.List[PlayerData]):
    lines = [['#', 'CS Rating', 'Name', 'Wins', 'Ties', 'Losses', 'Win%', 'Ancient', 'Nuke', 'Overpass', 'Vertigo', 'Mirage', 'Inferno', 'Anubis', 'Region', 'Last Played']]
    for player in data:
        lines.append([player.rank, player.score, sanitize_name_md(player.name), player.wins, player.ties, player.losses, round(player.wins/(player.wins+player.ties+player.losses) * 100, 2),
            player.map_details['Ancient'], player.map_details['Nuke'],player.map_details['Overpass'],player.map_details['Vertigo'],player.map_details['Mirage'],player.map_details['Inferno'],player.map_details['Anubis'],
            player.region, player.time_achieved])
        
    if not os.path.exists("leaderboards"):
        os.makedirs("leaderboards")
    with open(f"leaderboards/{region}.md", "w", encoding="utf-8") as file:
        file.write(make_markdown_table(region, lines))
    

def main():
    # Data from Steam API message with nethook.
    f = open('data.json')

    friends_data = json.load(f)
    total = friends_data["leaderboard_entry_count"]
    friends_entries = friends_data["entries"]
    friends_data = ([(entry['rating'], 1-entry['rank']/total) for entry in friends_entries])

    url = "https://api.steampowered.com/ICSGOServers_730/GetLeaderboardEntries/v1?format=json&lbname=official_leaderboard_premier_season1"

    response = requests.get(url)
    player_data = []

    if response.status_code == 200:
        global_count = response.json()['result']['data']
        global_entries = response.json()['result']['entries']
    else:
        print("Failed to get data.")
        exit()

    '''
        This section estimates the global rank distribution.
    '''

    # Since everyone here are top 1000 out of millions, it isn't actually that useful to estimate the curve with this data.
    # But more is better, I guess.
    player_data = [(entry['score'] >> 15, 1-entry['rank']/global_count) for entry in global_entries]

    # The real useful data
    player_data += friends_data

    generate_estimation(player_data)

    '''
        This section creates all the leaderboard tables, with extra detailed data.
    '''

    global_player_data_detailed = [PlayerData(entry) for entry in global_entries]
    create_leaderboard_md("Global", global_player_data_detailed)
    for i in range(0, len(REGIONS_SUFFIXES)):
        response = requests.get(url+REGIONS_SUFFIXES[i])
        player_data = []

        if response.status_code == 200:
            count = response.json()['result']['data']
            entries = response.json()['result']['entries']
        if count == 0 or len(entries) == 0:
            continue
        player_data_detailed = [PlayerData(entry) for entry in entries]
        create_leaderboard_md(REGIONS_TITLES[i], player_data_detailed)

if __name__ == "__main__":
    main()