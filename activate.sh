#!/usr/bin/env bash

activate_env(){
	if [ ! venv ]; then
		virtualenv -p python3 venv
	fi
	source venv/bin/activate
}
require_package(){
	# only needs to be run on devices with arm architecture
	local architect
	if hash dpkg 2>/dev/null; then
		set architect = $(dpkg --print-architecture)
	else
		set architect = $(uname -m)
	fi
	if [[ `${architect:""}` == "armhf" || `${architect:""}` == "arm64" ]]; then
		sudo apt install libatlas3-base
		sudo apt-get install python3-numpy
	fi
}

is_setup(){
	return $(diff <(pip freeze) <(cat requirements.txt))
}

if [ ! is_setup ]; then
	require_package
	pip install -r requirements.txt
fi

activate_env