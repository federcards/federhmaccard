#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

# The smart card has 72 slots, and we need a way to help people remember which
# slot they use. Luckily we have an ancient Chinese literature called
#   "The Thousand Characters Essay" 
#   https://www.angelfire.com/ns/pingyaozhuan/tce.html
# and we will use the first chapter.

wordlist = [e.strip().split(" ") for e in """
天 sky
地 earth
玄 black
黃 yellow
宇 space
宙 time
洪 vast
荒 vacant
日 sun
月 lunar
盈 full
昃 decline
辰 star
宿 constellation
列 placed
張 spread
寒 cold 
來 arrive
暑 heat 
往 depart
秋 autumn
收 harvest
冬 winter
藏 storage
閏 leap
餘 extras
成 fulfill
歲 year
律 pitches
呂 chromatics
調 harmonize
陽 yang
雲 cloud
騰 rise
致 cause
雨 rain
露 dew
結 congeal
為 result
霜 frost
金 gold
生 born
麗 beauty
水 river
玉 jade
出 origin
崑 Kunlun
崗 mountain
劍 sword
號 named
巨 great
闕 palace
珠 pearl
稱 called
夜 night
光 gleam
果 fruit
珍 dearest
李 plum
柰 apple
菜 vegetable
重 valued
芥 mustard
薑 ginger
海 ocean
鹹 saline
河 stream
淡 fresh
鱗 scale
潛 submerge
羽 feather
翔 glide
""".strip().split("\n")]
assert(len(set([e[0] for e in wordlist])) == 72)
assert(len(set([e[1] for e in wordlist])) == 72)


class VaultSelector(Frame):

    def __init__(self, parent):
        Frame.__init__(self)

        
