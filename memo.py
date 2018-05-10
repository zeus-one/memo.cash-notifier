#!/usr/bin/env python

from BeautifulSoup import BeautifulStoneSoup
from websocket import create_connection
from gi.repository import Notify
from termcolor import colored
import requests
import json 
import time
import sys

class MemoNotifier(object):

  def __init__(self, address):
    self.prefixes = {'6d03': 'Reply', '6d04': 'Like/Tip', '6d06': 'Follow', '6d07': 'Unfollow', '6d0c': 'Topic Message'}
    self.addr = address


  def memo_user(self, address):
    data = requests.get("https://memo.cash/profile/%s" %address, verify=False)
    soup = BeautifulStoneSoup(data.content)
    table = soup.find("table", { "class" : "table left profile" })
    return soup.find('td').text


  def notify(self):
    Notify.init("Memo.cash notificator")
    Notify.Notification.new("New memo event").show()



  def isOurPost(self, tx):
    re = requests.get("https://bccblock.info/api/tx/" + str(tx))
    data = re.json()
    return data["vin"][0]["addr"] == self.addr


  def Listen(self):
    ws = create_connection("wss://ws.blockchain.info/bch/inv")
    ws.send("""{"op":"unconfirmed_sub"}""")
    while True:
      tx = json.loads(ws.recv())
      outputs = tx["x"]['out']

      for vout in outputs:
        if vout["script"][0:2] == '6a' and vout['script'][4:8] in self.prefixes:
          # wich memo 
          rts = vout['script'][10:74]
          # get user name 
          thisUser =  self.memo_user(tx["x"]["inputs"][0]["prev_out"]["addr"])
          # memo type can be reply or like/tip or follow or unfollow or topic message
          MemoType = vout['script'][4:8]
          # check if is our event, not interested in our events notification
          if tx["x"]["inputs"][0]["prev_out"]["addr"] != self.addr:
            # recognize memo type
            if MemoType == "6d03":
              # New event reply to post 
              # tx hash of post wich got a reply
              txHashOfPostWichGotReply = rts.decode("hex")[::-1].encode("hex")
              # check if is our post
              if self.isOurPost(txHashOfPostWichGotReply):
                print colored('[*]', 'green'),("You got a new reply from %s to your post %s" %(thisUser, "https://memo.cash/post/" + str(txHashOfPostWichGotReply)))
                self.notify()

            elif MemoType == "6d04":
              # New event like/tip post
              # tx hash of post wich got like / tip
              txHashOfLikedOrTippedPost = rts.decode("hex")[::-1].encode("hex")
              # check if is our post
              if self.isOurPost(txHashOfLikedOrTippedPost):
                if len(outputs) == 3:
                  thisTippedAmount = outputs[1]["value"]
                  print colored('[*]', 'green'),("You got a %d satoshis tip from %s to your post %s" %(thisTippedAmount ,thisUser, "https://memo.cash/post/" + str(txHashOfLikedOrTippedPost)))
                  self.notify()
                else:
                  print colored('[*]', 'green'),("You got a new like from %s to your post %s" %(thisUser, "https://memo.cash/post/" + str(txHashOfLikedOrTippedPost)))
                  self.notify()
            else:
              pass


if __name__ == '__main__':
  print colored('[*]', 'green'),("Memo.cash Notifiier")
  print colored('[*]', 'green'),("Donations: 1NDMh9VsZAJ3WBKGYSvMtbP4NBzFwK9aJv")
  print 


  if(len(sys.argv) > 1):
    notifier = MemoNotifier(sys.argv[1])
    notifier.Listen()
  print "Usage: python memo.py your legacy address"
  sys.exit("Example: python memo.py 1NDMh9VsZAJ3WBKGYSvMtbP4NBzFwK9aJv")
