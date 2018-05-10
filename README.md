# Memo.cash Notifier

This is a simple memo notificator, currently supports notifications for replies and likes/tips, in the next days i will add support for follow && unfollow events, for each new like/tip or reply wich you get to a post a pop-up message will appear to your desktop with text "New memo event" notifications are visible via terminal an example how a notification look like:

``` bash
[*] You got a new reply from homopit to your post https://memo.cash/post/a1b5f8082d652335a3c88bff8a2ae5f42a5787c97af1ab21eafb52c51dd45197
[*] You got a new like/tip from homopit to your post https://memo.cash/post/63b29bc8e17dddef2c70aaf9f25da05e38555b3825be5e0dfa5f0bf8b127ee95
```


# INSTAL Memo.cash Notifier
``` bash
git clone https://github.com/zeus-one/memo.cash-notifier
cd memo.cash-notifier
sudo pip install -r memo_req.txt
```

# Running Memo.cash Notifier
Please use your legacy address, you can find your legacy address in your memo.cash profile by clicking  Show QR code & legacy address 
``` bash
cd memo.cash-notifier
python memo.py your legacy address
Example: python memo.py 1NDMh9VsZAJ3WBKGYSvMtbP4NBzFwK9aJv

```