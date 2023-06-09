from selenium import webdriver
from bs4 import BeautifulSoup
import time


# The below class is used to scrap data from the landing page
class HomePage:
    # landing page url
    baseUrl = 'https://www.theverge.com'
    # empty list to resultant scrap data
    res = list()
    # getting chrome webdriver using webdriver from selenium module
    driver = webdriver.Chrome()
    # opening landing page using get method of driver object
    driver.get(baseUrl)
    # delay to just load the page completely
    time.sleep(10)
    # getting html source of a page using attribute page_source
    html = driver.page_source
    # creating soup object for html
    soup = BeautifulSoup(html, 'html.parser')

    # to scrap main highlighted articles
    def mainContent(self):
        # getting parent div tag using find_all method
        div = self.soup.find_all('div',
                                 class_='home-hero relative mb-60 flex w-full max-w-container-lg flex-col px-10 md:mx-auto md:max-w-[560px] lg:mx-auto lg:max-w-container-lg lg:flex-row lg:pr-0')
        for i in div:
            # getting Subparent div using find method
            maindiv = i.find('div',
                             class_='relative border-b border-gray-31 pb-20 md:pl-80 lg:border-none lg:pl-[165px] -mt-20 sm:-mt-40')
            # to get title which is defined in h2 tag
            title = maindiv.find('h2',
                                 class_='mb-14 font-manuka text-65 font-black leading-80 tracking-1 text-white md:mb-18 md:text-90')
            # to get link which is defined in a tag and using ['href']
            link = maindiv.find('a', class_='group-hover:shadow-highlight-blurple')
            # to get date which is defined in span tag
            date = maindiv.find('span', class_='text-gray-63 dark:text-gray-94')
            # to get author name which is defined in a tag
            auth = maindiv.find('a', class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8').text
            # to get 2nd author name if any present which is defined in a tag and class mentioned below
            auth1 = maindiv.find('a', class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin')
            # concatenating the authors names if applicable
            if auth1 is not None:
                auth = auth + " and " + auth1.text
            # creating result dictionary and appending the same to result list
            resIter = {'headline': title.text, 'URL': self.baseUrl + link['href'], 'author': auth, 'date': date.text}
            self.res.append(resIter)
        return

    # to scrap top articles
    def topStories(self):
        div = self.soup.find_all('div',
                                 class_='max-w-content-block-standard md:w-content-block-compact md:max-w-content-block-compact lg:w-[240px] lg:max-w-[240px] lg:pr-10')
        for i in div:
            title = i.find('h2', class_='font-polysans text-20 font-bold leading-100 tracking-1 md:text-24 lg:text-20')
            link = i.find('a', class_='group-hover:shadow-underline-franklin')
            date = i.find('span', class_='text-gray-63 dark:text-gray-94')
            auth = i.find('a', class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8').text
            auth1 = i.find('a', class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin')
            if auth1 is not None:
                auth = auth + " and " + auth1.text
            resIter = {'headline': title.text, 'URL': self.baseUrl + link['href'], 'author': auth, 'date': date.text}
            self.res.append(resIter)
        return

    # to scrap articles which are generated by javascript
    def mainDynamicallyLoaded(self):
        div = self.soup.find_all('div',
                                 class_='max-w-content-block-mobile sm:w-content-block-compact sm:max-w-content-block-compact')
        for i in div:
            if i is not None:
                title = i.find('h2', class_='font-polysans text-20 font-bold leading-100 tracking-1 md:text-24')
                if title is not None:
                    link = i.find('a',
                                  class_='after:absolute after:inset-0 group-hover:shadow-underline-blurple dark:group-hover:shadow-underline-franklin')
                    date = i.find('span', class_='text-gray-63 dark:text-gray-94')
                    auth = i.find('a',
                                  class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8').text
                    auth1 = i.find('a',
                                   class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin')
                    if auth1 is not None:
                        auth = auth + " and " + auth1.text
                    resIter = {'headline': title.text, 'URL': self.baseUrl + link['href'], 'author': auth,
                               'date': date.text}
                    self.res.append(resIter)
        return

    # to scrap most popular articles
    def mostPopular(self):
        ol = self.soup.find('ol', class_='styled-counter w-full lg:mt-20 lg:w-[320px] styled-counter-compact')
        li = ol.find_all('li',
                         class_='mb-20 border-b pb-20 text-franklin last:mb-0 last:border-0 last:pb-0 lg:last:mb-20 border-b-franklin')
        for i in li:
            title = i.find('h3', class_='mb-4 font-polysans text-18 font-medium leading-110 tracking-1')
            link = i.find('a', class_='text-white hover:text-franklin')
            auth = i.find('span', class_='mr-8 text-gray-ef').text
            date = i.find('span', class_='mr-8 font-light text-gray-ef').text
            resIter = {'headline': title.text, 'URL': self.baseUrl + link['href'], 'author': auth,
                       'date': date}
            self.res.append(resIter)
        return

    # the main method which calls all the above functions in a particular order
    def getData(self):
        self.mainContent()
        self.topStories()
        self.mostPopular()
        self.mainDynamicallyLoaded()
        self.driver.quit()
        # returning the result list
        return self.res


class SpecificPage:
    baseUrl = 'https://www.theverge.com'
    res = list()
    # list of url for specific category
    urls = [baseUrl + '/tech', baseUrl + '/reviews', baseUrl + '/science', baseUrl + '/entertainment']

    # to scrap main highlighted articles
    def topContent(self, soup):
        div = soup.find_all('div',
                            class_='duet--content-cards--content-card group relative bg-white text-black dark:bg-gray-13 dark:text-white pb-24 border-b border-gray-cc dark:border-gray-4a sm:border-b-0 sm:mx-15 sm:w-1/2 lg:pb-24')
        for i in div:
            if i is not None:
                title = i.find('h2',
                               class_='mb-8 font-polysans text-30 font-bold leading-100 sm:text-35')
                link = i.find('a',
                              class_='after:absolute after:inset-0 group-hover:shadow-highlight-franklin dark:group-hover:shadow-highlight-blurple')
                date = i.find('span', class_='text-gray-63 dark:text-gray-94')
                auth = i.find('a', class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8').text
                auth1 = i.find('a', class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin')
                if auth1 is not None:
                    auth = auth + " and " + auth1.text
                resIter = {'headline': title.text, 'URL': self.baseUrl + link['href'], 'author': auth,
                           'date': date.text}
                self.res.append(resIter)
        return

    # to scrap articles which are generated by javascript
    def dynamicallyLoaded(self, soup):
        div = soup.find_all('div',
                            class_='max-w-content-block-mobile sm:w-content-block-standard sm:max-w-content-block-standard')
        for i in div:
            if i is not None:
                title = i.find('h2', class_='font-polysans text-20 font-bold leading-100 tracking-1 md:text-24')
                if title is not None:
                    link = i.find('a',
                                  class_='after:absolute after:inset-0 group-hover:shadow-underline-blurple dark:group-hover:shadow-underline-franklin')
                    date = i.find('span', class_='text-gray-63 dark:text-gray-94')
                    auth = i.find('a',
                                  class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8').text
                    auth1 = i.find('a',
                                   class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin')
                    if auth1 is not None:
                        auth = auth + " and " + auth1.text
                    resIter = {'headline': title.text, 'URL': self.baseUrl + link['href'], 'author': auth,
                               'date': date.text}
                    self.res.append(resIter)
        return

    def getData(self):
        for url in self.urls:
            driver = webdriver.Chrome()
            driver.get(url)
            time.sleep(10)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            self.topContent(soup)
            self.dynamicallyLoaded(soup)
            driver.quit()
        return self.res

