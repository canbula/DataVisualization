from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up the browser and sample data link
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
browser = webdriver.Chrome(options=chrome_options)
link = "https://www.sahibinden.com/jaguar?pagingSize=50"
browser.get(link)

# Detect the number of pieces of data
search_result = browser.find_element(by=By.CSS_SELECTOR, value=".result-text-sub-group").text
max_count = int(''.join(x for x in search_result if x.isdigit()))

# Variable for changing the page
paging_offset = 0

car_list = []
# Iterate through all available pages, compartmentalise the data, and append to an array
while paging_offset <= max_count:
    cars = browser.find_elements(by=By.CSS_SELECTOR, value='.searchResultsItem:not(.nativeAd)')
    for c in cars:
        model = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsTagAttributeValue')
        infos = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsAttributeValue')
        price = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsPriceValue')
        location = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsLocationValue')
        try:
            car_list.append(
                {
                'model': model[0].text,
                'version': model[1].text,
                'year': int(infos[0].text),
                'km': int(infos[1].text.replace('.', '')),
                'color': infos[2].text,
                'price': {
                'amount': int(price[0].text.split(" ")[0].replace(".", "")),
                'currency': price[0].text.split(" ")[1]
                },
                'location': location[0].text.replace('\n', ' ')
                }
            )
        finally:
            continue
    paging_offset += 50
    link = f"https://www.sahibinden.com/jaguar?pagingOffset={paging_offset}&pagingSize=50"
    browser.get(link)

print(car_list)
browser.close()