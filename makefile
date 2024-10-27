bchoc: bchoc.py block.py blockchain.py commandHandlers.py cryptography.py
	echo '#!/usr/bin/env python3' > bchoc
	cat bchoc.py >> bchoc
	chmod +x bchoc
	dos2unix bchoc

clean:
	rm -f bchoc
