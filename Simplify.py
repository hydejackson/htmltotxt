#Simplifies song title to quickly pull from list of songs
#params: str title
#return: str simpleTitle
def simplify(title):
    asciiChars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # ~ badChars = '!?@#*- \n'
    # ~ for c in badChars:
        # ~ title = title.replace(c, '')
        # ~ title = title.lower()
        # ~ title = title.replace('seazerbot', '')
        # ~ title = title.replace(' ','')
        # ~ title = title.replace('\n', '')
    title = title.lower()
    title = title.replace('seazerbot', '')
    for c in title:
        if c not in asciiChars:
            title = title.replace(c, '')
    if title == '':
        title = 'somethingjapanese'
    return title
