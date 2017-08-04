var express = require('express')
var path = require('path')
var app = express()
var request = require('request')
var fs =  require('fs')
var cheerio = require('cheerio')
require('should');
var csv = require('fast-csv');

var port = 8000
var parent_url = 'http://www.singaporelaw.sg'
var first_url = 'http://www.singaporelaw.sg/sglaw/laws-of-singapore/case-law/free-law/high-court-judgments?limit=0'
var invest_url = []
var inputFile= 'investors.csv'

function csv_parse(){
    // Create the parser
    csv
    .fromPath(inputFile)
    .on("data", function(data){
        invest_url.push(data[2]);
    })
    .on("end", function(){
        parse()
    });

}
function parse(){
    console.log("*************************************************************************")
    for (var i in invest_url)
    {
        if (i==0)
            continue
        console.log(invest_url[i])
        invest_category = invest_url[i].split("/")[3]
        console.log(invest_category)
        request('https://www.crunchbase.com/organization/500-startups#/entity', function(err, resp, body){
            console.log(resp.statusCode)
            console.log("ok")
            var $ = cheerio.load(body);
            invest_name = $("h1#profile_header_heading a").text()
            console.log(invest_name)
            overview_len = $("dt").length
            console.log(overview_len)
            invest_overview = $("dt")
            for (var i in overview_len)
            {
                console.log(invest_overview[i])
            }
        });
        return;
    }
}

function save_html(url){
    request(url, function(err, resp, body){
        if (!err && resp.statusCode === 200){
            var $ = cheerio.load(body);
            reg = /\d+/
            var filename = "html/" + reg.exec(url) + ".html"
            console.log(filename)
            var content = $("div.contentsOfFile").html()
            if (content !=null)
                fs.writeFileSync(path.join(process.cwd(), filename), content,{'encoding': 'utf-8'})
            
        }
    });
}                

csv_parse()
app.listen(port)
console.log('server running on ' + port);