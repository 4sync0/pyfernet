
def start():
    
    from shutil import move
    from LOGS import logs_setup as logger
    from os import listdir, chdir, getcwd
    from sys import platform
    
    
    dest = input("select working directory:\t")
    
    
    for sf in listdir():
        move(sf, dest)
    
    
    #except Exception: NotADirectoryError(), logger.logging.error("not a directory")
    
    
    
    #DIRECTORIES VARY ON PLATFORM
    
    if platform == "linux": chdir(f"{getcwd()}/{dest}")
    
    if platform == "win32": chdir(f"{getcwd()}\\{dest}")
    
    if platform == "darwin": chdir(f"{getcwd()}/{dest}")
    
    
    logger.logging.debug(f"current working directory moved: {getcwd()}")