import pyaes
#54b23f9b3596397b2acf70a81b2da31d=01f5237dd1a687bf0174f3cf17d2c274

url='01f5237dd1a687bf0174f3cf17d2c274'
magic="1579547dfghuh,09458721242affde,45h4jggf5f6g,f5fg65jj46,eedcfa0489174392".split(',')
decryptor = pyaes.new(magic[1], pyaes.MODE_CBC, IV=magic[4])
url= decryptor.decrypt(url.decode("hex")).split('\0')[0]
print url
