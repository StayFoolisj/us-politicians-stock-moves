The Stop Trading on Congressional Knowledge (STOCK) Act was signed into law by President Barack Obama in 2012 after a series of revelations of insider trading done by congressional members. 

This act forced a requirement to report all their trades to the Ethics of Financial Disclosures. Information that is publicly available, but very hard to navigate. This is an attempt to make this information much more accessible. Hopefully this can lead to people building something cool of the data. This idea was inspired from events in the beginning of the year where multiple senators where discovered in illegal acts. They used non-publicly disclosed information gained from their political office to profit of the financial markets, which is strictly illegal. 


The app is divided into two main parts. 

/extract : 
is responsible for the extraction of data. 

It uses Selenium to access public websites and queries every single record stored in their databases, one by one. I had an interesting problem here as not all records are digital. So I had to first store the documents metadata. For paper records, I store their metadata for later processing. For digital records, I extract all the data and post it to the API. 

/src :
is the API that contains the logic for recieving, storing and serving data. 
