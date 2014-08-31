from random import seed, sample
from string import ascii_letters, digits

magic_md5 = '$1$'

def gen_salt( length=8, symbols=ascii_letters + digits ):
    seed()
    return ''.join( sample( symbols, length ) )

#from hashlib import md5
import hashlib



def encrypt_md5( raw_pw, salt, magic=magic_md5 ):
    raw_pw = raw_pw.encode('utf-8')
    salt = salt.encode('utf-8')
    hash = hashlib.md5()
    hash.update( raw_pw + magic + salt )
    st = hashlib.md5()
    st.update( raw_pw + salt + raw_pw)
    stretch = st.digest()

    for i in range( 0, len( raw_pw ) ):
        hash.update( stretch[i % 16] )

    i = len( raw_pw )

    while i:
        if i & 1:
            hash.update('\x00')
        else:
            hash.update( raw_pw[0] )
        i >>= 1

    saltedmd5 = hash.digest()

    for i in range( 1000 ):
        hash = hashlib.md5()

        if i & 1:
            hash.update( raw_pw )
        else:
            hash.update( saltedmd5 )

        if i % 3:
            hash.update( salt )
        if i % 7:
            hash.update( raw_pw )
        if i & 1:
            hash.update( saltedmd5 )
        else:
            hash.update( raw_pw )

        saltedmd5 = hash.digest()

    itoa64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    rearranged = ''
    for a, b, c in ((0, 6, 12), (1, 7, 13), (2, 8, 14), (3, 9, 15), (4, 10, 5)):
        v = ord( saltedmd5[a] ) << 16 | ord( saltedmd5[b] ) << 8 | ord( saltedmd5[c] )

        for i in range(4):
            rearranged += itoa64[v & 0x3f]
            v >>= 6

    v = ord( saltedmd5[11] )

    for i in range( 2 ):
        rearranged += itoa64[v & 0x3f]
        v >>= 6

    return magic + salt + '$' + rearranged
e = raw_input('Insert the password: \n')
print encrypt_md5(e, gen_salt())
#print encrypt_md5('bvGkmwTKaFqws', gen_salt())
