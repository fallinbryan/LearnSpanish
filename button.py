import pygame

class Button:
    '''
    __init__(parent_surface,pygame.Rect,$label,callble_function=None,enabled=True
    '''
    white = (255,255,255)
    gray = (200,200,200)
    gray180 = (180,180,180)
    black = (0,0,0)
    dgray = (100,100,100)
    font = pygame.font.Font('freesansbold.ttf',15)
    
    def __init__(self,surface,rect,label='button',function=None,enabled=True):
        self.rect = rect
        self.label = label
        self.surface = surface
        self.function = function
        self.enabled = enabled
        self.textColor = self.black
        self.bgColor = self.gray
        pygame.draw.rect(self.surface,self.white,self.rect)
        pygame.draw.rect(self.surface,self.bgColor,(self.rect.inflate(-2,-2)).move(1,1))
        pygame.draw.rect(self.surface,self.dgray,self.rect,1)
        if self.enabled:
            self.textSurf = self.font.render(self.label,True,self.textColor)
        else:
            self.textSurf = self.font.render(self.label,True,self.gray180)
        self.textRect = self.textSurf.get_rect()
        self.textRect.center = self.rect.center
        self.surface.blit(self.textSurf,self.textRect)
    def click(self,*args):
        if self.enabled:
            return self.function(*args)
    def buttonDown(self):
        if self.enabled:
            self.isButtonDown = True
            pygame.draw.rect(self.surface,self.white,self.rect)
            pygame.draw.rect(self.surface,self.bgColor,(self.rect.inflate(-2,-2)).move(-1,-1))
            pygame.draw.rect(self.surface,self.dgray,self.rect,1)
            if self.enabled:
                self.textSurf = self.font.render(self.label,True,self.textColor)
            else:
                self.textSurf = self.font.render(self.label,True,self.gray180)
            self.textRect = self.textSurf.get_rect()
            self.textRect.center = self.rect.center
            self.surface.blit(self.textSurf,self.textRect)
    def buttonUp(self):
        if self.enabled:
            self.isButtonDown = False
            pygame.draw.rect(self.surface,self.white,self.rect)
            pygame.draw.rect(self.surface,self.bgColor,(self.rect.inflate(-2,-2)).move(1,1))
            pygame.draw.rect(self.surface,self.dgray,self.rect,1)
            if self.enabled:
                self.textSurf = self.font.render(self.label,True,self.textColor)
            else:
                self.textSurf = self.font.render(self.label,True,self.gray180)
            self.textRect = self.textSurf.get_rect()
            self.textRect.center = self.rect.center
            self.surface.blit(self.textSurf,self.textRect)

    def enable(self):
        self.enabled = True
        pygame.draw.rect(self.surface,self.white,self.rect)
        pygame.draw.rect(self.surface,self.bgColor,(self.rect.inflate(-2,-2)).move(1,1))
        pygame.draw.rect(self.surface,self.dgray,self.rect,1)
        self.textSurf = self.font.render(self.label,True,self.textColor)
        self.surface.blit(self.textSurf,self.textRect)
    def disable(self):
        self.enabled = False
        pygame.draw.rect(self.surface,self.white,self.rect)
        pygame.draw.rect(self.surface,self.bgColor,(self.rect.inflate(-2,-2)).move(1,1))
        pygame.draw.rect(self.surface,self.dgray,self.rect,1)
        self.textSurf = self.font.render(self.label,True,self.gray180)
        self.surface.blit(self.textSurf,self.textRect)
    def toggleEnabled(self):
        self.enabled = not self.enabled

    def setLabel(self,text):
        self.label = text
    


