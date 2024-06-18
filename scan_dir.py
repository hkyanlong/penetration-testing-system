from concurrent.futures import ThreadPoolExecutor
import requests
import tkinter as tk
from tkinter import filedialog


def get_request(url, choice_dir, state_codes):
    results = []

    def check_url(url):
        response = requests.head(url)
        print(f"URL: {url}, State Code: {response.status_code}")
        if response.status_code in state_codes:
            result = f"URL: {url}, State Code: {response.status_code}\n"
            results.append(result)

    if choice_dir == '1':
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        root.destroy()
        with open(file_path, 'r') as dir_file:
            urls = [url + line.strip() for line in dir_file]
    else:
        with open('directories.txt', 'r') as dir_file:
            urls = [url + line.strip() for line in dir_file]

    with ThreadPoolExecutor(max_workers=60) as executor:
        executor.map(check_url, urls)

    print()
    print()
    print_results_with_border(results)


def print_results_with_border(results):
    border = '-' * 100
    print(border)
    for result in results:
        print(f"|{result.strip():^98}|")
    print(border)
