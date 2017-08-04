# include packages
from scrapex import *
import config
# end include
# World Ranking function
def get_world_ranking():
    s = Scraper()
    doc = s.load(url=config.__WORLD_RANKING_URL__)
    rows = doc.q('//table[@class="data"]/tr[contains(@class,"row")]')
    for row in rows:
        item = []
        item.append('RK')
        RK                  = row.x('td[1]/text()').trim()
        item.append(RK)
        item.append('GOLDER')
        GOLFER              = row.x('td[2]//text()').trim()
        item.append(GOLFER)
        try:
            PROFILE         = row.x('td[2]/a/@href').trim()
        except:
            PROFILE         = row.x('td[2]/a/@href').trim()
        item.append('CNTRY')
        try:
            CNTRY           = row.x('td[3]/img/@alt').trim()
        except:
            CNTRY           = row.x('td[3]/text()').trim()
        item.append(CNTRY)
        item.append('WINS')
        WINS                = row.x('td[4]/text()').trim()
        item.append(WINS)
        item.append('TOP_10_FINISHES')
        TOP_10_FINISHES     = row.x('td[5]/text()').trim()
        item.append(TOP_10_FINISHES)
        item.append('TOP_25_FINISHES')
        TOP_25_FINISHES     = row.x('td[6]/text()').trim()
        item.append(TOP_25_FINISHES)
        item.append('AVG_PTS')
        AVG_PTS             = row.x('td[7]/strong/text()').trim()
        item.append(AVG_PTS)
        item.append('PROFILE')
        item.append(PROFILE)
        s.save(item, config.__WORLD_RANKING_EXPORT_FILE__)
# end world ranking function
# define world money list function
def get_world_money_list():
    s = Scraper()
    doc = s.load(url=config.__WORLD_MONEY_LIST_URL__)
    rows = doc.q('//table[@class="data"]/tr[contains(@class,"row")]')
    for row in rows:
        item = []
        item.append('RK')
        RK                  = row.x('td[1]/text()').trim()
        item.append(RK)
        item.append('GOLDER')
        GOLFER              = row.x('td[2]//text()').trim()
        item.append(GOLFER)
        try:
            PROFILE         = row.x('td[2]/a/@href').trim()
        except:
            PROFILE         = row.x('td[2]/a/@href').trim()
        item.append('CNTRY')
        try:
            CNTRY           = row.x('td[3]/img/@alt').trim()
        except:
            CNTRY           = row.x('td[3]/text()').trim()
        item.append(CNTRY)
        item.append('WINS')
        WINS                = row.x('td[4]/text()').trim()
        item.append(WINS)
        item.append('TOP_10_FINISHES')
        TOP_10_FINISHES     = row.x('td[5]/text()').trim()
        item.append(TOP_10_FINISHES)
        item.append('TOP_25_FINISHES')
        TOP_25_FINISHES     = row.x('td[6]/text()').trim()
        item.append(TOP_25_FINISHES)
        item.append('AMOUNT')
        AMOUNT              = row.x('td[7]/strong/text()').trim()
        item.append(AMOUNT)
        item.append('PROFILE')
        item.append(PROFILE)
        s.save(item, config.__WORLD_MONEY_LIST_EXPORT_FILE__)
# end world money list function
# define world cup points function
def get_world_cup_points():
    s = Scraper()
    doc = s.load(url=config.__WORLD_CUP_POINTS_URL__)
    rows = doc.q('//table[@class="data"]/tr[contains(@class,"row")]')
    for row in rows:
        item = []
        item.append('RK')
        RK                  = row.x('td[1]/text()').trim()
        item.append(RK)
        item.append('GOLDER')
        GOLFER              = row.x('td[2]//text()').trim()
        item.append(GOLFER)
        try:
            PROFILE         = row.x('td[2]/a/@href').trim()
        except:
            PROFILE         = row.x('td[2]/a/@href').trim()
        item.append('CNTRY')
        try:
            CNTRY           = row.x('td[3]/img/@alt').trim()
        except:
            CNTRY           = row.x('td[3]/text()').trim()
        item.append(CNTRY)
        item.append('WINS')
        WINS                = row.x('td[4]/text()').trim()
        item.append(WINS)
        item.append('TOP_10_FINISHES')
        TOP_10_FINISHES     = row.x('td[5]/text()').trim()
        item.append(TOP_10_FINISHES)
        item.append('TOP_25_FINISHES')
        TOP_25_FINISHES     = row.x('td[6]/text()').trim()
        item.append(TOP_25_FINISHES)
        item.append('POINTS')
        POINTS              = row.x('td[7]/strong/text()').trim()
        item.append(POINTS)
        item.append('PROFILE')
        item.append(PROFILE)
        s.save(item, config.__WORLD_CUP_POINTS_EXPORT_FILE__)    
# end world cup points function
# define PGA TOURNAMENT function
def get_pga_tour():
    s = Scraper()
    doc = s.load(url=config.__SCHEDULE_PGA_TOUR_URL__)
    rows = doc.q('//table[@class="data"]/tr[contains(@class,"row")]')
    for row in rows:
        item = []
        item.append('DATE')
        DATE                  = row.x('td[1]/text()').trim()
        item.append(DATE)
        item.append('TOURNAMENT')
        TOURNAMENT            = row.x('td[2]//text()').trim()
        item.append(TOURNAMENT)
        try:
            PROFILE           = row.x('td[2]/a/@href').trim()
        except:
            PROFILE           = row.x('td[2]/@href').trim()
        item.append('LOCATION')
        LOCATION              = row.x('td[3]/text()').trim()
        item.append(LOCATION)
        item.append('COURSE')
        COURSE                = row.x('td[4]/text()').trim()
        item.append(COURSE)
        item.append('PURSE')
        PURSE                 = row.x('td[5]/text()').trim()
        item.append(PURSE)
        item.append('NETWORK')
        NETWORK               = row.x('td[6]/text()').trim()
        item.append(NETWORK)
        item.append('CHAMPION')
        CHAMPION              = row.x('td[7]/text()').trim()
        item.append(CHAMPION)
        item.append('PROFILE')
        item.append(PROFILE)
        s.save(item, config.__WORLD_PGA_TOUR_EXPORT_FILE__)        
# end PGA TOURNAMENT function
# define PGA TOURNAMENT function
def get_lpga_tour():
    s = Scraper()
    doc = s.load(url=config.__SCHEDULE_LPGA_TOUR_URL__)
    rows = doc.q('//table[@class="data"]/tr[contains(@class,"row")]')
    for row in rows:
        item = []
        item.append('DATE')
        DATE                  = row.x('td[1]/text()').trim()
        item.append(DATE)
        item.append('TOURNAMENT')
        TOURNAMENT            = row.x('td[2]//text()').trim()
        item.append(TOURNAMENT)
        try:
            PROFILE           = row.x('td[2]/a/@href').trim()
        except:
            PROFILE           = row.x('td[2]/@href').trim()
        item.append('LOCATION')
        LOCATION              = row.x('td[3]/text()').trim()
        item.append(LOCATION)
        item.append('COURSE')
        COURSE                = row.x('td[4]/text()').trim()
        item.append(COURSE)
        item.append('PURSE')
        PURSE                 = row.x('td[5]/text()').trim()
        item.append(PURSE)
        item.append('NETWORK')
        NETWORK               = row.x('td[6]/text()').trim()
        item.append(NETWORK)
        item.append('CHAMPION')
        CHAMPION              = row.x('td[7]/text()').trim()
        item.append(CHAMPION)
        item.append('PROFILE')
        item.append(PROFILE)
        s.save(item, config.__WORLD_LPGA_TOUR_EXPORT_FILE__)        
# end PGA TOURNAMENT function
# define PGA TOURNAMENT function
def get_european_tour():
    s = Scraper()
    doc = s.load(url=config.__SCHEDULE_EUROPEAN_TOUR_URL__)
    rows = doc.q('//table[@class="data"]/tr[contains(@class,"row")]')
    for row in rows:
        item = []
        item.append('DATE')
        DATE                  = row.x('td[1]/text()').trim()
        item.append(DATE)
        item.append('TOURNAMENT')
        TOURNAMENT            = row.x('td[2]//text()').trim()
        item.append(TOURNAMENT)
        try:
            PROFILE           = row.x('td[2]/a/@href').trim()
        except:
            PROFILE           = row.x('td[2]/@href').trim()
        item.append('LOCATION')
        LOCATION              = row.x('td[3]/text()').trim()
        item.append(LOCATION)
        item.append('COURSE')
        COURSE                = row.x('td[4]/text()').trim()
        item.append(COURSE)
        item.append('PURSE')
        PURSE                 = row.x('td[5]/text()').trim()
        item.append(PURSE)
        item.append('NETWORK')
        NETWORK               = row.x('td[6]/text()').trim()
        item.append(NETWORK)
        item.append('CHAMPION')
        CHAMPION              = row.x('td[7]/text()').trim()
        item.append(CHAMPION)
        item.append('PROFILE')
        item.append(PROFILE)
        s.save(item, config.__WORLD_EURP_TOUR_EXPORT_FILE__)        
# end PGA TOURNAMENT function
# define PGA TOURNAMENT function
def get_chapmpions_tour():
    s = Scraper()
    doc = s.load(url=config.__SCHEDULE_CHAMPIONS_TOUR_URL__)
    rows = doc.q('//table[@class="data"]/tr[contains(@class,"row")]')
    for row in rows:
        item = []
        item.append('DATE')
        DATE                  = row.x('td[1]/text()').trim()
        item.append(DATE)
        item.append('TOURNAMENT')
        TOURNAMENT            = row.x('td[2]//text()').trim()
        item.append(TOURNAMENT)
        try:
            PROFILE           = row.x('td[2]/a/@href').trim()
        except:
            PROFILE           = row.x('td[2]/@href').trim()
        item.append('LOCATION')
        LOCATION              = row.x('td[3]/text()').trim()
        item.append(LOCATION)
        item.append('COURSE')
        COURSE                = row.x('td[4]/text()').trim()
        item.append(COURSE)
        item.append('PURSE')
        PURSE                 = row.x('td[5]/text()').trim()
        item.append(PURSE)
        item.append('NETWORK')
        NETWORK               = row.x('td[6]/text()').trim()
        item.append(NETWORK)
        item.append('CHAMPION')
        CHAMPION              = row.x('td[7]/text()').trim()
        item.append(CHAMPION)
        item.append('PROFILE')
        item.append(PROFILE)
        s.save(item, config.__WORLD_CHAM_TOUR_EXPORT_FILE__)        
# end PGA TOURNAMENT function
# define PGA TOURNAMENT function
def get_webcom_tour():
    s = Scraper()
    doc = s.load(url=config.__SCHEDULE_WEB_TOUR_URL__)
    rows = doc.q('//table[@class="data"]/tr[contains(@class,"row")]')
    for row in rows:
        item = []
        item.append('DATE')
        DATE                  = row.x('td[1]/text()').trim()
        item.append(DATE)
        item.append('TOURNAMENT')
        TOURNAMENT            = row.x('td[2]//text()').trim()
        item.append(TOURNAMENT)
        try:
            PROFILE           = row.x('td[2]/a/@href').trim()
        except:
            PROFILE           = row.x('td[2]/@href').trim()
        item.append('LOCATION')
        LOCATION              = row.x('td[3]/text()').trim()
        item.append(LOCATION)
        item.append('COURSE')
        COURSE                = row.x('td[4]/text()').trim()
        item.append(COURSE)
        item.append('PURSE')
        PURSE                 = row.x('td[5]/text()').trim()
        item.append(PURSE)
        item.append('NETWORK')
        NETWORK               = row.x('td[6]/text()').trim()
        item.append(NETWORK)
        item.append('CHAMPION')
        CHAMPION              = row.x('td[7]/text()').trim()
        item.append(CHAMPION)
        item.append('PROFILE')
        item.append(PROFILE)
        s.save(item, config.__WORLD_WEBP_TOUR_EXPORT_FILE__)        
# end PGA TOURNAMENT function
# main
if __name__ == '__main__':
    get_world_ranking()
    get_world_money_list()
    get_world_cup_points()
    get_pga_tour()
    get_lpga_tour()
    get_european_tour()
    get_chapmpions_tour()
    get_webcom_tour()