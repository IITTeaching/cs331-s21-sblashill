import urllib
import requests


def book_to_words(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    booktxt = urllib.request.urlopen(book_url).read().decode()
    bookascii = booktxt.encode('ascii','replace')
    return bookascii.split()


def radix_a_book(book_url='https://www.gutenberg.org/files/84/84-0.txt'):

    # turn url inot usable byte objects
    keys = book_to_words(book_url)
    nkeys = []

    # create lists of ascii values
    for key in keys:
        nkey = []
        for digit in key:
            nkey.append(digit)
        nkeys.append(nkey)

    # fill lists to uniform lengths
    fill = max( len(x) for x in nkeys )
    for nkey in nkeys:
        while True:
            if len(nkey) != fill:
                nkey.insert(0, 0)
            else:
                break

    #buckets and sort
    for idx in range(fill - 1, -1, -1): # loop through each index
        buckets = {}
        for key in range(0,256): # create buckets
            buckets[key] = []
        for nkey in nkeys: # append each ascii to right bucket
            buckets[nkey[idx]].append(nkey)           
        nkeys = []
        for bucket in buckets: # create new nkeys based on bucket order
            for nkey in buckets[bucket]:
                nkeys.append(nkey)

    #remove zeros
    for nkey in nkeys:
        while True:
            if nkey[0] == 0:
                del nkey[idx]
            else:
                break

    # remerge into usable form
    key = []
    keylist = []
    for nkey in nkeys:
        for car in nkey:
            key.append(chr(car))
        keylist.append("".join(key).encode("ascii"))
        key = []
    return keylist
    

def main():

    radix_a_book()

if __name__ == '__main__':
    main()