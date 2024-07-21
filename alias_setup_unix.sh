#!/usr/bin/env bash

# Find the path to the encryption directory
encryption_dir=$(realpath main.py)

# Set a permanent alias to run the main.py script in the encryption directory. Powershell, zsh & bash
if [ "$SHELL" == "/bin/bash" ]
then
  echo "alias fernet='/bin/python $encryption_dir'" >> ~/.bashrc
elif [ "$SHELL" == "/bin/zsh" ]
then
  echo "alias fernet='/bin/python $encryption_dir'" >> ~/.zshrc
elif [ "$SHELL" == "/usr/bin/pwsh" ]
then
  echo "Set-Alias fernet '/bin/python $encryption_dir'" >> ~/.config/powershell/Microsoft.PowerShell_profile.ps1
fi