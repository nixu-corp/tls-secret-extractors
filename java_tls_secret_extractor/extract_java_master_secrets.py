state = ""

while True:
    try:
        line = raw_input()
    except:
        break
    #print("(%s) %s" % (state, line))
    if line.startswith("Client Nonce:"):
        state = "read client random"
        client_random = ""
    elif state == "read client random":
        if line.startswith("Server Nonce:"):
            state = ""
            assert len(client_random) == 64
        else:
            assert line.startswith("00")
            for i in range(16):
                client_random += filter(lambda x: len(x) > 0, line.split(" "))[i + 1]
                
    elif line.startswith("Master Secret:"):
        state = "read master secret"
        master_secret = ""
    elif state == "read master secret":
        if line.startswith("Client MAC write Secret:"):
            state = ""
            assert len(master_secret) == 96
            print("CLIENT_RANDOM %s %s" % (client_random, master_secret))
        else:
            assert line.startswith("00")
            for i in range(16):
                master_secret += filter(lambda x: len(x) > 0, line.split(" "))[i + 1]
                
    elif line.startswith("*** ClientKeyExchange, RSA PreMasterSecret"):
        state = "read encrypted premaster secret after next line"
    elif state == "read encrypted premaster secret after next line":
        assert line.startswith("[write] MD5 and SHA1 hashes:")
        state = "read encrypted premaster secret"
    elif state == "read encrypted premaster secret":
        assert line.startswith("00")
        encrypted_premaster_secret = ""
        for i in range(8):
            encrypted_premaster_secret += filter(lambda x: len(x) > 0, line.split(" "))[i + 7]
        assert len(encrypted_premaster_secret) == 16
        state = ""
        
    elif line.startswith("PreMaster Secret:"):
        state = "read premaster secret"
        premaster_secret = ""
    elif state == "read premaster secret":
        if line.startswith("CONNECTION KEYGEN:"):
            state = ""
            assert len(premaster_secret) in [96, 134]
            try:
                print("RSA %s %s" % (encrypted_premaster_secret, premaster_secret))
            except NameError:
                pass
        else:
            assert line.startswith("00")
            for i in range(16):
                try:
                    premaster_secret += filter(lambda x: len(x) > 0, line.split(" "))[i + 1]
                except IndexError:
                    pass
