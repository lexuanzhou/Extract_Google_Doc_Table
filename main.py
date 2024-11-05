import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_table_from_google_doc(url):
  try:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table')
    if not table:
      print("No table found.")
      return

    df = pd.read_html(str(table), header=1)[0]

    df.columns = ['x-coordinate', 'Character', 'y-coordinate']

    max_x = df['x-coordinate'].max()
    max_y = df['y-coordinate'].max()

    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for index, row in df.iterrows():
      grid[row['y-coordinate']][row['x-coordinate']] = row['Character']

    for row in grid:
      print(''.join(row))

  except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
  except Exception as e:
    print(f"Error processing data: {e}")

if __name__ == '__main__':
    url = 'https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub'
    extract_table_from_google_doc(url)

