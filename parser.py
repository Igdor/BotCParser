import datetime
import csv

from bs4 import BeautifulSoup
from dotenv import dotenv_values

import nara_scraper


config = dotenv_values("settings.env")


def game_data_save(game_data):
    #headers = ["game_date", "pack_name", "player_data"]

    with open('GameResults.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
    #    writer.writerow(headers)
        writer.writerow([game_data.get("game_date")])
        writer.writerow([game_data.get("pack_name")])
        writer.writerows(game_data.get("player_data"))
    csvfile.close()


def parse_game(link):

    page_source = nara_scraper.get_source_data(link)
    # parsing content of the page
    soup = BeautifulSoup(page_source, "html.parser")

    game_data = {}
    # extracting data about game
    pack_name = soup.find("div", class_="absolute top-0 left-16 flex items-center justify-center text-start mt-1 px-2 font-bold bg-gray-800 bg-opacity-70 rounded-md z-0").get_text().replace("\t", "").replace(
            "\r", "").replace("\n", "")
    # extracting data about players
    roles = soup.find_all("div", {"class": "relative player-seat flex flex-col items-center pointer-events-auto"})
    seat_counter = 0
    player_data = []
    reminders = []
    for role in roles:
        role_name = role.find("div", class_="rounded-full cursor-pointer").get_text().replace("\t", "").replace(
            "\r", "").replace("\n", "")
        role_nickname = role.find("div",
                                  {"class": "w-full text-center font-sembibold px-1 truncate w-32"}).get_text().replace(
            "\t", "").replace("\r", "").replace("\n", "")
        role_reminders = role.find("section", class_="absolute flex justify-end items-center text-gray-800 overflow-visible")
        role_reminders = role_reminders.find_all("div", {"class": ("reminder-token-" + str(seat_counter))})
        for reminder in role_reminders:
            reminders.append(
                reminder.get_text().replace("\t", "").replace("\r", "").replace("\n", "").lstrip().rstrip())

        player_data.append([seat_counter + 1, role_name.lstrip().rstrip(), role_nickname.lstrip().rstrip(), reminders])
        reminders = []
        seat_counter += 1

    game_date = datetime.datetime.now()
    game_data["game_date"] = game_date.strftime("%d/%m/%Y %H:%M:%S")
    game_data["pack_name"] = pack_name.lstrip().rstrip()
    game_data["player_data"] = player_data

    game_data_save(game_data)

    return game_data


print(parse_game(config.get("NARA_URL")))

