text=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'!\"#%&()*,.¨/:;?@^_+<=>¢£§€"
key1=" icolapxstvybjeruknfhqg;dzw>FAUTCYOLVJDZINQKSEHG<.1PB523406789-¨_&m@:\"*(#WM§^,¢/?!)%X'R+€£="
key2=" torbiudfhgzcvanqyepskx¢1w;RC>GHAPND<VUBLIKJETOYXM2QF63405789-¨§)\"j?,m#*@.Z£!W+^/&(:1_S%=€'"
key3=" hrnctqlpsxwogiekzaufyd+b;¢SARYO>QIUX<GFDLJVTHNP1Z3KC7405689-¨§£(mv/Wj@#?MB€&.%!^\"*,2)E:'=_"
key4=" sneohkbufd;rxtaywiqpzl%c¢+E>SPNRKLG1XYCUDV<HOIQ2B4JA805679-¨§£€*jg^.v?@/ZF=\"N:&!m#W3(T,_')"

decipher_me = "Xhch utod Aharst catd gtc Ra;kfem >ohlltf ta (TUJ£YSN056{Aharst N;kt+asfta O£44¨}("
keys = [key1, key2, key3, key4]

for key in keys:
    new_text=''
    for c in decipher_me:
        new_text+=(text[key.find(c, )])
    print(new_text)