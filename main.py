import pygame
import math
import settings
import characters

pygame.init()

#generation de fenêtre

pygame.display.set_caption('Comet Fall Game')
screen = pygame.display.set_mode((settings.WIDTH,settings.HEIGHT)) #création de la fenetre
background= pygame.image.load('assets/bg.jpg') #importer image 

#importer et charger la bannière pour l'accueil
banner=pygame.image.load('assets/banner.png') 
#redimensionner le banner
banner= pygame.transform.scale(banner, (500,500))
banner_rect=banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)

#importer et charger le button pour lancer le jeu
play_button=pygame.image.load('assets/button.png')
#redimensionnement
play_button= pygame.transform.scale(play_button, (400,150))
play_button_rect=play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.33)
play_button_rect.y = math.ceil(screen.get_height() / 2)

#charger le jeu
game=characters.Game()


running= True
#Boucle infini pour faire tourner le jeu
while running:
    #appliquer l'arriere plan du jeu
    screen.blit(background,(settings.BG_WIDTH,settings.BG_HEIGHT)) #blit<==(surface,coord)
    
    #vérifier si le jeu a commencer
    if game.is_playing:
        #déclancher les inscructions du jeu
        game.update(screen)
    #vérifier si le jeu est lancé
    else:
        #ajouter l'ecran de bienvenue
        screen.blit(play_button,play_button_rect)
        screen.blit(banner,banner_rect)
    #mettre à jour l'écran pour afficher les images
    pygame.display.flip() 

   

    #si le joueur ferme le jeu
    #on parcours la liste des evements
    for event in pygame.event.get():
        #evenement fermeture
        if event.type == pygame.QUIT:
            running = False # arret de la boucle
            pygame.QUIT() #fermeture de la fenetre
        #detecter si le joueur appui une touche du clavier
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key]=True
            
             #détecter la touche espace pour lancer la boule
            if event.key == pygame.K_SPACE:
                game.player.launch_projectile()
        elif event.type == pygame.KEYUP:
            game.pressed[event.key]=False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Verifier si le click de la souris est en collision avec le button play
            if play_button_rect.collidepoint(event.pos):
                game.start()

       
