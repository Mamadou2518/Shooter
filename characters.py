import pygame
import settings
import random 

#class pour le joueur qui heritera de 
# la super class sprite comme toute element graphique 
class Player(pygame.sprite.Sprite): 
    def __init__(self,game):
        super().__init__() #init de la super class
        self.game= game
        self.health= 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 5
        self.image= pygame.image.load('assets/player.png')
        #recuperre les coord de l'image
        self.rect=self.image.get_rect()
        self.rect.x=settings.WIDTH/2
        self.rect.y=500
        #ensemble des projectiles lancées vont être rangées dans un group
        self.all_projectiles = pygame.sprite.Group()
    
    def move_right(self):
        #verifier si le joueur n'est pas en collision avec un montre
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    #Instance qui va permettre au joueur de lancer le projectile
    def launch_projectile(self):
        #creer nouvelle instance de la classe projectille
        projectile= Projectile(self)
        #ajouter le projecter dans le groupe de projectiles lancés
        self.all_projectiles.add(projectile)

    def update_health_bar(self,surface):
        #definir couleur jauge de vie
        bar_color =(111, 210, 46)
        #definir bar arrière plan
        back_bar_color =(60, 63, 60)
        #definir position , largeur et épaisseur de la jauge 
        bar_position = [self.rect.x + 50, self.rect.y + 10, self.health, 7]
        back_bar_position = [self.rect.x + 50, self.rect.y + 10, self.max_health, 7]
        #dessiner la barre de vie
        pygame.draw.rect(surface, back_bar_color,back_bar_position)
        pygame.draw.rect(surface, bar_color,bar_position)
    
    def damage(self,amount):
        if self.health - amount > amount:
            self.health-= amount
        else:
            #si le joueur n'a plus de point de vie
            self.game.game_over()


#representation de notre jeu
class Game:
    def __init__(self):
        #definir si le jeu a commencer ou non
        self.is_playing= False        
        # #generer  un joueur
        self.player=Player(self)
        #On creer un GROUP contetnant player pour 
        # ensuite pouvoir l'ulisée dans l'istance collision 
        self.all_players= pygame.sprite.Group()
        self.all_players.add(self.player)
        #boutton pressés (dicctionnaire)
        self.pressed={}
        #Groupe de monstres
        self.all_monsters = pygame.sprite.Group()
        
 
    def start(self):
        self.is_playing = True
        self.spawn_monster()
        self.spawn_monster()
    
    def update(self,screen):
        #appliquer l'imagge du joueur
        screen.blit(self.player.image, self.player.rect)
        #faire apparaitre la barre de vie du joueur
        self.player.update_health_bar(screen)
        #recuperer les projectiles presents dans le groupe projectiles
        for projectile in self.player.all_projectiles:
            projectile.move()
        #appliquer l'ensemble des images de projectiles du groupe projectiles
        self.player.all_projectiles.draw(screen)

        #recuperer les monstres presents dans le groupe groupe monstre
        for monster in self.all_monsters:
            monster.forward()
            #mise à jour de la barre de vie
            monster.update_health_bar(screen)
            

        #appliquer l'ensemble des images de montres du groupe
        self.all_monsters.draw(screen)

        #verifier si le joeur veut aller à gauche ou droite
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x < 900:
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > -25:
            self.player.move_left()
        

        #Instance pour faire apparaitre le monstre
    def spawn_monster(self):
        monster= Monster(self)
        self.all_monsters.add(monster)

    #Instance pour gerer la collision
    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False,pygame.sprite.collide_mask)

    def game_over(self):
        #remettre le jeu à neuf: retirer les monstre, remettre le joueur à 100 point de vie, mettre le jeu en attente
        self.all_monsters = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.is_playing = False


#class qui va gérer le projectile qui va herité les caract de la class sprite
class Projectile (pygame.sprite.Sprite):

    def __init__(self,player):
        super().__init__()
        self.player=player
        self.velocity=5
        self.image=pygame.image.load('assets/projectile.png')
        #redimensionnement de l'image
        self.image=pygame.transform.scale(self.image,(50,50))
        self.rect=self.image.get_rect()
        #placer le projectile au memes coord que ceux du joueur
        self.rect.x= player.rect.x + 120
        self.rect.y = player.rect.y + 80
        #on sauvergarde l'image original car on envigage de le faire tournerne
        self.origin_image=self.image
        self.angle=0

    #instance pour faire tourner le projectile
    def rotate(self):
        self.angle+=12
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        #rotation par rapport au centre
        self.rect = self.image.get_rect(center=self.rect.center)

    #instance de supression
    def remove(self):
        self.player.all_projectiles.remove(self)
        
    #Nouvelle instance pour le mouvement du projectile
    def move(self):
        self.rect.x += self.velocity
        self.rotate()

        #vérifier si le projectil est en collision avec le monstre
        for monster in self.player.game.check_collision(self,self.player.game.all_monsters):
            #supprimer le projectil
            self.remove() 
            #inflinger des degats
            monster.damage(self.player.attack)

        #si le projectile n'est plus present sur l'écran
        if self.rect.x > settings.WIDTH:
            #supprimer le projectile
            self.remove() 
        
#class pour le monstre
class Monster(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__() #init de la super class
        self.game= game
        self.health= 100
        self.max_health = 100
        self.attack = 2
        self.velocity = random.randint(1,3)
        self.image= pygame.image.load('assets/mummy.png')
        self.rect = self.image.get_rect()   
        self.rect.x = 1000 + random.randint(0,300)
        self.rect.y = 525         
    #instance pour faire avancer le monstre
    def forward(self):
        #deplacement possible ssi pas collision avec un joueur
        if not self.game.check_collision(self,self.game.all_players):
            self.rect.x -= self.velocity
        #si collision avec joeur, inflinger degat au joeur
        else:
            
            self.game.player.damage(self.attack)
    #mise à jour de la bar de vie  
    def update_health_bar(self,surface):
        #definir couleur jauge de vie
        bar_color =(111, 210, 46)
        #definir bar arrière plan
        back_bar_color =(60, 63, 60)
        #definir position , largeur et épaisseur de la jauge 
        bar_position = [self.rect.x + 10, self.rect.y - 20, self.health, 5]
        back_bar_position = [self.rect.x + 10, self.rect.y - 20, self.max_health, 5]
        #dessiner la barre de vie
        pygame.draw.rect(surface, back_bar_color,back_bar_position)
        pygame.draw.rect(surface, bar_color,bar_position)
    
    #instance pour inflinger des degat au monstre
    def damage(self, amount): 
        self.health -= amount  
        #verifier si la vie est inf ou egale à 0
        if self.health <=0:
            #faire reaparettre le monstre comme nouveau montre
            self.rect.x= settings.WIDTH + random.randint(0,300)
            #avec la jaune de vie rempli 
            self.health = self.max_health
            self.velocity= random.randint(1,3)



