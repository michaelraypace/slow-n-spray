# Slow-N-Spray
Selenium-powered password sprayer
Slow-N-Spray defeats cookie/session based security measures by using selenium to emulate new browser instances for each request. Use in conjunction with [Proxy Cannon](https://github.com/proxycannon/proxycannon-ng) for best results.

## Requirements

Slow and Spray requires the following
* Python3
* selenium
* WebDriver (I use gecko; installation instructions [here](https://selenium-python.readthedocs.io/installation.html "Selenium readthedocs.io"))

Usage: python threadedLogin.py -f \<users.lst\> -t \<threadCount\> -u \<url\> -p \<password\>
