<h1>VCCF</h1>
<p>VCCF (<em>Venture Capital Company Finder</em>) is a Python based web appication that allows Venture Capital Firms to reseaerch Start Up companies from <a href="https://www.producthunt.com/">producthunt.com</a> by collecting data from the web, scraping website, and presenting the dataa in the form of charts, tables and statistics.</p>
<h1>Installation</h1>
<p>Due to the delicate nature of webscraping much of the core functionaity of this web applciation is no longer viable, due to lack of maintenance of the website and many of the websites being scraped employing anti-scraping barriers to their codeset. Therefor installation of this Web App is no longer realistic and the code is now theoretical / proof of concept</p>
<h1>Features</h1>
<h2>Web Crawling & Scraping</h2>
<p>
One of the core elements of this program is that it allowed the user to enter the slug of a product from producthunt and intelligently search the web to find key statistics and details on the wide range of aspects of the Start Up. The websites scraped include:
<ul>
    <li>Github</li>
    <li>Crunchbase</li>
    <li>LinkedIn</li>
    <li>Y Combinator</li>
    <li>Apollo.io</li>
    <li>SaasHub</li>
    <li>SaasWorthy</li>
</ul>
</p>
<img src="static/images/product-info.png">
<p>Further scraping was used on the website Statista to search for, and replicate, the non-premium graphs available on their site. To scrape Statista as well as other websites, a local version of chrome driver was installed inside the docker container of this website runs of from, allowing the web scraper to disguise itself as an actual user preventing the site and avoiding detection and blockers placed on conventional web scraping bots.</p>
<img src="static/images/market-data.png">
<br>
<br>
<h2>'Big Five' Personality Scores Using LIWC Text Analysis & 'Closest Match' Algorithim</h2>
<p><a href="https://www.liwc.app/">LIWC</a> is a tool used to analyze others’ language and can help to understand their thoughts, feelings, personality. Using this tool in conjunction with the Twitter API, I was able to obtain the results produced by LIWC for each of the Start Up's founders. Then, a set of sample data containg text from participants in a psychological study along with their known 'Big Five' Personality score was also run through LIWC. Finally the 'Closest Match' Algorithim was used to match the founders LIWC scores to the Sample's participant LIWC score who's matched closest to it, and returning the sample particpants 'Big Five' score in a bar chart.</p>
<img src="static/images/founders.png">
<br>
<br>
<h2>Save Favourites to your profile</h2>
<p>Save your favourite Start Up companies to your profile by selecting the 'favourite' option at the top of the page. This allows the company to be saved in the VCCF database for quick access without requiring the need to reload the analysis everytime. If you do want to reload the analysis however, simply search for the Start Up again, and updated analysis will be presented to you.</p>
<img src="static/images/favourites.png">
<h1>Extra Screenshots</h1>
<img src="screenshots/Product-Tab.png">
<p><small><em>Analysis and statistics on the Start Up, collected from websites across the web.</em></small></p>
<img src="screenshots/Founder-Tab.png">
<p><small><em>Founder tab with 'Big 5' analaysis and links to the founders social media.</em></small></p>
<img src="screenshots/Market-Tab.png">
<p><small><em>Graphs scraped from Statista relating to the industry and technology used by the Start Up company.</em></small></p>
<hr>

