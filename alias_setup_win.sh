$encryption_dir = Get-ChildItem -Path ~ -Directory -Filter "pyfernet" -Recurse | Select-Object -First 1

if ($env:SHELL -eq "/bin/bash") {
  Add-Content -Path $PROFILE -Value "function fernet { & '/bin/python' '$encryption_dir/main.py' }"

}
elseif ($env:SHELL -eq "/bin/zsh") {
  Add-Content -Path $PROFILE -Value "function fernet { & '/bin/python' '$encryption_dir/main.py' }"

}
elseif ($env:SHELL -eq "/usr/bin/pwsh") {
  Add-Content -Path $PROFILE -Value "function fernet { & '/bin/python' '$encryption_dir/main.py' }"
}