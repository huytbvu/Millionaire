# Who wants to be a Millionaire
# simple version
# by Huy Vu
# 2012
import pygame, random, time
from pygame.locals import *
SCREEN_SIZE = (960,640)

# object to hold 4 options for each quesion
class Option(object):
    def __init__(self,description, position, id, font, color):
        self.position = position
        self.label = font.render(description,True,color)
        self.id = id
        
    def render(self,surface):
        x,y = self.position
        surface.blit(self.label,(x,y))
    
    def mouse_over(self,point):
        x,y = self.position
        px,py = point
        return px>=x and px<x+100 and py>=y and py<y + 20

#########################################
# score equivalent to each level (as in real life TV show)
SCORELEVEL = (100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000)

# indicator of helping option <Polling, 50/50, Change question>
HELP = [False, False, False]
#################################################

# object to hold question: title, options and the right answer
class Question(object):
    
    def __init__(self, title, opt, correct):
        self.__title = title
        self.__opt = opt
        self.__correct = correct
    
    def get_Question(self):
        return self.__title
    
    def get_Choice(self):
        return self.__opt
    
    # get correct answer
    def get_RightAnswer(self):
        return self.__correct
     
    # Audience are sometimes incorrect
    def get_AudienceAnswer(self):
        if random.choice([1,2,3,4,5,6,7,8,9,10]) < 9:
            return self.__correct
        else:
            return self.__opt[random.choice([1,2,3,4])]
#############################################
        
# choose next question from file 
def next_question(file):
    quest = file.readline()
    option = []
    for i in range(4):
        option.append(file.readline())
    correct = file.readline()
    if correct:
        correct = correct[0]
    return quest, option, correct

# display question based on their level and current file
def display_question(level, current, screen):
    screen.fill((255,255,255))
    font = pygame.font.SysFont("aerial", 50, False)
    screen.blit(font.render("question number " + str(level+1),False,(255,255,0)),(10,10));
    x = 50
    y = 50
    w = 40
    opt = {}
    answer = current.get_Choice()
    
    # screen setting
    font = pygame.font.SysFont("aerial", 20, False)
    opt["title"] = Option(current.get_Question()[:-1],(20,y),0,font, (0,0,0))
    font = pygame.font.SysFont("aerial", 40, False)
    opt["opt1"] = Option("1." + answer[0][:-1],(x,y+w),1,font, (0,0,0))
    opt["opt2"] = Option("2." + answer[1][:-1],(x,y+2*w),2,font, (0,0,0))
    opt["opt3"] = Option("3." + answer[2][:-1],(x,y+3*w),3,font, (0,0,0))
    opt["opt4"] = Option("4." + answer[3][:-1],(x,y+4*w),4,font, (0,0,0))
    font = pygame.font.SysFont("time new roman", 30, False)
    opt["quit"] = Option("Stop the game",(x,y+5*w+20),5,font, (255,128,0))
    opt["poll"] = Option("Polling Help",(6*x,y+5*w+20),6,font, (0,128,255))
    opt["fifty"] = Option("50/50 Help",(x,y+6*w+20),7,font, (255,0,0))
    opt["change"] = Option("Change Question",(6*x,y+6*w+20),8,font, (0,255,0))
        
    # draw everything
    for eop in opt.values():
        eop.render(screen)
            
    pygame.display.update()   
    return opt 
    
# create question bank    
def bank(file):
    quest, option, correct = next_question(file)
    bank = []
    while quest:
        curr = Question(quest,option,correct)
        bank.append(curr)
        quest, option, correct = next_question(file)
    return bank    

# display if answer is right
def display_right(level, font, screen):
    screen.fill((255,255,255))
    score = "CORRECT! Your current score is " + str(SCORELEVEL[level])
    screen.blit(font.render(score,False,(0,255,255)),(50,200));
    if level == 14:
        screen.blit(font.render("CONGRATULATION",False,(255,0,0)),(20,300));
        screen.blit(font.render("You are the next millionaire",False,(255,0,0)),(20,370));
    
    pygame.display.update()
    time.sleep(1) 

# display if answer is wrong
def display_wrong(level, font, screen):
    screen.fill((255,255,255))
    screen.blit(font.render("TOO BAD!! You're wrong",False,(100,0,100)),(50,50));
    #print "The Game is Over, you are at level ", level
    if level == 0:
        screen.blit(font.render("Your Score is 0",False,(100,0,100)),(50,250));
    else:
        score = "Your final score is " + str(SCORELEVEL[level-1]/2)
        screen.blit(font.render(score,False,(100,0,100)),(50,250));
        
    pygame.display.update()
    time.sleep(2)  

# display if user quits
def display_quit(level, font, screen):
    screen.fill((255,255,255))
    screen.blit(font.render("You decided to stop",False,(100,0,100)),(50,50));
    if level == 0:
        screen.blit(font.render("Your Score is 0",False,(100,0,100)),(50,250));
    else:
        score = "Your current score is " + str(SCORELEVEL[level-1])
        screen.blit(font.render(score,False,(100,0,100)),(50,250));       
        
    pygame.display.update()
    time.sleep(1)   
        
#############################
# choose questionDB out of 3 possible: easy, medium, hard         
def choose_db(level, easy, medium, hard):        
    current_db = []
    if level < 6:
        current_db = easy
    elif level <11:
        current_db = medium
    else:
        current_db = hard
        
    return current_db
        
                
#############################
# determine user input
# quit - user quits
# 1-4: answer options
# 5: user stops the game
# 6-8: user uses helps        
def determine(font, screen, opt):
    button_pressed = None
    ans = "0"
    while button_pressed is None:
            
        for event in pygame.event.get():
            # detect if user hit "X" button
            if event.type == QUIT:
                ans = "quit"
                return ans
                
            # detect if user hit anything    
            if event.type == MOUSEBUTTONDOWN:
                for buttonname, button in opt.iteritems():
                    if button.mouse_over(event.pos):
                        button_pressed = buttonname
                        font = pygame.font.SysFont("arial_black", 25, False)
                         # if a help-option is already used, user cannot use again
                        if button_pressed == "poll":
                            if HELP[0]:
                                button_pressed = None
                                screen.blit(font.render("You have already used this help",False,(100,0,100)),(10,450));
                                pygame.display.update()
                            else:
                                HELP[0] = True
                        elif button_pressed == "fifty":
                            if HELP[1]:
                                button_pressed = None
                                screen.blit(font.render("You have already used this help",False,(100,0,100)),(10,450));
                                pygame.display.update()
                            else:
                                HELP[1] = True
                        elif button_pressed == "change":
                            if HELP[2]:
                                button_pressed = None
                                screen.blit(font.render("You have already used this help",False,(100,0,100)),(10,450));
                                pygame.display.update()
                            else:
                                HELP[2] = True
                        break;
            
        
        if button_pressed is not None:
                
            if button_pressed == "opt1":
                ans = "1"
            elif button_pressed == "opt2":
                ans = "2"
            elif button_pressed == "opt3":
                ans = "3"
            elif button_pressed == "opt4":
                ans = "4"
            elif button_pressed == "quit":
                ans = "5"
            elif button_pressed == "poll":
                ans = "6"
            elif button_pressed == "fifty":
                ans = "7"
            elif button_pressed == "change":
                ans = "8"
    
    return ans


#############################
def main():
    font = pygame.font.SysFont("default_font", 50, False)
    
    for i in range(15):
        screen.fill((255,255,255))
         
        # get question DB based on level 
        cur_db = choose_db(i, qdbE, qdbM, qdbH)
        # get question randomly from THAT level
        curr = random.choice(cur_db)
            
        # display question
        opt = display_question(i,curr,screen)
        
        # determine answer
        ans = determine(font, screen, opt)
        
        if ans == curr.get_RightAnswer():
            display_right(i, font, screen)
            
        # if user stop the game
        elif ans == "5":
            display_quit(i, font, screen)
            return    
          
        # if "Polling" is used, tell user what most audience think
        elif ans == "6":
            font = pygame.font.SysFont("arial", 25, False)
            screen.blit(font.render("Most audience answer " + curr.get_AudienceAnswer(),False,(100,180,250)),(10,350));
            pygame.display.update()
            ans = determine(font, screen, opt)
            while ans == "7" or ans == "8":
                screen.blit(font.render("You can only use one help per question",False,(100,180,250)),(10,400));
                pygame.display.update()
                HELP[1] = False
                HELP[2] = False
                ans = determine(font, screen, opt)
                
            if ans == curr.get_RightAnswer():
                display_right(i, font, screen)    
            elif ans == "5":
                display_quit(i, font, screen)
                return
            else:
                display_wrong(i, font, screen)
                return
        
        # if "50/50" is used, tell user the INCCORECT answer  
        elif ans == "7":
            avoid = int(curr.get_RightAnswer())
            e_one = avoid + 1
            if e_one > 4:
                e_one -= 4
            e_two = avoid + 2
            if e_two > 4:
                e_two -= 4
            font = pygame.font.SysFont("arial", 25, False)
            msg = "The following answers are NOT right " + str(e_one) + " and " + str(e_two)
            screen.blit(font.render(msg,False,(255,0,0)),(10,350));
            pygame.display.update()
            ans = determine(font, screen, opt)
            while ans == "6" or ans == "8":
                screen.blit(font.render("You can only use one help per question",False,(255,0,0)),(10,400));
                pygame.display.update()
                HELP[0] = False
                HELP[2] = False
                ans = determine(font, screen, opt)
                
            if ans == curr.get_RightAnswer():
                display_right(i, font, screen)    
            elif ans == "5":
                display_quit(i, font, screen)
                return
            else:
                display_wrong(i, font, screen)
                return
            
        # if "Change" is used, change the question
        elif ans == "8":
                
            if i < 6:
                qdbE.remove(curr)
            elif i < 11:
                qdbM.remove(curr)
            else:
                qdbH.remove(curr)
            
            cur_db = choose_db(i, qdbE, qdbM, qdbH)
            curr = random.choice(cur_db)
            screen.fill((255,255,255))
            font = pygame.font.SysFont("verdana", 25, False)
            screen.blit(font.render("You have changed questions. Your new question is ...",False,(0,255,0)),(10,150));
            pygame.display.update()
            time.sleep(2)
            display_question(i,curr, screen)
            ans = determine(font, screen, opt)
            while ans == "6" or ans == "7":
                screen.blit(font.render("You can only use one help per question",False,(0,255,0)),(10,400));
                pygame.display.update()
                HELP[0] = False
                HELP[1] = False
                ans = determine(font, screen, opt)
                
            if ans == curr.get_RightAnswer():
                display_right(i, font, screen)    
            elif ans == "5":
                display_quit(i, font, screen)
                return
            else:
                display_wrong(i, font, screen)
                return
        
        # if user hit "X" then quit
        elif ans == "quit":
            display_quit(i, font, screen)
            return 
        else:
            display_wrong(i, font, screen)
            return    
            
        # remove current question
        if i < 6:
            qdbE.remove(curr)
        elif i < 11:
            qdbM.remove(curr)
        else:
            qdbH.remove(curr)
            
        continue

# Main Program 
# create question from files    
efile = open("questionbankE.txt","r")
mfile = open("questionbankM.txt","r")
hfile = open("questionbankH.txt","r")
qdbE = bank(efile)
qdbM = bank(mfile)
qdbH = bank(hfile)
efile.close()
mfile.close()
hfile.close()

# initialize games
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE,0)    
main()
screen.fill((255,255,255))
font = pygame.font.SysFont("default_font", 50, False)

# if game finished, intruct to exit
exop = Option("Click to exit",(250,220),0,font,(0,0,0))
exop.render(screen)
pygame.display.update()

# while not exit, continue the game
ex = True
while ex:
    for event in pygame.event.get():
        if event.type == QUIT:
            ex = False;
            break;
            
        if event.type == MOUSEBUTTONDOWN:
            if exop.mouse_over(event.pos):
                ex = False;
                break;
