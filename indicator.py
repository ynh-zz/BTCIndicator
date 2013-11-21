#!/usr/bin/env python
import os
import sys
import gtk
import appindicator
import json
import threading
import urllib2

PING_FREQUENCY = 60 # seconds

# Translated from https://github.com/turingou/btc/blob/master/libs/cli.js
def btcchina(v):
    stat = 'error'
    last = 'data error'
    if 'ticker' in v and 'last' in v['ticker']:
        stat = 'ok'
        last = u'\u00A5 ' + str(v['ticker']['last'])

    return {
        'stat': stat,
        'last': last
    }


def bitstamp(v):
    stat = 'error'
    last = 'data error'
    if 'last' in v:
        stat = 'ok'
        last = '$ ' + str(v['last'])

    return {
        'stat': stat,
        'last': last
    }


def mtgox(v):
    stat = 'error'
    last = 'data error'
    if 'data' in v and 'last' in v['data']:
        stat = 'ok'
        last = '$ ' + str(v['data']['last']['value'])

    return {
        'stat': stat,
        'last': last
    }


def fxbtc(v):
    stat = 'error'
    last = 'data error'
    if 'result' in v:
        stat = 'ok'
        last = u'\u00A5 ' + str(v['ticker']['ask'])

    return {
        'stat': stat,
        'last': last
    }


def okcoin(v):
    stat = 'error'
    last = 'data error'
    if 'ticker' in v:
        stat = 'ok'
        last = u'\u00A5 ' + str(v['ticker']['last'])

    return {
        'stat': stat,
        'last': last
    }


def btctrade(v):
    stat = 'error'
    last = 'data error'
    if 'last' in v:
        stat = 'ok'
        last = u'\u00A5 ' + str(v['last'])

    return {
        'stat': stat,
        'last': last
    }


def chbtc(v):
    stat = 'error'
    last = 'data error'
    if 'ticker' in v:
        stat = 'ok'
        last = u'\u00A5 ' + str(v['ticker']['last'])

    return {
        'stat': stat,
        'last': last
    }


def futures796(v):
    stat = 'error'
    last = 'data error'
    if 'ticker' in v:
        stat = 'ok'
        last = '$ ' + str(v['ticker']['last'])

    return {
        'stat': stat,
        'last': last
    }


def btc100(v):
    stat = 'error'
    last = 'data error'
    if 'ticker' in v:
        stat = 'ok'
        last = u'\u00A5 ' + str(v['ticker']['last'])

    return {
        'stat': stat,
        'last': last
    }

#Copied from https://github.com/turingou/btc/blob/master/libs/sdk.js
api = {
    'mtgox': {
        'url': 'http://www.btc123.com/e/interfaces/tickers.php?type=MtGoxTicker&suffix=0.8636577818542719'
    },
    'bitstamp': {
        'url': 'https://www.bitstamp.net/api/ticker'
    },
    'futures796': {
        'url': 'http://www.btc123.com/e/interfaces/tickers.php?type=796futuresTicker&suffix=0.38433733163401484'
    },
    'btcchina': {
        'url': 'http://www.btc123.com/e/interfaces/tickers.php?type=btcchinaTicker&suffix=0.3849131213501096'
    },
    'okcoin': {
        'url': 'http://www.btc123.com/e/interfaces/tickers.php?type=okcoinTicker&suffix=0.7636065774131566'
    },
    'chbtc': {
        'url': 'http://www.btc123.com/e/interfaces/tickers.php?type=chbtcTicker&suffix=0.5108873315621167'
    },
    'fxbtc': {
        'url': 'http://www.btc123.com/e/interfaces/tickers.php?type=fxbtcTicker&suffix=0.19148686854168773'
    },
    'btctrade': {
        'url': 'http://www.btc123.com/e/interfaces/tickers.php?type=btctradeTicker&suffix=0.1531917753163725'
    },
    'btc100': {
        'url': 'http://www.btc123.com/e/interfaces/tickers.php?type=btc100Ticker&suffix=0.16103304247371852'
    }
}


class BitcoinChecker:
    def __init__(self):
        self.apimenu = {}
        self.use = 'mtgox'
        self.ind = appindicator.Indicator("bitcoin-indicator",
                                          os.path.dirname(os.path.realpath(__file__))+"/btc.png",
                                          appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.menu_setup()
        self.apimenu[self.use].set_label("=> "+self.use)
        self.ind.set_menu(self.menu)

    def menu_setup(self):
        self.menu = gtk.Menu()
        for k in api.items():
            name = k[0]
            item = gtk.MenuItem(name)
            item.connect("activate", lambda widget, n=name: self.set_source(n))
            item.show()
            self.menu.append(item)
            self.apimenu[name] = item

        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(gtk.SeparatorMenuItem())
        self.menu.append(self.quit_item)

    def set_source(self, name):
        self.apimenu[self.use].set_label(self.use)
        self.use = name
        self.apimenu[self.use].set_label("=> "+self.use)
        self.check_price()

    def main(self):
        threading.Thread(target=self.check_price).start()
        gtk.timeout_add(PING_FREQUENCY * 1000, self.check_price)
        gtk.main()

    def quit(self, widget):
        sys.exit(0)

    def check_price(self):
        use = self.use
        data = json.load(urllib2.urlopen(api[use]['url']))
        if use == self.use:
            values = globals()[use](data)
            self.ind.set_label(values['last'])


if __name__ == "__main__":
    indicator = BitcoinChecker()
    indicator.main()