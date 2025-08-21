from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pandas import read_csv

DUCKDUCKGO = "https://duckduckgo.com/"

df = read_csv("keywords.csv")

chrome_driver = ChromeDriverManager().install()
driver = Chrome(service=Service(chrome_driver))
driver.maximize_window()

SEARCH_SELECTORS = [
    (By.ID, "search_form_input_homepage"),  
    (By.ID, "searchbox_input"),             
    (By.NAME, "q"),                         
]

for parola in df["keyword"]:
    driver.get(DUCKDUCKGO)

    search_box = None
    for by, value in SEARCH_SELECTORS:
        try:
            search_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((by, value))
            )
            print(f"[OK] Trovato campo ricerca con selettore: {by}={value}")
            break
        except:
            print(f"[X] Campo ricerca non trovato con: {by}={value}")

    if not search_box:
        print("Errore: nessun campo di ricerca trovato!")
        continue

    search_box.clear()
    search_box.send_keys(parola)
    search_box.submit()

    RESULT_SELECTORS = [
        (By.CSS_SELECTOR, "a[data-testid='result-title-a']"),
        (By.CSS_SELECTOR, "a.result__a"),
        (By.CSS_SELECTOR, "h2 a"),  
    ]

    primo_risultato = None
    for by, value in RESULT_SELECTORS:
        try:
            primo_risultato = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((by, value))
            )
            print(f"[OK] Primo risultato trovato con: {by}={value}")
            break
        except:
            print(f"[X] Primo risultato non trovato con: {by}={value}")

    if primo_risultato:
        df.loc[df["keyword"] == parola, "primo_risultato"] = primo_risultato.text
    else:
        df.loc[df["keyword"] == parola, "primo_risultato"] = "Nessun risultato trovato"

df.to_csv("risultati.csv", index=False)

driver.quit()