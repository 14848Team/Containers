download:
	mkdir -p base_images
	wget -P base_images/ http://www.andrew.cmu.edu/user/ayushagr/basefs.tar.gz

install:
	# Put any compilation instructions here if required
	# Any third party installations shuld also occur here

manager:
	# Put instruction to run your manager here
	sudo ../venv/bin/python server.py

clean:
	# Remove all config files stored by the manager in it's lifetime
	# and kill the manager process
	rm -rf mountables/cabbage
	rm -rf mountables/potato
	rm -rf mountables/tomato
	rm -rf configs
	rm -rf containers
	rm -f index*
	rm -f grading/cli_tests/obtained*

cli_tests: clean
	sudo ./grading/cli_tests/test_1_upload.sh
	sudo ./grading/cli_tests/test_2_cfginfo.sh
	sudo ./grading/cli_tests/test_3_launch.sh
	sudo ./grading/cli_tests/test_4_list.sh
	sudo ./grading/cli_tests/test_5_destroyall.sh
	sudo make clean

api_tests: clean
	python3 grading/rest/grading.py 
	sudo ./cli/destroyall
	sudo make clean
