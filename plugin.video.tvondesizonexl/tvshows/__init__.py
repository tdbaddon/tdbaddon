try:
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
except:
    #do nothing
    print 'ssl verified context available'
