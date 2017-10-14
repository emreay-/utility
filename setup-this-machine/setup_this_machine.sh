#!/bin/bash

endcol="\033[0m"
red="\033[031m"
green="\033[032m"
yellow="\033[033m"
purple="\033[035m"

printc () {
    echo -e $1$2 $endcol    
}

install () {
    printc $green "\nProcess: Install $1...\n"
    sudo apt-get install $1
}

install git
install curl
install trash-cli
install terminator
install caffeine
install tree
install sqlitebrowser 
install meld
install gimp
install gthumb 
install unzip
install htop
install openjdk-8-jre
install openjdk-8-jdk
install python-autopep8
