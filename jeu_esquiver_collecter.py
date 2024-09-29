# Importation du module os pour interagir avec le système d'exploitation
import os
import pygame  # Importer la bibliothèque 'Pygame' pour le développement de jeux.
import random  # Importer le module 'random' pour la génération de formes aléatoires.
import sys  # Importer le module 'sys' pour permettre la fermeture propre du programme.

# Chargement des ressources :

# Comment charger des images et des sons.
# Organisation des ressources dans le projet.
def resource_path(relative_path):
    """ Obtenez le chemin absolu vers la ressource, fonctionne pour le développement et pour PyInstaller """
    try:
        # PyInstaller crée un dossier temporaire et stocke le chemin dans _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Initialisation de 'Pygame' et du 'mixer' pour le son.
pygame.init()
pygame.mixer.init()

# Charger la musique de fond
music_path = resource_path('background_jeu.ogg')
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)  # Jouer la musique en boucle indéfiniment.

# Charger le son "Thank You"
thank_you_sound_path = resource_path('music_fin.ogg')
thank_you_sound = pygame.mixer.Sound(thank_you_sound_path)

# Charger le son "GAME OVER"
game_over_sound = pygame.mixer.Sound(resource_path('game-over2.wav'))

# Charger les sons pour les interactions
collision_aide_sound_path = resource_path('collision_aide.ogg')
collision_obstacle_sound_path = resource_path('collision_obstacle.ogg')
collision_aide_sound = pygame.mixer.Sound(collision_aide_sound_path)
collision_obstacle_sound = pygame.mixer.Sound(collision_obstacle_sound_path)

# Charger la musique de fin de jeu
fin_jeu_music_path = resource_path('fin_jeu.ogg')
fin_jeu_music = pygame.mixer.Sound(fin_jeu_music_path)

# Définition des dimensions de l'écran en pixels.
LARGEUR_ECRAN, HAUTEUR_ECRAN = 940, 680

# Charger l'icône
icon_path = resource_path('icone.ico')
icon_image = pygame.image.load(icon_path)
pygame.display.set_icon(icon_image)

# Création de l'écran de jeu
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Esquiver et collecter version expert")

# Chargement et redimensionnement des images
player_image_path = resource_path('image_joueur4.png')
player_image = pygame.image.load(player_image_path).convert_alpha()
player_image = pygame.transform.scale(player_image, (70, 70))

# Charger les images des obstacles pour chaque niveau
obstacle_images = [
    pygame.image.load(resource_path('image_obstacle_niveau1.png')).convert_alpha(),
    pygame.image.load(resource_path('image_obstacle_niveau2.png')).convert_alpha(),
    pygame.image.load(resource_path('image_obstacle_niveau3.png')).convert_alpha(),
    pygame.image.load(resource_path('image_obstacle_niveau4.png')).convert_alpha()
]

aid_image_path = resource_path('image_aide.png')
aid_image = pygame.image.load(aid_image_path).convert_alpha()
aid_image = pygame.transform.scale(aid_image, (30, 30))

# Charger les images de fond pour chaque niveau
background_images = [
    pygame.image.load(resource_path('background_niveau1.png')).convert(),
    pygame.image.load(resource_path('background_niveau2.png')).convert(),
    pygame.image.load(resource_path('background_niveau3.png')).convert(),
    pygame.image.load(resource_path('background_niveau4.png')).convert()
]

# Charger l'image de fin de jeu et la redimensionner
end_game_image_path = resource_path('end_game_image.png')
end_game_image = pygame.image.load(end_game_image_path).convert_alpha()
end_game_image = pygame.transform.scale(end_game_image, (400, 300))

# Choix de la police pour le texte affiché sur l'écran
font = pygame.font.Font(None, 40)
end_font = pygame.font.Font(None, 60)

# Fonction pour ajuster la difficulté en fonction du score du joueur
def ajuster_difficulte(score):
    if score < 50:
        return 2000, 3000, 1, "Niveau 1", background_images[0], obstacle_images[0]
    elif score < 100:
        return 1500, 2500, 1.5, "Niveau 2", background_images[1], obstacle_images[1]
    elif score < 150:
        return 1000, 2000, 2, "Niveau 3", background_images[2], obstacle_images[2]
    else:
        return 500, 1500, 2.5, "Niveau 4", background_images[3], obstacle_images[3]

# Classes pour les sprites
class Mobile(pygame.sprite.Sprite):
    def __init__(self, image, vitesse_chute, niveau):
        super().__init__()
        self.image = pygame.transform.scale(image, (30, 30 if image == aid_image else 40))
        self.rect = self.image.get_rect()
        self.vitesse_chute = vitesse_chute
        self.direction = 'bas'

        if niveau == "Niveau 4":
            # Déterminer de manière aléatoire si l'obstacle apparaît à gauche, à droite ou en haut
            self.direction = random.choice(['gauche', 'droite', 'bas'])
            if self.direction == 'gauche':
                self.rect.x = -self.rect.width
                self.rect.y = random.randint(0, HAUTEUR_ECRAN - self.rect.height)
            elif self.direction == 'droite':
                self.rect.x = LARGEUR_ECRAN
                self.rect.y = random.randint(0, HAUTEUR_ECRAN - self.rect.height)
            else:
                self.rect.x = random.randint(0, LARGEUR_ECRAN - self.rect.width)
                self.rect.y = -self.rect.height
        else:
            self.rect.x = random.randint(0, LARGEUR_ECRAN - self.rect.width)
            self.rect.y = -self.rect.height

    def update(self):
        if self.direction == 'gauche':
            self.rect.x += self.vitesse_chute
        elif self.direction == 'droite':
            self.rect.x -= self.vitesse_chute
        else:
            self.rect.y += self.vitesse_chute

        if self.rect.top > HAUTEUR_ECRAN or self.rect.left > LARGEUR_ECRAN or self.rect.right < 0:
            self.kill()

class Joueur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(player_image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = (LARGEUR_ECRAN // 2, HAUTEUR_ECRAN - 50)
        self.score = 0

    def update(self, direction=None):
        if direction == 'gauche':
            self.rect.x -= 5 if self.rect.x > 0 else 0
        elif direction == 'droite':
            self.rect.x += 5 if self.rect.x < LARGEUR_ECRAN - self.rect.width else 0
        elif direction == 'haut':
            self.rect.y -= 5 if self.rect.y > 0 else 0
        elif direction == 'bas':
            self.rect.y += 5 if self.rect.y < HAUTEUR_ECRAN - self.rect.height else 0

def ask_replay():
    replay_text = font.render("Appuyez 'R' pour Rejouer ou 'Q' pour Quitter", True, (255, 255, 255))
    ecran.blit(replay_text, (LARGEUR_ECRAN // 2 - replay_text.get_width() // 2, HAUTEUR_ECRAN // 2 + 50))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    show_thank_you()

def show_thank_you():
    pygame.mixer.music.stop()  # Arrêter la musique de fond
    thank_you_sound.play()  # Jouer le son de remerciement
    thank_you_text = font.render("Merci d'avoir joué à notre jeu aujourd'hui, à bientôt", True, (0, 255, 0))
    ecran.fill((0, 0, 0))  # Fond noir
    ecran.blit(thank_you_text, (LARGEUR_ECRAN // 2 - thank_you_text.get_width() // 2, HAUTEUR_ECRAN // 8))
    pygame.display.flip()
    pygame.time.wait(10000)
    pygame.quit()
    sys.exit()

# Fonction pour afficher l'écran de fin de jeu avec un effet de fondu et le texte de relance
def show_end_game():
    pygame.mixer.music.stop()  # Arrêter la musique de fond
    fin_jeu_music.play()  # Jouer la musique de fin de jeu
    alpha = 0
    end_game_image.set_alpha(alpha)
    ecran.fill((0, 0, 0))  # Fond noir
    end_text = end_font.render("Vous avez réussi à finir le jeu, félicitation !", True, (0, 255, 0))
    replay_prompt_text = font.render("Super, voulez-vous rejouer ? Appuyez sur 'R'", True, (255, 255, 255))
    while alpha < 255:
        ecran.fill((0, 0, 0))
        end_game_image.set_alpha(alpha)
        ecran.blit(end_game_image, (LARGEUR_ECRAN // 2 - end_game_image.get_width() // 2, HAUTEUR_ECRAN // 2 - end_game_image.get_height() // 2 - 20))
        ecran.blit(end_text, (LARGEUR_ECRAN // 2 - end_text.get_width() // 2, HAUTEUR_ECRAN // 2 + end_game_image.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(100)  # Ajuster pour contrôler la vitesse du fondu
        alpha += 5

    # Effet de fondu pour le texte de relance
    alpha = 0
    while alpha < 255:
        ecran.fill((0, 0, 0))
        end_game_image.set_alpha(255)  # Image de fin de jeu déjà visible
        ecran.blit(end_game_image, (LARGEUR_ECRAN // 2 - end_game_image.get_width() // 2, HAUTEUR_ECRAN // 2 - end_game_image.get_height() // 2 - 20))
        ecran.blit(end_text, (LARGEUR_ECRAN // 2 - end_text.get_width() // 2, HAUTEUR_ECRAN // 2 + end_game_image.get_height() // 2))
        replay_prompt_surface = font.render("Super, voulez-vous rejouer? Appuyez sur 'R'", True, (255, 255, 255))
        replay_prompt_surface.set_alpha(alpha)
        ecran.blit(replay_prompt_surface, (LARGEUR_ECRAN // 2 - replay_prompt_surface.get_width() // 2, HAUTEUR_ECRAN // 2 + end_game_image.get_height() // 2 + 60))
        pygame.display.flip()
        pygame.time.wait(100)  # Ajuster pour contrôler la vitesse du fondu
        alpha += 5

    start_time = pygame.time.get_ticks()
    waiting_for_replay = True
    while waiting_for_replay:
        current_time = pygame.time.get_ticks()
        if current_time - start_time > 30000:  # 30000 milliseconds = 30 seconds
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    fin_jeu_music.stop()  # Arrêter la musique de fin de jeu
                    pygame.mixer.music.load(music_path)  # Recharger la musique de fond initiale
                    pygame.mixer.music.play(-1)  # Jouer la musique de fond en boucle
                    main()
                    return

def game_over(joueur):
    game_over_sound.play()
    pygame.time.wait(500)
    game_over_text = font.render("GAME OVER", True, (255, 255, 255))
    ecran.blit(game_over_text, (LARGEUR_ECRAN // 2 - game_over_text.get_width() // 2, HAUTEUR_ECRAN // 2 - 30))
    final_score_text = font.render(f"Score final : {joueur.score} points", True, (255, 255, 255))
    ecran.blit(final_score_text, (LARGEUR_ECRAN // 2 - final_score_text.get_width() // 2, HAUTEUR_ECRAN // 2 + 10))
    pygame.display.flip()
    pygame.time.wait(2000)
    if not ask_replay():
        pygame.quit()
        sys.exit()

def main():
    global ecran  # Déclarez ecran comme variable globale pour pouvoir la modifier
    joueur = Joueur()
    obstacles = pygame.sprite.Group()
    aides = pygame.sprite.Group()
    tous_sprites = pygame.sprite.Group(joueur)
    clock = pygame.time.Clock()
    dernier_temps_obstacle = dernier_temps_aide = pygame.time.get_ticks()
    image_fond = background_images[0]  # Image de fond initiale
    obstacle_image = obstacle_images[0]  # Image des obstacles initiale
    niveau = "Niveau 1"
    plein_ecran = False  # Variable pour suivre l'état du plein écran

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:  # Appuyer sur 'f' pour entrer ou sortir du plein écran
                    plein_ecran = not plein_ecran
                    if plein_ecran:
                        ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.FULLSCREEN)
                    else:
                        ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            joueur.update('gauche')
        elif keys[pygame.K_RIGHT]:
            joueur.update('droite')
        elif keys[pygame.K_UP]:
            joueur.update('haut')
        elif keys[pygame.K_DOWN]:
            joueur.update('bas')

        temps_actuel = pygame.time.get_ticks()
        intervalle_obstacle, intervalle_aide, vitesse_chute, niveau, nouvelle_image_fond, nouvelle_obstacle_image = ajuster_difficulte(joueur.score)
        if nouvelle_image_fond != image_fond:
            image_fond = nouvelle_image_fond
        if nouvelle_obstacle_image != obstacle_image:
            obstacle_image = nouvelle_obstacle_image

        if temps_actuel - dernier_temps_obstacle > intervalle_obstacle:
            obstacle = Mobile(obstacle_image, vitesse_chute, niveau)
            obstacles.add(obstacle)
            tous_sprites.add(obstacle)
            dernier_temps_obstacle = temps_actuel

        if temps_actuel - dernier_temps_aide > intervalle_aide:
            aide = Mobile(aid_image, vitesse_chute, niveau)
            aides.add(aide)
            tous_sprites.add(aide)
            dernier_temps_aide = temps_actuel

        tous_sprites.update()
        if pygame.sprite.spritecollideany(joueur, obstacles):
            collision_obstacle_sound.play()
            game_over(joueur)
            joueur = Joueur()
            obstacles.empty()
            aides.empty()
            tous_sprites = pygame.sprite.Group(joueur)

        bonus_collide = pygame.sprite.spritecollide(joueur, aides, True)
        if bonus_collide:
            collision_aide_sound.play()
            joueur.score += 5 * len(bonus_collide)

        ecran.blit(image_fond, (0, 0))  # Afficher l'image de fond actuelle
        tous_sprites.draw(ecran)
        score_text = font.render(f"Score : {joueur.score} - {niveau}", True, (255, 255, 255))
        ecran.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(60)

        if joueur.score >= 155:
            show_end_game()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
