#!/usr/bin/env bash

endcol="\033[0m"
red="\033[031m"
green="\033[032m"
yellow="\033[033m"
purple="\033[035m"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DEPENDENCIES=(git curl trash-cli terminator caffeine tree sqlitebrowser
              meld gimp gthumb unzip htop openjdk-8-jre openjdk-8-jdk)
ARG=$1

printc () {
    echo -e $1$2 $endcol
}

install () {
    printc $green "\nProcess: Install $1...\n"
    sudo apt-get install $1
}

install_list () {
    local -n dep_list=$1
    for dep in "${dep_list[@]}"
    do
        install $dep
    done
}

install_atom () {
    printc $yellow "\nProcess: Install Atom...\n"
    wget -O $HOME/Downloads/atom.deb https://atom.io/download/deb
    sudo dpkg --install $HOME/Downloads/atom.deb
}

install_vscode () {
    printc $yellow "\nProcess: Install VSCode...\n"
    wget -O $HOME/Downloads/vscode.deb https://go.microsoft.com/fwlink/?LinkID=760868
    sudo dpkg -i $HOME/Downloads/vscode.deb
    sudo apt-get install -f
}

install_anaconda () {
    printc $yellow "\nProcess: Install Anaconda 3...\n"
    wget -O $HOME/Downloads/anaconda3.sh https://repo.continuum.io/archive/Anaconda3-5.0.0.1-Linux-x86_64.sh
    bash $HOME/Downloads/anaconda3.sh
}

customize_shrc () {
    printc $green "\nProcess: Customize .*shrc ...\n"
    install zsh
    sudo chsh -s $(which zsh)

    sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"

    truncate -s 0 $HOME/.bashrc
    cat $DIR/custom_shrc >> $HOME/.bashrc
    echo "source $HOME/.bashrc" >> $HOME/.zshrc

    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $HOME/
    echo "source ${(q-)PWD}/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ${ZDOTDIR:-$HOME}/.zshrc

    printc $yellow "\nREMEMBER: Activate the higlight plugin in .zshrc by \nplugins=( [plugins...] zsh-syntax-highlighting)\n"
    printc $yellow "\nTHEN, close and reopen a new terminal"
}

install_ros () {
    sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
    sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
    sudo apt-get update
    install ros-kinetic-desktop-full
    sudo rosdep init
    rosdep update
    echo "source /opt/ros/kinetic/setup.bash" >> $HOME/.bashrc
    local DEP=(python-rosinstall python-rosinstall-generator python-wstool build-essential)
    install_list DEP
    mkdir -p $HOME/catkin_ws/src
    printc $yellow '\ncatkin_ws is created, create and setup the environment manually (run catkin_make, source setup.bash etc.)\n'
}

if [ "$ARG" == "dep" ]; then
  install_list DEPENDENCIES
elif [ "$ARG" == "ros" ]; then
  install_ros
elif [ "$ARG" == "anaconda_only" ]; then
  install_anaconda
elif [ "$ARG" == "shell" ]; then
  install_list DEPENDENCIES
  customize_shrc
elif [ "$ARG" == "full" ]; then
  install_list DEPENDENCIES
  customize_shrc
  install_anaconda
  install_atom
  install_vscode
  install_ros
else
  printc $purple "\n $ARG is not a valid command\n"
fi
