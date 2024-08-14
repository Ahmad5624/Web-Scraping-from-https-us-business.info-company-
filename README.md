
# Web Scraping from "https://us-business.info/company/"

✅ Scraped millions of data from this site.

✅ Scraped the data from all 50 states of USA.

✅ Used the httpx and selectolax to scrape this site.

✅ All data scraped into the excel file.

✅ Final data was cleaned and ready for use.





## Deployment

To run the "overall_data.py":
```bash
  pip install httpx
  pip install csv
  pip install pandas
  pip install time
```

## Usage(overall_data.py)

```javascript
import csv
import httpx
import pandas as pd
from selectolax.parser import HTMLParser
import time

#  DECLARATION
OUTPUT_FILE_NAME = 'Overall_data.csv'


# Run the Scraper
def RunScrapper():
    start_time = time.time()
    df = pd.read_excel('Location_links.xlsx', engine='openpyxl')
    # Access a specific column in the DataFrame
    Links = df['Links'].tolist()
    # get to the website
    count1 = 1
    for link in Links:
        print("*************************", count1, "*************************")
        # Loop through the pages
        for i in range(1, 9999999999):
            try:
                # Create an HTTP client
                client = httpx.Client()
                # Set follow_redirects attribute to True
                client.follow_redirects = True
                # Make a GET request with follow_redirects enabled
                resp = client.get(link + f'part{i}/', timeout=10)
                # Close the HTTP client
                client.close()
                root = HTMLParser(resp.text)
                # Function to fetch overall data
                fetch_over_all_data(link, root)
                # check for the next button
                buttons = root.css('a.button')
                if len(buttons) == 1:
                    previous_button = buttons[0].text()
                    if previous_button == 'Previous':
                        print("Page Ended")
                        break
                elif len(buttons) == 2:
                    print(buttons[1].text())
                else:
                    print("Button not found!")
                    break
            except:
                pass

        count1 += 1
        # time.sleep(0.1)
    # give time taken to execute everything
    print("time elapsed: {:.2f}s".format(time.time() - start_time))


# Fetch the Overall Data
def fetch_over_all_data(link, root):
    # Going into the Modals
    modals = root.css("div [class ='vcards'] div[class*='vcard']")
    for modal in modals:
        print('.............')
        # 1. Link Name
        try:
            Link_Name = 'https://us-business.info/company/' + modal.attributes.get('data-cid') + '/'
        except:
            Link_Name = 'Link not found'
        # 2. Name
        try:
            Name = 'Name not found'
            Name = bool(modal.css_first("div[class='fn org']"))
            if Name:
                Name = modal.css_first("div[class='fn org']").text()
        except:
            pass
        # 3. Category
        try:
            category_list = []
            Categories = modal.css('span.value')
            for Category in Categories:
                category_list.append(Category.text())
            # Convert the list to a string separated by commas
            Category = ', '.join(category_list)
        except:
            Category = 'Category not found'

        # 4. Address
        try:
            street_address = modal.css_first('span.street-address').text()
            locality = modal.css_first('span.locality').text()
            Address = street_address + ',' + locality
        except:
            Address = 'Address not found'

        # 5. State
        try:
            State = modal.css_first("abbr.region").text()
        except:
            State = "State not found"
        # 6. Postal Code
        try:
            Postal_code = modal.css_first("span.postal-code").text()
        except:
            Postal_code = 'Postal Code not found'

        # 7. Phone Number
        try:
            Phone_number = modal.css_first('div.tel').text()
        except:
            Phone_number = 'Phone Number not found'

        # 8. Website
        try:
            Website = "Website not found"
            website_checker = bool(modal.attributes.get('data-site'))
            if website_checker:
                Website = modal.attributes.get('data-site')
        except:
            pass

        # 0. Main Link
        print("0.Main Link:", link)
        # 1. Link Name
        print("1.Link Name:", Link_Name)
        # 2. Name
        print("2.Name:", Name)
        # 3. Category
        print("3.Category:", Category)
        # 4. Address
        print("4.Address:", Address)
        # 5. State
        print("5.State:", State)
        # 6. Postal Code
        print("6.Postal Code:", Postal_code)
        # 7. Phone Number
        print("7.Phone Number:", Phone_number)
        # 8. Website
        print("8.Website:", Website)

        # Write to the file
        output_result = [link] + [Link_Name] + [Name] + [Category] + [Address] + [State] + [Postal_code] + [
            Phone_number] + [Website]
        write_to_file([output_result])


# Write the data to the file
def write_to_file(rows):
    file = open(OUTPUT_FILE_NAME, 'a', encoding='utf-8-sig', newline="")
    writer = csv.writer(file)
    writer.writerows(rows)
    file.close()


# Main function just like in C++/
if __name__ == '__main__':
    # Run Scraper
    RunScrapper()

```
## Documentation
To learn more about the selectolax, visit the official page now:
[Documentation](https://pypi.org/project/selectolax/)


# Support
For support email me at: razawarraich2334@gmail.com