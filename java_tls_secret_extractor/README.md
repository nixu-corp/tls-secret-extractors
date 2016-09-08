#Java TLS Secret Extractor
----------
A script to extract TLS secrets from Java debug logs to help in decrypting and debugging TLS-encrypted communications.

The following shows a usage example with [TShark][1]:

1. Run a traffic capture:
	
	`tcpdump -s0 -w traffic.pcap -U -i eth0 &`

2. Run your Java app with the appropriate debug option:

	`timeout 15s java -Djavax.net.debug=all -jar application.jar | tee debug_log.log`

3. Extract the secrets into a [keylog file][2]:

	`./extract_java_master_secrets.py debug_log.log keylog.txt`

4. Feed the keylog file to TShark to view the decrypted content:

	`tshark -o ssl.keylog_file:keylog.txt -o http.ssl.port:443 -x -r traffic.pcap -V | grep -A5 'Decrypted SSL data'`



[1]: https://www.wireshark.org/docs/man-pages/tshark.html
[2]: https://wiki.wireshark.org/SSL#Using_the_.28Pre.29-Master-Secret
