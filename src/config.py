import sys
import json

config = None
with open(sys.argv[1]) as f:
	config = json.loads(f.read())
