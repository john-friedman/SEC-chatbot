from sec_parsers import Filing, download_sec_filing, set_headers

output_dir = "10K XML/"

urls = [('Tesla','https://www.sec.gov/Archives/edgar/data/1318605/000095017022000796/tsla-20211231.htm'),
        ('Apple','https://www.sec.gov/Archives/edgar/data/320193/000119312514383437/d783162d10k.htm'),
        ('Meta','https://www.sec.gov/Archives/edgar/data/1326801/000132680123000013/meta-20221231.htm'),
        ('Netflix','https://www.sec.gov/Archives/edgar/data/1065280/000106528023000035/nflx-20221231.htm')]

set_headers("John doe","johndoe@email.com")
for company_name, url in urls:
    html = download_sec_filing(url)
    filing = Filing(html)
    filing.parse()

    filing.save_xml(output_dir + company_name + '.xml')


