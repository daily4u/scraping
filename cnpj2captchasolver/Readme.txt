
- Requirement
  
	python 2.7.12+

- File Structure

  1. cnpj.py - script for scraping
	2. captcha.jpg - captcha image (temporary file)	
	3. cnpj_list.csv - cnpj's list csv file
	4. item.csv - result csv file 

- Packages & Install
	pip install selenium
	pip install captcha2upload
	pip install pil
	pip install https://github.com/cungnv/scrapex/archive/master.zip

- Web driver (Chrome Driver)
	
	1. download https://chromedriver.storage.googleapis.com/2.30/chromedriver_linux64.zip (Ubuntu, linux)
	2. upzip this file, you can see chromedriver file:
	3. open terminal window and type following command(copy chromedriver file to /usr/bin directory):
		 sudo cp chromedriver /usr/bin  
	
- Execute script file

	python cnpj.py
