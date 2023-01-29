
def start():
    
    from shutil import move
    from LOGS import logs_setup as logger
    from os import listdir, chdir, getcwd
    from sys import platform
    
    
    dest = input("select working directory:\t")

    #move pyfernet to the new working dir
    move(getcwd(), dest) 
    
    #NOTE: add error handle after changing working dir & move the error to logs
    
    #change directory to new cwd
    if platform == "linux": chdir(f"{getcwd()}/{dest}")
    
    if platform == "win32": chdir(f"{getcwd()}\\{dest}")
    
    if platform == "darwin": chdir(f"{getcwd()}/{dest}")
    
    
    logger.logging.debug(f"current working directory moved: {getcwd()}")