from ecsdiLAB.ecsdimazon.controllers import Constants
import sys
import requests

def main():
	var = raw_input("ean: ")
	print requests.get("http://127.0.0.1:" + Constants.PORT_AUPDATER)
	


if __name__ == "__main__":
	main()
