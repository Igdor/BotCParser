import datetime
import csv
import logging
from sys import stdout

from bs4 import BeautifulSoup
from dotenv import dotenv_values

import nara_scraper


config = dotenv_values('settings.env')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    handlers=[logging.FileHandler("info.log", encoding='utf-8', mode='w'), logging.StreamHandler(stdout)])


def game_data_save(game_data):

    with open('GameResults.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([game_data.get('game_date'), game_data.get('pack_name'), game_data.get('fable_list')])
        writer.writerows(game_data.get('player_data'))
    csvfile.close()


def parse_game(link):

    page_source = nara_scraper.get_source_data(link)
    if page_source == "No":
        logging.error("No eligible data found")
        return None
    soup = BeautifulSoup(page_source, 'html.parser')
    logging.info("Data successfully retrieved from " + str(link))
    game_data = {}
    # extracting data about game
    pack_name = soup.find("div", class_="absolute top-0 left-16 flex items-center justify-center text-start mt-1 px-2 font-bold bg-gray-800 bg-opacity-70 rounded-md z-0").get_text().replace("\t", "").replace(
            "\r", "").replace("\n", "")
    fables = soup.find_all("section", {'class': "flex items-center justify-center gap-2 w-full h-full p-1"})
    fable_list = []
    for fable in fables:
        fable_list.append(fable.get_text().replace("\t", "").replace("\r", "").replace("\n", "").lstrip().rstrip())
    # extracting data about players
    roles = soup.find_all("div", {'class': "relative player-seat flex flex-col items-center pointer-events-auto"})
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
    game_data["fable_list"] = fable_list
    game_data["player_data"] = player_data

    game_data_save(game_data)
    logging.info("Data saved to GameResults.csv")

    return game_data


print(parse_game(config.get("NARA_URL")))

