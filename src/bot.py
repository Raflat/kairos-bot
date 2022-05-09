"""Automatic class reservation bot for Kairos"""
from configparser import ConfigParser
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

# Load configuration from the .ini file
config = ConfigParser()
config.read(r"resources\config.ini")

# Create driver for Chrome in headless mode, to prevent user inputs while running
options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service(config["DEFAULT"]["DriverPath"]), options=options)

def click(xpath):
    """
    Clicks on the interactables from the given list.

    Parameter:
        xpath (str): XPath of the interactables
    """
    elements = driver.find_elements(By.XPATH, xpath)
    for element in elements:
        element.click()


def write(xpath, text):
    """
    Writes some text in the given form.

    Parameters:
        xpath (str): XPath of the interactable

        text (str): text to write
    """
    driver.find_element(By.XPATH, xpath).send_keys(text)


def main():
    """Main function"""
    # Set implicit wait to be sure that everything loads on the page
    driver.implicitly_wait(3)

    # Load Kairos in the current session
    kairos_url = ("https://kairos.unifi.it/agendaweb/index.php?view="
                  "prenotalezione&include=prenotalezione_home&_lang=it")
    driver.get(kairos_url)

    # Accept terms
    click("//div[3]/div[2]/label/span[@class='slider round']")
    click("//div[4]/div[2]/label/span[@class='slider round']")
    click("//*[@id='oauth_btn']")

    # Log in to Kairos
    write("//*[@id='username']", config["DEFAULT"]["Username"])
    write("//*[@id='password']", config["DEFAULT"]["Password"])
    click("/html/body/div/div/div/div[1]/form/div[5]/button")

    # Open tab for new reservations
    click("//*[@id='menu_container']/div[1]/div/div[1]/a")

    # Click on available reservations
    click("//*[@title='Verifica e prenota il tuo posto']")

    # Quit the current session
    driver.quit()


if __name__ == "__main__":
    main()
