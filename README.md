# WebScarp_Trulia_property
This code is to use Python 3.5 to parse the content of property from Trulia.com as the follows and photo of property.
1. Features
2. Public Record
3. Price History
4. Real Estate Trend
This infomation will be stored as json. The code will use the Beautifulsoup Class mainly so before you run the code, you have to install the bs4 library first. Please unzip the beautifulsoup4-4.1.0.tar and run the follown command propmt
> python setup.py install

In command prompt, run the following command propmt
a. output json file and photo 
> python webscrap_trulia.py <properties.txt> -a

b. output json file only
> python webscrap_trulia.py <properties.txt> -j

c. output photo only (format jpg)
> python webscrap_trulia.py <properties.txt> -p

Annotation: 
(1) <properties.txt> is a txt file containing links from Trulia and each link is separated by newline character as attached file "properties.txt"
(2) The filename of photo is the address of each property, each word separated by "-"
(3) The filename of json is the same as the filename of properties.txt
(4) json format
{  link A:
   {"Features": [  ] ,
    "Public Records" : [  ] , 
    "Price History": [ ],
      "Real Estate Trends": [ ] }, 
     link B:
   {"Features": [  ] ,
    "Public Records" : [  ] , 
    "Price History": [ ],
      "Real Estate Trends": [ ] },
       ..........
       .......... }    
