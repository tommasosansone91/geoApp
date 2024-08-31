## Install python 3.10 and uninstall python 3.12 on Ubuntu 22.04

## Install pyenv on Ubuntu 22.04

### Update and Install Dependencies

    sudo apt-get update && sudo apt-get install make build-essential libssl-dev \
    zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

### Install Pyenv using pyenv-installer

    curl https://pyenv.run | bash

### Configure user profile to use pyenv

Ensure the following is in your ~/.bash_profile (if exists), ~/.profile (for login shells), ~/.bashrc (for interactive shells), or ~/.zshrc

    # Load pyenv automatically by appending
    # the following to 
    # ~/.bash_profile if it exists, otherwise ~/.profile (for login shells)
    # and ~/.bashrc (for interactive shells) :
    
    export PYENV_ROOT="$HOME/.pyenv"
    [[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"

otherwise insert it in .bashrc

    vim ~/.bashrc

### reload bashrc

    source ~/.bashrc

### initialize pyenv 

    eval "$(pyenv virtualenv-init -)"


## Install python 3.10 and uninstall python 3.12 via pyenv

### Install python using pyenv

    pyenv install 3.10

### set the new python version

    pyenv local 3.10

### Remove other python version

    sudo apt-get remove --purge python3.12
