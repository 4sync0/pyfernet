#!/usr/bin/env bash

# Find the path to the encryption directory
encryption_dir=$(find ~ -type d -name "pyfernet" 2>/dev/null | head -n 1)

# Set a permanent alias to run the main.py script in the encryption directory. Powershell, zsh & bash
if [ "$SHELL" == "/bin/bash" ]
then
  echo "alias fernet='/bin/python $encryption_dir/main.py'" >> ~/.bashrc
elif [ "$SHELL" == "/bin/zsh" ]
then
  echo "alias fernet='/bin/python $encryption_dir/main.py'" >> ~/.zshrc
elif [ "$SHELL" == "/usr/bin/pwsh" ]
then
  echo "Set-Alias fernet '/bin/python $encryption_dir/main.py'" >> ~/.config/powershell/Microsoft.PowerShell_profile.ps1
fi