import os, subprocess
import argparse
import certifi
import shutil
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
from new_day import new_day

# Load session cache
def load_session_cache():
    session_cache_file = '.session_cache.lock'
    if not os.path.exists(session_cache_file):
        session = input('Please give session cookies:')
        with open(session_cache_file,'w') as file:
            file.write(session)
        file.close()

    session = open(session_cache_file).read()
    if not isinstance(session, str):
        raise TypeError('Provided session cookie must be a string')

    return session


def collect_test_input(instructions, test_input_path):
    '''
    COLLECT TEST INPUT
    '''
    if os.path.exists(test_input_path):
        return

    for i, section in enumerate(instructions):
        if section.name == 'p' and 'example' in section.text.lower():
            next_section = section.find_next_sibling()
            if next_section and next_section.name == "pre":
                pre_content = next_section.text.strip()
                with open(test_input_path, "w", encoding="utf-8") as file:
                    file.write(pre_content)
                    print(f"Content for test input saved at: {test_input_path}")
                break


def collect_real_input(day_url, session, real_input_path):
    '''
    COLLECT REAL INPUT
    '''
    if os.path.exists(real_input_path):
        print(f"File already exists: {real_input_path}")
        return
    
    # Define headers for the request
    headers = {
        "User-Agent": "{USER_AGENT}",
        "Cookie": f"session={session}",
    }
    
    # Perform the HTTP GET request
    try:
        response = requests.get(f"{day_url}/input", headers=headers, verify=certifi.where())
        
        # Check if the response was successful
        if response.status_code == 200:
            with open(real_input_path, "w") as file:
                file.write(response.text)
            print(f"Content for real input saved at: {real_input_path}")
        else:
            print(f"Failed to fetch input. HTTP Status: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching input: {e}")




def daily_collect(args):

    # Day String
    day_str = f"{int(args.d):02d}"
    test_input_path = f"{day_str}_test.txt"
    real_input_path = f"{day_str}.txt"

    #Check if we already downloaded it
    if os.path.exists(test_input_path) and os.path.exists(real_input_path):
        #Both already exist, so stop
        return

    load_dotenv()  # Load environment variables from .env file

    ########### PARSE DAY PROBLEM ###########
    url = 'https://adventofcode.com'
    line_size = 120
    day_url = f'{url}/{args.y}/day/{args.d}'

    USER_AGENT = os.getenv("AOC_USER_AGENT")
    if not USER_AGENT:
        raise EnvironmentError("AOC_USER_AGENT environment variable not set. Please configure it.")

    headers = {'User-Agent': USER_AGENT}
    response = requests.get(day_url, headers=headers, verify=certifi.where())

    soup = BeautifulSoup(response.text, features="html.parser")
    instructions = soup.find('article',attrs={'class':'day-desc'})
    session = load_session_cache()

    ########### COLLECT DAY DESCRIPTION ###########
    # day_desc_title = soup.select_one(".day-desc h2")
    # title_text = day_desc_title.get_text(strip=True) if day_desc_title else ""
    # day_desc_path = os.path.join(dest, 'day_desc.md')
    # with open(day_desc_path, "w", encoding='utf-8') as md_file:
    #     md_file.write(f"# {title_text}\n\n")
    #     for section in instructions:
    #         if section.name == "p":
    #             md_file.write(section.get_text(strip=True) + "\n\n")
    #         elif section.name == "pre":
    #             md_file.write("```shell\n")
    #             md_file.write(section.get_text(strip=True) + "\n")
    #             md_file.write("```\n")
    #     print(f"Content for test input saved at : {day_desc_path}")
    #     md_file.close()

    collect_real_input(day_url, session, real_input_path)
    collect_test_input(instructions, test_input_path)

    #Setup Template
    new_day(int(args.d))

if __name__ == "__main__":

    ########### COLLECT ARGUMENTS ###########
    try:
        parser = argparse.ArgumentParser(description='Collect input for Advent of Code')
        parser.add_argument('-d',type=str,required=True,help='Day to collect')
        parser.add_argument('-y',type=str,required=True,help='Year to collect')
        args = parser.parse_args()
    except:
        raise KeyError('Missing entry for day (-d) or year (-y)')
    
    daily_collect(args)