[docfernet]: https://cryptography.io/en/latest/fernet/# "fernet pip doc"
[repofernet]: https://github.com/Party-Pie/pyfernet "pyfernet github repo"

# pyfernet
### python cryptography fernet    
![fernet encryption jpg](https://cdn.pixabay.com/photo/2015/12/13/15/32/cryptographic-1091257_960_720.jpg)  
<br>
![maintained badge](https://img.shields.io/maintenance/yes/2023?logo=github&logoColor=gold)
![last-commit badge](https://img.shields.io/github/last-commit/Party-Pie/pyfernet?color=gold&logo=github&logoColor=gold)
![discord badge](https://img.shields.io/badge/discord-P4rtyPi5%236988-gold?logo=discord)
![build badge](https://img.shields.io/appveyor/build/Party-Pie/pyfernet?color=gold&label=build&logo=AppVeyor&logoColor=yellow)
<br>
<br>
## What's all this?  
this is a cryptography project built thanks to [the cryptography package](https://pypi.org/project/cryptography/ "cryptography pip package")  
with this project, you can encrypt any file using [fernet][docfernet] 
for more information regarding the fernet package, check [their github repo](https://github.com/fernet "fernet package github repo")  
<br>
## Why use [pyfernet][repofernet]?  
Everyone can encrypt their files using [fernet][docfernet], but you could save all those 20 minutes that would take you to set up the package,
plus the headache you'd get for any error, specially if you don't know what you're doing.  
With [pyfernet][repofernet], you can now do all without wasting time, no knowledge with [python](https://en.wikipedia.org/wiki/Python_(programming_language "python wikipedia")
 or [cryptography](https://en.wikipedia.org/wiki/Cryptography, "cryptography wikipedia") is required  
 With pyfernet, you can encyrpt files, decrypt files, save it in a json file, manage the keys... & weekly updates!  
 <br>
 - [x] Compatibility with Mac, linux & windows
 - [x] frequently updated
 - [x] easy to use  
 - [x] feature-rich
 <br>
 
 ## Installation Guide  
 This section of the readme file is totally dedicated to the installation of [pyfernet][repofernet], if you follow all the stepts, you should get no errors
 during the process.  
 <br>
 1. Make sure you have [python](https://en.wikipedia.org/wiki/Python_(programming_language "python wikipedia") and [pip](https://en.wikipedia.org/wiki/Pip_(package_manager) "pip wikipedia") downloaded, if not, download it [**here**](https://www.python.org/ "python web") <sup>(pip should already come with python)</sup>  
 you can check it by running ```python --version``` and ```pip --version```  
 2. [git](https://git-scm.com/ "git website") is required for this step, so make sure you've it installed, once you have [git](https://git-scm.com/ "git website") and [python](https://www.python.org/ "python website") installed, clone this repository by running the following command:  
 ```git clone https://github.com/Party-Pie/pyfernet.git```  
 3. Now, navigate to the root directory of the repository with this command: ```cd pyfernet```  
 4. Once there, install the package dependencies which are essential:  ```pip install -r requirements.txt```  
 5. And finally, run **main.py**: ```python main.py``` (make sure you're still on the root directory)  
    
 
 You're all done! now, every time you want to use [pyfernet][repofernet] you can do so by running ```fernet``` in your terminal.  
 <br>
 ## **How to use [pyfernet][repofernet]**
 Please read this section, specially if it's your first time using [pyfernet][repofernet] as it contains essential information over how to use this.  
 <br>
 Once you've gone over the [intallation guide](https://github.com/Party-Pie/pyfernet#installation-guide "README.md installation guide"), you may be wondering how to do use this great tool, don't worry, it's nothing complex, infact, it's pretty simple but do read carefully.  
  #### Essential commands (you'd run each time you start another sesion)
 * Firstly, you need to type ```/new``` in order to tell the script which file you're going to be using **during this sesion**
 * Now, you'll have to either **generate the key** (```/genkey```) or, if you already have a key, (```/setkey```). **Note**: each time you close sesion, none of this info. will save, so you'll need to run these last commands again.  
 A key are some words and numbers, joint together, which can be used to decrypt or encrypt files. Each file has a unique key.  
 You can check if there is a key and a file generated/setted running these commands: ```/key``` and ```/file```.  
#### Other important commands  
* You can encrypt files with this self-explanatory command: ```/encrypt``` & to decrypt: ```/decrypt```  
* You could also change the current working directory with the ```/changedir``` command, and check it with the ```cwd``` command  
* **to save encrypted files and keys**, you'll have to follow this steps:  
   * 1st, save it running the ```/save``` command, this will save the key and file you have encrypted **during that same sesion**  
   * Then, you can either **load it directly** -> ```/load```, or **save it to a json file** -> ```/tojson``` <sup>(saved in ~encryption/storage.json)</sup>  
   **In order to delete** the content inside the files where these files & their keys are saved, you'd need to run: ```/destroydict```  
* You can also **view the debug and error logs** by typing ```/logs``` & destroy it with the ```/relogs``` command  
* You can **view info about the sesion** running this following command ```/sesion```, **you need to have generated a key during that same sesion**  
* Another little thing you can do is **deleting the variables** during that same sesion, to do so, type: ```/delvars```  
* In order to **exit**, you should run, ```/exit```, or hold ctrl+C, but that's only recommended if the script froze.  
* Another **pretty important** command, would be: ```/update```. This, not only **checks if your [pyfernet][repofernet] clone is outdated and updates it**, but it also does a customized and simple backup of certain files (storage.json, logs.log & true.txt)
<br>

#### Multifernet encryption  
This new feature allows you to encrypt files using several keys instead of just one.  
There's no change in commands, just **start** it using the ```/multi -s``` command & **quit** the multifernet mode with: ```/multi -q```  
But first, there are some things you need to **take into account**:
* If you type the ```/setkey``` command, you'll only type the **keys separated by** <sub>space</sub>**and**<sub>space</sub> else the key won'tsave correctly into the list
* This multifernet implementation into [pyfernet][repofernet] is pretty new and recent, so **you may experience some bugs** while using it, please report any problem in [issues](https://github.com/Party-Pie/pyfernet/issues "pyfernet issues tab")

<br>
<sup>That'd be all for now, appreciate taking your time in reading this</sup>
  
Made with love, by PartyPie
