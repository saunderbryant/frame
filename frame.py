#import sys
import pygame
import glob
import random
#import time
import Pillow
from Pillow import Image
import os
import shutil

def run_frame():
    #Initialize the frame and create a screen object
    pygame.init()
    screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
    pygame.mouse.set_visible(0)

    #Set the waiting time
    waittime = 1000
    switchtime = pygame.time.get_ticks()

    #Get background image
    bg_image = pygame.image.load("init.jpg").convert()

    #Draw canvas object
    screen.blit(bg_image, [0, 0])

    #Refresh the screen
    pygame.display.flip()
    done = False
    
    #Get the wallpapers
    wps = get_wallpapers()
    
    while not done:
        #Waits for events
        for event in pygame.event.get():
            #Quits if a quit event is detected
            if event.type == pygame.QUIT:
                done = True

            #Quits if the mouse is clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                done = True


        currenttime = pygame.time.get_ticks()

        if currenttime - switchtime >= waittime:
            switchtime = currenttime
            #Get a random background and print it to the screen
            select_wallpaper(wps)
            bg_image = pygame.image.load('current_img.jpg').convert()
            screen.blit(bg_image, [0, 0])
            pygame.display.flip()
            waittime = random.randint(1, 5) * 60 * 1000

def get_wallpapers():
    files = [f for f in glob.glob('/home/sbs/winshare/**/*', recursive=True) if 'jpg' in f or '.JPG' in f] 
    wallpapers = {}
    i =  0
    for name in files:
        wallpapers[i] = name
        i += 1
    return wallpapers

def select_wallpaper(wallpapers):
    landscape = False
    name = wallpapers[random.randint(0, len(wallpapers.keys()) - 1)]
    im = Image.open(name)
    while landscape == False:
        if im.size[0] < im.size[1]:
            im.close()
            name = wallpapers[random.randint(0, len(wallpapers.keys()) - 1)]
            im = Image.open(name)
        else:
            landscape = True
    resizeimage(name)

def resizeimage(filename):
    #COPY CURRENT IMAGE INTO TEMP IMAGE; USE TRY EXCEPT FOR NEXT BLOCK, IF THROWN, USE OLD IMAGE
    shutil.copyfile(filename, 'temp_img.jpg')
    im = Image.open('temp_img.jpg')
    #Try to save random wallpaper; if it fails, use old image
    try:
        im.convert('RGB')
        im.save('temp_img.jpg')
        shutil.copyfile('temp_img.jpg', 'current_img.jpg')
    except IOError:
        pass
        im = Image.open('current_img.jpg')
        print('shit')

    wpercent = (800 / float(im.size[0]))

    #CHECK HERE TO MAKE SURE THAT HEIGHE IS AT LEAST 480, IF NOT, RESIZE USING HEIGHT
    if wpercent * float(im.size[1]) >= 480:
        hsize = int((float(im.size[1]) * float(wpercent)))
        im = im.resize((800, hsize), Pillow.Image.ANTIALIAS)
    else:
        hpercent = (480 / float(im.size[1]))
        wsize = int((float(im.size[0]) * float(hpercent)))
        im = im.resize((wsize, 480), Pillow.Image.ANTIALIAS)
    if os.path.isfile('current_img.jpg'):
        os.remove('current_img.jpg')
    im.save('current_img.jpg')

run_frame()

#print(resizeimage("02.jpg"))

#wps = get_wallpapers()
#num_wps = len(wps.keys())

#print(wps)


