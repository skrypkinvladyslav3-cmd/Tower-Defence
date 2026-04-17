import pygame
import math
import random
import json
# Это позволит игре сохранять данные в правильное место на телефоне
import os

if 'ANDROID_ARGUMENT' in os.environ:
    # Путь для Android
    SAVE_FILE = os.path.join(os.environ['PYTHON_SERVICE_ARGUMENT'], 'savegame.json')
else:
    # Путь для ПК (Mac/Windows)
    SAVE_FILE = "savegame.json"

def load_progress():
    default_save = {
        "diamonds": 5000,
        "unlocked_towers": ["BASIC"],
        "equipped_towers": ["BASIC"],
        "unlocked_gadgets": [],
        "equipped_gadgets": [],
        "used_codes": []
    }
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for key in default_save:
                    if key not in data:
                        data[key] = default_save[key]
                return data
        except:
            pass
    return default_save


def save_progress(diamonds, unlocked, equipped, unl_gadgets, eq_gadgets, codes):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "diamonds": diamonds,
            "unlocked_towers": unlocked,
            "equipped_towers": equipped,
            "unlocked_gadgets": unl_gadgets,
            "equipped_gadgets": eq_gadgets,
            "used_codes": codes
        }, f)


# --- 1. Game Settings ---
pygame.init()

WIDTH, HEIGHT = 800, 600
PANEL_HEIGHT = 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TOWER DEFENSE - BY VLAD")
try:
    pygame.display.set_icon(pygame.image.load("Снимок экрана 2026-04-11 в 19.38.38.png"))
except:
    pass

# Base Colors
RED = (220, 20, 60)
TOWER_GUN = (192, 192, 192)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL_BG = (30, 30, 40)
BTN_COLOR = (30, 180, 70)
BTN_HOVER = (50, 220, 90)
BTN_DISABLED = (100, 100, 100)
SHOP_COLOR = (70, 100, 180)
SHOP_HOVER = (100, 140, 220)
EXIT_COLOR = (200, 50, 50)
EXIT_HOVER = (240, 70, 70)
PURPLE = (147, 112, 219)
GOLD = (255, 215, 0)

RARITY_COLORS = {
    "COMMON": (180, 180, 180),
    "RARE": (50, 150, 255),
    "EPIC": (200, 50, 255),
    "LEGENDARY": GOLD
}

# --- Maps and Decorations Settings ---
MAPS = [
    {
        "name": "FOREST",
        "bg_color": (34, 139, 34),
        "path": [(0, 300), (200, 300), (200, 100), (600, 100), (600, 400), (800, 400)],
        "path_color": (210, 180, 140),
        "path_outline": (139, 69, 19),
        "decorations": []
    },
    {
        "name": "DESERT",
        "bg_color": (237, 201, 175),
        "path": [(0, 150), (300, 150), (300, 450), (550, 450), (550, 250), (800, 250)],
        "path_color": (210, 180, 140),
        "path_outline": (184, 134, 11),
        "decorations": [
            ("cactus", 150, 300), ("rock", 650, 350), ("cactus", 450, 150),
            ("rock", 200, 50), ("cactus", 100, 400), ("rock", 700, 100)
        ]
    },
    {
        "name": "WINTER",
        "bg_color": (240, 248, 255),
        "path": [(0, 400), (150, 400), (150, 150), (450, 150), (450, 400), (650, 400), (650, 150), (800, 150)],
        "path_color": (176, 224, 230),
        "path_outline": (135, 206, 235),
        "decorations": [
            ("pine", 250, 250), ("snowman", 550, 250), ("pine", 80, 100),
            ("snowman", 300, 450), ("pine", 700, 300)
        ]
    }
]

CURRENT_MAP = MAPS[0]
TILE_SIZE = 40
STATE = "MENU"

# Fonts (initialized later)
font_tiny = None

# --- Global lists for effects ---
PARTICLES = []
FLOATING_TEXTS = []

# --- Tower Stats ---
TOWER_TYPES = {
    "BASIC": {"name": "Basic", "cost": 50, "range": 180, "damage": 15, "cooldown": 20, "color": (150, 150, 150),
              "unlock_cost": 0, "rarity": "COMMON"},
    "RAPID": {"name": "Rapid", "cost": 75, "range": 120, "damage": 5, "cooldown": 5, "color": (200, 100, 100),
              "unlock_cost": 100, "rarity": "COMMON"},
    "WIND": {"name": "Wind", "cost": 100, "range": 200, "damage": 10, "cooldown": 8, "color": (150, 255, 255),
             "unlock_cost": 300, "rarity": "COMMON"},
    "SNIPER": {"name": "Sniper", "cost": 120, "range": 350, "damage": 60, "cooldown": 60, "color": (50, 50, 180),
               "unlock_cost": 250, "rarity": "RARE"},
    "CANNON": {"name": "Cannon", "cost": 150, "range": 150, "damage": 40, "cooldown": 45, "color": (80, 80, 80),
               "unlock_cost": 400, "rarity": "RARE"},
    "ICE": {"name": "Ice", "cost": 100, "range": 160, "damage": 5, "cooldown": 15, "color": (0, 200, 255),
            "unlock_cost": 600, "rarity": "RARE"},
    "POISON": {"name": "Poison", "cost": 180, "range": 140, "damage": 2, "cooldown": 8, "color": (50, 200, 50),
               "unlock_cost": 800, "rarity": "RARE"},
    "FIRE": {"name": "Fire", "cost": 200, "range": 150, "damage": 25, "cooldown": 15, "color": (255, 140, 0),
             "unlock_cost": 1000, "rarity": "RARE"},
    "LASER": {"name": "Laser", "cost": 250, "range": 200, "damage": 2, "cooldown": 1, "color": (255, 50, 50),
              "unlock_cost": 1200, "rarity": "EPIC"},
    "ELECTRIC": {"name": "Electro", "cost": 300, "range": 170, "damage": 25, "cooldown": 12, "color": (255, 255, 0),
                 "unlock_cost": 1500, "rarity": "EPIC"},
    "EARTH": {"name": "Earth", "cost": 350, "range": 130, "damage": 120, "cooldown": 55, "color": (139, 69, 19),
              "unlock_cost": 1800, "rarity": "EPIC"},
    "PLASMA": {"name": "Plasma", "cost": 400, "range": 250, "damage": 100, "cooldown": 50, "color": (200, 50, 255),
               "unlock_cost": 2000, "rarity": "EPIC"},
    "MAGIC": {"name": "Magic", "cost": 500, "range": 220, "damage": 80, "cooldown": 25, "color": (255, 105, 180),
              "unlock_cost": 2500, "rarity": "LEGENDARY"},
    "NUCLEAR": {"name": "Nuclear", "cost": 600, "range": 300, "damage": 250, "cooldown": 90, "color": (50, 255, 50),
                "unlock_cost": 3000, "rarity": "LEGENDARY"},
    "BLACK_HOLE": {"name": "Black Hole", "cost": 1000, "range": 400, "damage": 600, "cooldown": 150, "color": (30, 30, 30),
                   "unlock_cost": 5000, "rarity": "LEGENDARY"}
}

# --- Gadgets ---
GADGET_TYPES = {
    "WEALTH": {"name": "Wealth", "desc": "+$200 at start", "unlock_cost": 800, "color": (50, 200, 50),
               "rarity": "COMMON"},
    "HEALTH": {"name": "Health", "desc": "+5 Lives", "unlock_cost": 1200, "color": RED, "rarity": "RARE"},
    "POWER": {"name": "Power", "desc": "+10% All Dmg", "unlock_cost": 2500, "color": PURPLE, "rarity": "EPIC"},
    "G_BASIC": {"name": "Upgraded Barrel", "desc": "Basic: +10 Dmg", "unlock_cost": 500, "color": (150, 150, 150),
                "rarity": "COMMON"},
    "G_RAPID": {"name": "Cooling", "desc": "Rapid: -2s CD", "unlock_cost": 800, "color": (200, 100, 100),
                "rarity": "COMMON"},
    "G_WIND": {"name": "Hurricane", "desc": "Wind: +50 Rng", "unlock_cost": 1000, "color": (150, 255, 255),
               "rarity": "COMMON"},
    "G_SNIPER": {"name": "Heavy Bullets", "desc": "Sniper: +40 Dmg", "unlock_cost": 1200, "color": (50, 50, 180),
                 "rarity": "RARE"},
    "G_CANNON": {"name": "Super Gunpowder", "desc": "Cannon: +20 Dmg", "unlock_cost": 1500, "color": (80, 80, 80),
                 "rarity": "RARE"},
    "G_ICE": {"name": "Cryo Generator", "desc": "Ice: Slow x2", "unlock_cost": 1800, "color": (0, 200, 255),
              "rarity": "RARE"},
    "G_POISON": {"name": "Toxicity", "desc": "Poison: Long Psn", "unlock_cost": 2000, "color": (50, 200, 50),
                 "rarity": "RARE"},
    "G_FIRE": {"name": "Napalm", "desc": "Fire: Long Burn", "unlock_cost": 2200, "color": (255, 140, 0),
               "rarity": "RARE"},
    "G_LASER": {"name": "Focus", "desc": "Laser: +2 Dmg", "unlock_cost": 2500, "color": (255, 50, 50),
                "rarity": "EPIC"},
    "G_ELECTRIC": {"name": "Short Circuit", "desc": "Electro: -4s CD", "unlock_cost": 3000, "color": (255, 255, 0),
                   "rarity": "EPIC"},
    "G_EARTH": {"name": "Earthquake", "desc": "Earth: Long Slow", "unlock_cost": 3500, "color": (139, 69, 19),
                "rarity": "EPIC"},
    "G_PLASMA": {"name": "Superplasma", "desc": "Plasma: +50 Rng", "unlock_cost": 4000, "color": (200, 50, 255),
                 "rarity": "EPIC"},
    "G_MAGIC": {"name": "Ancient Runes", "desc": "Magic: +40 Dmg", "unlock_cost": 4500, "color": (255, 105, 180),
                "rarity": "LEGENDARY"},
    "G_NUCLEAR": {"name": "Uranium-235", "desc": "Nuclear: -20s CD", "unlock_cost": 5000, "color": (50, 255, 50),
                  "rarity": "LEGENDARY"},
    "G_BLACK_HOLE": {"name": "Singularity", "desc": "B. Hole: +400 Dmg", "unlock_cost": 8000, "color": (30, 30, 30),
                     "rarity": "LEGENDARY"}
}


# --- Effect Classes ---
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 4)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.timer = random.randint(15, 30)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.timer -= 1

    def draw(self, surface):
        if self.timer > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), max(1, self.timer // 6))


class FloatingText:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.timer = 40
        self.vy = -1.5

    def update(self):
        self.y += self.vy
        self.timer -= 1

    def draw(self, surface):
        if self.timer > 0 and font_tiny:
            # Make text transparent over time
            text_surf = font_tiny.render(self.text, True, self.color)
            alpha = max(0, min(255, int((self.timer / 40) * 255)))
            text_surf.set_alpha(alpha)
            surface.blit(text_surf, (int(self.x), int(self.y)))


# --- Classes ---
class Enemy:
    def __init__(self, wave):
        self.path = CURRENT_MAP["path"]
        self.target_waypoint = 1
        self.x, self.y = self.path[0]

        # Chance for BOSS to spawn every 5th wave
        if wave % 5 == 0 and random.random() < 0.15:  # 15% chance for a boss on waves 5, 10, 15, etc.
            self.type = "BOSS"
            self.color = PURPLE
            self.base_speed = 1.0 + (wave * 0.05)
            self.max_health = 1000 + (wave * 150)
            self.radius = 25
            self.reward = 150
        else:
            rand = random.random()
            if rand < 0.2:
                self.type = "FAST"
                self.color = (255, 140, 0)
                self.base_speed = 3.5 + (wave * 0.2)
                self.max_health = 50 + (wave * 15)
                self.radius = 10
                self.reward = 15
            elif rand < 0.4:
                self.type = "TANK"
                self.color = (120, 120, 120)
                self.base_speed = 1.0 + (wave * 0.1)
                self.max_health = 250 + (wave * 40)
                self.radius = 18
                self.reward = 40
            else:
                self.type = "NORMAL"
                self.color = RED
                self.base_speed = 2.0 + (wave * 0.15)
                self.max_health = 100 + (wave * 25)
                self.radius = 14
                self.reward = 20

        self.health = self.max_health
        self.slow_timer = 0
        self.poison_timer = 0
        self.burn_timer = 0

    def update(self):
        current_speed = self.base_speed
        if self.slow_timer > 0:
            current_speed *= 0.4
            self.slow_timer -= 1
        if self.poison_timer > 0:
            self.health -= 0.2
            self.poison_timer -= 1
            if random.random() < 0.2:
                PARTICLES.append(Particle(self.x, self.y, (50, 200, 50)))
        if self.burn_timer > 0:
            self.health -= 0.5
            self.burn_timer -= 1
            if random.random() < 0.2:
                PARTICLES.append(Particle(self.x, self.y, (255, 100, 0)))

        if self.target_waypoint < len(self.path):
            target_x, target_y = self.path[self.target_waypoint]
            dx, dy = target_x - self.x, target_y - self.y
            dist = math.hypot(dx, dy)
            if dist < current_speed:
                self.target_waypoint += 1
            else:
                self.x += (dx / dist) * current_speed
                self.y += (dy / dist) * current_speed

    def draw(self, surface):
        # Shadow
        pygame.draw.circle(surface, (60, 60, 60), (int(self.x + 3), int(self.y + 3)), self.radius)
        # Outline
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius + 2)

        # Draw spikes if it's a boss
        if self.type == "BOSS":
            for i in range(8):
                angle = i * (math.pi / 4)
                px = self.x + math.cos(angle) * (self.radius + 5)
                py = self.y + math.sin(angle) * (self.radius + 5)
                pygame.draw.circle(surface, BLACK, (int(px), int(py)), 4)

        # Body
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

        # Status indicators
        if self.slow_timer > 0:
            pygame.draw.circle(surface, (0, 255, 255), (int(self.x), int(self.y)), self.radius + 4, 2)
        if self.poison_timer > 0:
            pygame.draw.circle(surface, (50, 200, 50), (int(self.x), int(self.y)), self.radius + 7, 2)
        if self.burn_timer > 0:
            pygame.draw.circle(surface, (255, 100, 0), (int(self.x), int(self.y)), self.radius + 5, 2)

        # Health bar
        if self.health > 0 and self.health < self.max_health:
            health_ratio = self.health / self.max_health
            bar_width = 30 if self.type != "BOSS" else 50
            y_offset = self.radius + 10

            pygame.draw.rect(surface, BLACK, (self.x - bar_width // 2 - 1, self.y - y_offset - 4, bar_width + 2, 7))
            pygame.draw.rect(surface, RED, (self.x - bar_width // 2, self.y - y_offset - 3, bar_width, 5))
            pygame.draw.rect(surface, (0, 255, 0),
                             (self.x - bar_width // 2, self.y - y_offset - 3, bar_width * health_ratio, 5))


class Tower:
    def __init__(self, x, y, tower_type, dmg_multiplier=1.0, equipped_gadgets=None):
        if equipped_gadgets is None:
            equipped_gadgets = []

        self.x = x
        self.y = y
        self.type = tower_type
        stats = TOWER_TYPES[tower_type]
        self.cost = stats["cost"]
        self.range = stats["range"]
        self.damage = stats["damage"] * dmg_multiplier
        self.cooldown = stats["cooldown"]
        self.color = stats["color"]
        self.current_cooldown = 0
        self.angle = 0
        self.level = 1
        self.upgrade_cost = int(self.cost * 0.8)

        self.ice_slow_dur = 60
        self.poison_dur = 120
        self.fire_dur = 90
        self.earth_slow_dur = 20

        # Apply gadgets
        if self.type == "BASIC" and "G_BASIC" in equipped_gadgets:
            self.damage += 10
        elif self.type == "RAPID" and "G_RAPID" in equipped_gadgets:
            self.cooldown = max(1, self.cooldown - 2)
        elif self.type == "WIND" and "G_WIND" in equipped_gadgets:
            self.range += 50
        elif self.type == "SNIPER" and "G_SNIPER" in equipped_gadgets:
            self.damage += 40
        elif self.type == "CANNON" and "G_CANNON" in equipped_gadgets:
            self.damage += 20
        elif self.type == "ICE" and "G_ICE" in equipped_gadgets:
            self.ice_slow_dur = 120
        elif self.type == "POISON" and "G_POISON" in equipped_gadgets:
            self.poison_dur = 240
        elif self.type == "FIRE" and "G_FIRE" in equipped_gadgets:
            self.fire_dur = 180
        elif self.type == "LASER" and "G_LASER" in equipped_gadgets:
            self.damage += 2
        elif self.type == "ELECTRIC" and "G_ELECTRIC" in equipped_gadgets:
            self.cooldown = max(1, self.cooldown - 4)
        elif self.type == "EARTH" and "G_EARTH" in equipped_gadgets:
            self.earth_slow_dur = 60
        elif self.type == "PLASMA" and "G_PLASMA" in equipped_gadgets:
            self.range += 50
        elif self.type == "MAGIC" and "G_MAGIC" in equipped_gadgets:
            self.damage += 40
        elif self.type == "NUCLEAR" and "G_NUCLEAR" in equipped_gadgets:
            self.cooldown = max(10, self.cooldown - 20)
        elif self.type == "BLACK_HOLE" and "G_BLACK_HOLE" in equipped_gadgets:
            self.damage += 400

    def upgrade(self):
        self.level += 1
        self.damage = int(self.damage * 1.5)
        self.range = int(self.range * 1.15)
        self.upgrade_cost = int(self.upgrade_cost * 1.5)
        FLOATING_TEXTS.append(FloatingText(self.x - 10, self.y - 20, "LVL UP!", YELLOW))

    def draw(self, surface):
        pygame.draw.circle(surface, (60, 60, 60), (self.x + 5, self.y + 5), 20)
        pygame.draw.circle(surface, (40, 40, 40), (self.x, self.y), 20)
        pygame.draw.circle(surface, (100, 100, 100), (self.x, self.y), 16)

        gun_color = TOWER_GUN
        end_x = self.x + math.cos(self.angle) * 24
        end_y = self.y + math.sin(self.angle) * 24

        if self.type == "SNIPER":
            end_x = self.x + math.cos(self.angle) * 34
            end_y = self.y + math.sin(self.angle) * 34
            pygame.draw.line(surface, (50, 50, 50), (self.x, self.y), (end_x, end_y), 5)
            pygame.draw.line(surface, gun_color, (self.x, self.y), (end_x, end_y), 3)
        elif self.type == "CANNON":
            pygame.draw.line(surface, (40, 40, 40), (self.x, self.y), (end_x, end_y), 11)
            pygame.draw.line(surface, gun_color, (self.x, self.y), (end_x, end_y), 7)
        elif self.type == "RAPID":
            off_x = math.cos(self.angle + math.pi / 2) * 4
            off_y = math.sin(self.angle + math.pi / 2) * 4
            pygame.draw.line(surface, gun_color, (self.x + off_x, self.y + off_y), (end_x + off_x, end_y + off_y), 4)
            pygame.draw.line(surface, gun_color, (self.x - off_x, self.y - off_y), (end_x - off_x, end_y - off_y), 4)
        elif self.type in ["LASER", "PLASMA"]:
            pygame.draw.line(surface, gun_color, (self.x, self.y), (end_x, end_y), 4)
            pygame.draw.circle(surface, self.color, (int(end_x), int(end_y)), 7)
            pygame.draw.circle(surface, WHITE, (int(end_x), int(end_y)), 3)
        elif self.type == "ELECTRIC":
            pygame.draw.line(surface, (50, 50, 50), (self.x, self.y), (end_x, end_y), 6)
            pygame.draw.line(surface, self.color, (self.x, self.y), (end_x, end_y), 3)
        elif self.type == "NUCLEAR":
            pygame.draw.line(surface, (30, 80, 30), (self.x, self.y), (end_x, end_y), 14)
            pygame.draw.line(surface, self.color, (self.x, self.y), (end_x, end_y), 4)
        elif self.type == "WIND":
            pygame.draw.line(surface, (200, 255, 255), (self.x, self.y), (end_x, end_y), 5)
            pygame.draw.circle(surface, WHITE, (int(end_x), int(end_y)), 4)
        elif self.type == "FIRE":
            pygame.draw.line(surface, (200, 50, 0), (self.x, self.y), (end_x, end_y), 8)
            pygame.draw.line(surface, (255, 150, 0), (self.x, self.y), (end_x, end_y), 4)
        elif self.type == "EARTH":
            pygame.draw.line(surface, (80, 40, 10), (self.x, self.y), (end_x, end_y), 12)
            pygame.draw.line(surface, (139, 69, 19), (self.x, self.y), (end_x, end_y), 8)
        elif self.type == "MAGIC":
            pygame.draw.line(surface, (255, 105, 180), (self.x, self.y), (end_x, end_y), 6)
            pygame.draw.circle(surface, (255, 20, 147), (int(end_x), int(end_y)), 8)
        elif self.type == "BLACK_HOLE":
            pygame.draw.circle(surface, (150, 0, 255), (self.x, self.y), 15)
            pygame.draw.circle(surface, BLACK, (self.x, self.y), 10)
        else:
            pygame.draw.line(surface, (50, 50, 50), (self.x, self.y), (end_x, end_y), 8)
            pygame.draw.line(surface, gun_color, (self.x, self.y), (end_x, end_y), 5)

        if self.type != "BLACK_HOLE":
            pygame.draw.circle(surface, (30, 30, 30), (self.x, self.y), 12)
            pygame.draw.circle(surface, self.color, (self.x, self.y), 10)
            pygame.draw.circle(surface, WHITE, (self.x - 3, self.y - 3), 3)

        if self.level > 1:
            lvl_font = pygame.font.SysFont("Arial", 12, bold=True)
            surface.blit(lvl_font.render(str(self.level), True, YELLOW), (self.x + 8, self.y + 8))

    def attack(self, enemies, surface):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

        for enemy in enemies:
            dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
            if dist <= self.range:
                self.angle = math.atan2(enemy.y - self.y, enemy.x - self.x)
                if self.current_cooldown <= 0:
                    actual_damage = self.damage
                    enemy.health -= actual_damage
                    self.current_cooldown = self.cooldown

                    # Create floating damage text
                    if random.random() > 0.5:  # Don't show every bullet for rapid towers to avoid clutter
                        FLOATING_TEXTS.append(
                            FloatingText(enemy.x + random.randint(-10, 10), enemy.y - 20, str(int(actual_damage)),
                                         WHITE))

                    if self.type == "ICE":
                        enemy.slow_timer = max(enemy.slow_timer, self.ice_slow_dur)
                    elif self.type == "POISON":
                        enemy.poison_timer = max(enemy.poison_timer, self.poison_dur)
                    elif self.type == "FIRE":
                        enemy.burn_timer = max(enemy.burn_timer, self.fire_dur)
                    elif self.type == "EARTH":
                        enemy.slow_timer = max(enemy.slow_timer, self.earth_slow_dur)

                    flash_color = YELLOW
                    if self.type in ["LASER", "FIRE"]:
                        flash_color = RED
                    elif self.type in ["ICE", "WIND"]:
                        flash_color = (0, 255, 255)
                    elif self.type in ["PLASMA", "MAGIC"]:
                        flash_color = PURPLE
                    elif self.type == "POISON":
                        flash_color = (50, 200, 50)
                    elif self.type == "ELECTRIC":
                        flash_color = YELLOW
                    elif self.type == "NUCLEAR":
                        flash_color = (50, 255, 50)
                    elif self.type == "BLACK_HOLE":
                        flash_color = (100, 0, 200)

                    # Draw beam
                    if self.type != "BLACK_HOLE":
                        pygame.draw.line(surface, flash_color, (self.x, self.y), (enemy.x, enemy.y), 3)
                    else:
                        pygame.draw.line(surface, flash_color, (self.x, self.y), (enemy.x, enemy.y), 8)

                    # Add sparks (particles)
                    for _ in range(3 if self.type != "NUCLEAR" else 15):
                        PARTICLES.append(Particle(enemy.x, enemy.y, flash_color))

                    end_x = self.x + math.cos(self.angle) * 24
                    end_y = self.y + math.sin(self.angle) * 24
                    pygame.draw.circle(surface, WHITE, (int(end_x), int(end_y)), 6)
                break


# --- Helper Functions ---
def draw_grid(surface):
    for x in range(0, WIDTH, TILE_SIZE):
        pygame.draw.line(surface, (255, 255, 255, 30), (x, 0), (x, HEIGHT - PANEL_HEIGHT))
    for y in range(0, HEIGHT - PANEL_HEIGHT, TILE_SIZE):
        pygame.draw.line(surface, (255, 255, 255, 30), (0, y), (WIDTH, y))


def draw_decorations(surface, decorations):
    for dec_type, x, y in decorations:
        if dec_type == "tree":
            pygame.draw.rect(surface, (139, 69, 19), (x - 6, y, 12, 20))
            pygame.draw.circle(surface, (0, 100, 0), (x, y - 5), 18)
            pygame.draw.circle(surface, (34, 139, 34), (x - 8, y + 2), 12)
            pygame.draw.circle(surface, (34, 139, 34), (x + 8, y + 2), 12)
        elif dec_type == "bush":
            pygame.draw.circle(surface, (46, 139, 87), (x, y), 14)
            pygame.draw.circle(surface, (34, 139, 34), (x + 10, y + 5), 10)
            pygame.draw.circle(surface, (60, 179, 113), (x - 8, y + 8), 12)
        elif dec_type == "cactus":
            pygame.draw.rect(surface, (46, 139, 87), (x - 8, y - 20, 16, 40), border_radius=8)
            pygame.draw.rect(surface, (46, 139, 87), (x - 18, y - 5, 12, 10), border_radius=4)
            pygame.draw.rect(surface, (46, 139, 87), (x + 6, y - 15, 12, 10), border_radius=4)
            pygame.draw.line(surface, (0, 50, 0), (x, y), (x + 10, y - 5), 1)
            pygame.draw.line(surface, (0, 50, 0), (x, y - 10), (x - 10, y - 15), 1)
        elif dec_type == "rock":
            pygame.draw.circle(surface, (105, 105, 105), (x, y), 15)
            pygame.draw.circle(surface, (128, 128, 128), (x + 8, y + 5), 10)
            pygame.draw.circle(surface, (169, 169, 169), (x - 5, y + 8), 12)
        elif dec_type == "pine":
            pygame.draw.rect(surface, (101, 67, 33), (x - 4, y + 10, 8, 15))
            pygame.draw.polygon(surface, (46, 139, 87), [(x, y - 20), (x - 15, y + 5), (x + 15, y + 5)])
            pygame.draw.polygon(surface, (34, 139, 34), [(x, y - 5), (x - 18, y + 15), (x + 18, y + 15)])
        elif dec_type == "snowman":
            pygame.draw.circle(surface, WHITE, (x, y + 15), 16)
            pygame.draw.circle(surface, WHITE, (x, y), 12)
            pygame.draw.circle(surface, WHITE, (x, y - 12), 10)
            pygame.draw.circle(surface, BLACK, (x - 3, y - 14), 2)
            pygame.draw.circle(surface, BLACK, (x + 3, y - 14), 2)
            pygame.draw.polygon(surface, (255, 140, 0), [(x, y - 10), (x, y - 12), (x + 8, y - 10)])


def draw_map(surface):
    surface.fill(CURRENT_MAP["bg_color"])
    grid_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    draw_grid(grid_surface)
    surface.blit(grid_surface, (0, 0))
    path = CURRENT_MAP["path"]
    pygame.draw.lines(surface, CURRENT_MAP["path_outline"], False, path, 46)
    pygame.draw.lines(surface, CURRENT_MAP["path_color"], False, path, 38)
    draw_decorations(surface, CURRENT_MAP["decorations"])


def is_on_path(x, y):
    road_width = 25
    path = CURRENT_MAP["path"]
    for i in range(len(path) - 1):
        p1, p2 = path[i], path[i + 1]
        min_x, max_x = min(p1[0], p2[0]) - road_width, max(p1[0], p2[0]) + road_width
        min_y, max_y = min(p1[1], p2[1]) - road_width, max(p1[1], p2[1]) + road_width
        if min_x <= x <= max_x and min_y <= y <= max_y: return True
    return False


def is_on_decoration(x, y):
    for dec_type, dx, dy in CURRENT_MAP["decorations"]:
        if math.hypot(x - dx, y - dy) < 25: return True
    return False


def draw_interactive_button(surface, rect, text, font, normal_color, hover_color, is_hovered):
    current_color = hover_color if is_hovered else normal_color
    if is_hovered:
        pygame.draw.rect(surface, WHITE, rect.inflate(6, 6), 2, border_radius=12)
    pygame.draw.rect(surface, current_color, rect, border_radius=10)
    pygame.draw.rect(surface, (255, 255, 255, 50), rect, 2, border_radius=10)
    text_surf = font.render(text, True, WHITE)
    surface.blit(text_surf, text_surf.get_rect(center=rect.center))


def draw_diamond(surface, x, y, width=16, height=22):
    points = [(x, y - height // 2), (x + width // 2, y), (x, y + height // 2), (x - width // 2, y)]
    pygame.draw.polygon(surface, (0, 255, 255), points)
    pygame.draw.polygon(surface, WHITE, points, 2)


def get_random_item_from_box(box_type):
    rand = random.random()
    if box_type == "NORMAL":
        if rand < 0.65:
            rarity = "COMMON"
        elif rand < 0.90:
            rarity = "RARE"
        elif rand < 0.98:
            rarity = "EPIC"
        else:
            rarity = "LEGENDARY"
    else:
        if rand < 0.25:
            rarity = "RARE"
        elif rand < 0.75:
            rarity = "EPIC"
        else:
            rarity = "LEGENDARY"

    pool = []
    for k, v in TOWER_TYPES.items():
        if v["rarity"] == rarity: pool.append(("TOWER", k))
    for k, v in GADGET_TYPES.items():
        if v["rarity"] == rarity: pool.append(("GADGET", k))

    if not pool: pool = [("TOWER", list(TOWER_TYPES.keys())[0])]
    return random.choice(pool)


# --- Main Function ---
def main():
    global STATE, CURRENT_MAP, font_tiny, PARTICLES, FLOATING_TEXTS
    clock = pygame.time.Clock()

    font_title = pygame.font.SysFont("Arial", 50, bold=True)
    font_large = pygame.font.SysFont("Arial", 36, bold=True)
    font_small = pygame.font.SysFont("Arial", 22, bold=True)
    font_mini = pygame.font.SysFont("Arial", 16, bold=True)
    font_tiny = pygame.font.SysFont("Arial", 14, bold=True)

    save_data = load_progress()
    diamonds = save_data["diamonds"]
    unlocked_towers = save_data["unlocked_towers"]
    equipped_towers = save_data["equipped_towers"]
    unlocked_gadgets = save_data["unlocked_gadgets"]
    equipped_gadgets = save_data["equipped_gadgets"]
    used_codes = save_data["used_codes"]

    enemies, towers = [], []
    occupied_cells = set()
    money, wave, enemies_spawned, spawn_timer = 400, 1, 0, 0
    lives = 10
    wave_active = False
    dmg_mult = 1.0

    if not equipped_towers: equipped_towers = ["BASIC"]
    selected_tower = equipped_towers[0]
    selected_placed_tower = None
    active_input, input_text = False, ""
    shop_tab = "GADGETS"
    menu_backpack_tab = "TOWERS"

    anim_ticks = 0
    won_item_type = None
    won_item_id = None
    won_duplicate = False
    won_compensation = 0
    current_box_type = None

    # UI Rectangles
    play_btn_rect = pygame.Rect(WIDTH // 2 - 150, 180, 300, 60)
    menu_shop_btn_rect = pygame.Rect(WIDTH // 2 - 150, 260, 300, 60)
    menu_backpack_btn_rect = pygame.Rect(WIDTH // 2 - 150, 340, 300, 60)
    exit_btn_rect = pygame.Rect(WIDTH // 2 - 150, 420, 300, 60)
    game_btn_rect = pygame.Rect(WIDTH - 190, HEIGHT - 80, 170, 60)
    in_game_backpack_btn_rect = pygame.Rect(WIDTH - 380, HEIGHT - 80, 170, 60)
    promo_rect = pygame.Rect(WIDTH // 2 - 260, 550, 250, 40)
    back_to_menu_rect_shop = pygame.Rect(WIDTH // 2 + 10, 550, 250, 40)
    back_to_menu_rect_bp = pygame.Rect(WIDTH // 2 - 125, 550, 250, 40)
    back_to_game_rect = pygame.Rect(WIDTH // 2 - 150, 550, 300, 40)
    game_to_menu_rect = pygame.Rect(20, 20, 120, 40)
    game_over_menu_rect = pygame.Rect(WIDTH // 2 - 150, 400, 300, 60)
    claim_btn_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
    tab_gadgets_rect = pygame.Rect(WIDTH // 2 - 190, 60, 180, 40)
    tab_boxes_rect = pygame.Rect(WIDTH // 2 + 10, 60, 180, 40)
    tab_bp_towers_rect = pygame.Rect(WIDTH // 2 - 190, 60, 180, 40)
    tab_bp_gadgets_rect = pygame.Rect(WIDTH // 2 + 10, 60, 180, 40)

    item_slots = []
    card_w, card_h = 140, 135
    start_x, start_y = 30, 110
    for i, t_type in enumerate(TOWER_TYPES.keys()):
        rect = pygame.Rect(start_x + (i % 5) * 148, start_y + (i // 5) * 145, card_w, card_h)
        item_slots.append({"type": t_type, "rect": rect})

    gadget_slots = []
    g_w, g_h = 180, 80
    g_start_x, g_start_y = 20, 105
    for i, g_type in enumerate(GADGET_TYPES.keys()):
        col = i % 4
        row = i // 4
        rect = pygame.Rect(g_start_x + col * (g_w + 10), g_start_y + row * (g_h + 8), g_w, g_h)
        gadget_slots.append({"type": g_type, "rect": rect})

    box_normal_rect = pygame.Rect(WIDTH // 2 - 250, 200, 200, 250)
    box_premium_rect = pygame.Rect(WIDTH // 2 + 50, 200, 200, 250)

    def save_all():
        save_progress(diamonds, unlocked_towers, equipped_towers, unlocked_gadgets, equipped_gadgets, used_codes)

    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        upgrade_btn_rect = sell_btn_rect = pygame.Rect(0, 0, 0, 0)

        if selected_placed_tower:
            t = selected_placed_tower
            px, py = t.x + 20, t.y - 40
            if px + 140 > WIDTH: px = t.x - 140 - 20
            if py + 90 > HEIGHT - PANEL_HEIGHT: py = HEIGHT - PANEL_HEIGHT - 90
            upgrade_btn_rect = pygame.Rect(px + 10, py + 25, 120, 25)
            sell_btn_rect = pygame.Rect(px + 10, py + 55, 120, 25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_all()
                running = False

            if event.type == pygame.KEYDOWN:
                if STATE == "MENU_SHOP" and active_input:
                    if event.key == pygame.K_RETURN:
                        code = input_text.upper()
                        if code == "AZURI" and "AZURI" not in used_codes:
                            diamonds += 67
                            used_codes.append("AZURI")
                        elif code == "artishok" and "artishok" not in used_codes:
                            diamonds += 100
                            used_codes.append("artishok")






                        save_all()
                        input_text = ""
                        active_input = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if len(input_text) < 15:
                            input_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if STATE == "MENU":
                    if play_btn_rect.collidepoint(mx, my):
                        CURRENT_MAP = random.choice(MAPS)
                        enemies, towers, occupied_cells = [], [], set()
                        PARTICLES.clear()
                        FLOATING_TEXTS.clear()
                        money, wave, enemies_spawned, wave_active = 400, 1, 0, False
                        lives = 10
                        dmg_mult = 1.0

                        if "WEALTH" in equipped_gadgets: money += 200
                        if "HEALTH" in equipped_gadgets: lives += 5
                        if "POWER" in equipped_gadgets: dmg_mult = 1.1

                        selected_tower = equipped_towers[0] if equipped_towers else "BASIC"
                        selected_placed_tower = None
                        STATE = "GAME"
                    elif menu_shop_btn_rect.collidepoint(mx, my):
                        STATE = "MENU_SHOP"
                    elif menu_backpack_btn_rect.collidepoint(mx, my):
                        STATE = "MENU_BACKPACK"
                    elif exit_btn_rect.collidepoint(mx, my):
                        save_all()
                        running = False

                elif STATE == "GAME":
                    if game_to_menu_rect.collidepoint(mx, my):
                        save_all()
                        STATE = "MENU"
                        selected_placed_tower = None
                    elif game_btn_rect.collidepoint(mx, my) and not wave_active:
                        wave_active = True
                        selected_placed_tower = None
                    elif in_game_backpack_btn_rect.collidepoint(mx, my):
                        STATE = "IN_GAME_BACKPACK"
                        selected_placed_tower = None
                    else:
                        clicked_in_popup = False
                        if selected_placed_tower:
                            if upgrade_btn_rect.collidepoint(mx, my):
                                clicked_in_popup = True
                                if money >= selected_placed_tower.upgrade_cost:
                                    money -= selected_placed_tower.upgrade_cost
                                    selected_placed_tower.upgrade()
                            elif sell_btn_rect.collidepoint(mx, my):
                                clicked_in_popup = True
                                refund = int((selected_placed_tower.cost + (
                                    selected_placed_tower.upgrade_cost if selected_placed_tower.level > 1 else 0)) * 0.5)
                                money += refund
                                occupied_cells.remove((selected_placed_tower.x, selected_placed_tower.y))
                                towers.remove(selected_placed_tower)
                                FLOATING_TEXTS.append(
                                    FloatingText(selected_placed_tower.x, selected_placed_tower.y, f"+${refund}",
                                                 YELLOW))
                                selected_placed_tower = None

                        if not clicked_in_popup:
                            selected_placed_tower = None
                            clicked_tower = None
                            for t in towers:
                                if math.hypot(mx - t.x, my - t.y) < 20:
                                    clicked_tower = t
                                    break

                            if clicked_tower:
                                selected_placed_tower = clicked_tower
                            elif my < HEIGHT - PANEL_HEIGHT:
                                grid_x, grid_y = (mx // TILE_SIZE) * TILE_SIZE + 20, (my // TILE_SIZE) * TILE_SIZE + 20
                                if (grid_x, grid_y) not in occupied_cells and not is_on_path(grid_x,
                                                                                             grid_y) and not is_on_decoration(
                                        grid_x, grid_y):
                                    cost = TOWER_TYPES[selected_tower]["cost"]
                                    if money >= cost:
                                        towers.append(Tower(grid_x, grid_y, selected_tower, dmg_mult, equipped_gadgets))
                                        occupied_cells.add((grid_x, grid_y))
                                        money -= cost
                                        # Dust on build
                                        for _ in range(10): PARTICLES.append(Particle(grid_x, grid_y, (150, 150, 150)))

                elif STATE == "MENU_SHOP":
                    active_input = promo_rect.collidepoint(mx, my)
                    if back_to_menu_rect_shop.collidepoint(mx, my):
                        save_all()
                        STATE = "MENU"
                        active_input = False

                    if tab_gadgets_rect.collidepoint(mx, my):
                        shop_tab = "GADGETS"
                    elif tab_boxes_rect.collidepoint(mx, my):
                        shop_tab = "BOXES"

                    if shop_tab == "GADGETS":
                        for slot in gadget_slots:
                            rect = slot["rect"]
                            act_rect = pygame.Rect(rect.x + 8, rect.bottom - 26, rect.width - 16, 20)
                            if act_rect.collidepoint(mx, my):
                                g_type = slot["type"]
                                if g_type not in unlocked_gadgets and diamonds >= GADGET_TYPES[g_type]["unlock_cost"]:
                                    diamonds -= GADGET_TYPES[g_type]["unlock_cost"]
                                    unlocked_gadgets.append(g_type)
                                    save_all()
                    elif shop_tab == "BOXES":
                        if box_normal_rect.collidepoint(mx, my) and diamonds >= 500:
                            diamonds -= 500
                            current_box_type = "NORMAL"
                            won_item_type, won_item_id = get_random_item_from_box("NORMAL")
                            anim_ticks = 0
                            STATE = "BOX_ANIMATION"
                        elif box_premium_rect.collidepoint(mx, my) and diamonds >= 2000:
                            diamonds -= 2000
                            current_box_type = "PREMIUM"
                            won_item_type, won_item_id = get_random_item_from_box("PREMIUM")
                            anim_ticks = 0
                            STATE = "BOX_ANIMATION"

                        if STATE == "BOX_ANIMATION":
                            if won_item_type == "TOWER":
                                won_duplicate = won_item_id in unlocked_towers
                                won_compensation = TOWER_TYPES[won_item_id]["unlock_cost"] // 2 if won_duplicate else 0
                                if not won_duplicate: unlocked_towers.append(won_item_id)
                            else:
                                won_duplicate = won_item_id in unlocked_gadgets
                                won_compensation = GADGET_TYPES[won_item_id]["unlock_cost"] // 2 if won_duplicate else 0
                                if not won_duplicate: unlocked_gadgets.append(won_item_id)

                elif STATE == "MENU_BACKPACK":
                    if back_to_menu_rect_bp.collidepoint(mx, my):
                        save_all()
                        STATE = "MENU"

                    if tab_bp_towers_rect.collidepoint(mx, my):
                        menu_backpack_tab = "TOWERS"
                    elif tab_bp_gadgets_rect.collidepoint(mx, my):
                        menu_backpack_tab = "GADGETS"

                    if menu_backpack_tab == "TOWERS":
                        for slot in item_slots:
                            act_rect = pygame.Rect(slot["rect"].x + 10, slot["rect"].bottom - 25,
                                                   slot["rect"].width - 20, 20)
                            if act_rect.collidepoint(mx, my):
                                t_type = slot["type"]
                                if t_type not in unlocked_towers:
                                    if diamonds >= TOWER_TYPES[t_type]["unlock_cost"]:
                                        diamonds -= TOWER_TYPES[t_type]["unlock_cost"]
                                        unlocked_towers.append(t_type)
                                        save_all()
                                else:
                                    if t_type in equipped_towers:
                                        if len(equipped_towers) > 1:
                                            equipped_towers.remove(t_type)
                                            save_all()
                                    else:
                                        equipped_towers.append(t_type)
                                        save_all()
                    elif menu_backpack_tab == "GADGETS":
                        for slot in gadget_slots:
                            rect = slot["rect"]
                            act_rect = pygame.Rect(rect.x + 8, rect.bottom - 26, rect.width - 16, 20)
                            if act_rect.collidepoint(mx, my):
                                g_type = slot["type"]
                                if g_type in unlocked_gadgets:
                                    if g_type in equipped_gadgets:
                                        equipped_gadgets.remove(g_type)
                                    else:
                                        equipped_gadgets.append(g_type)
                                    save_all()

                elif STATE == "BOX_ANIMATION":
                    if anim_ticks > 150 and claim_btn_rect.collidepoint(mx, my):
                        if won_duplicate: diamonds += won_compensation
                        save_all()
                        STATE = "MENU_SHOP"

                elif STATE == "IN_GAME_BACKPACK":
                    if back_to_game_rect.collidepoint(mx, my): STATE = "GAME"
                    for i, t_type in enumerate(equipped_towers):
                        rect = pygame.Rect(30 + (i % 5) * 148, 110 + (i // 5) * 145, 140, 135)
                        act_rect = pygame.Rect(rect.x + 10, rect.bottom - 25, rect.width - 20, 20)
                        if act_rect.collidepoint(mx, my) or rect.collidepoint(mx, my):
                            selected_tower = t_type
                            STATE = "GAME"

                elif STATE == "GAME_OVER":
                    if game_over_menu_rect.collidepoint(mx, my):
                        save_all()
                        STATE = "MENU"

        # --- Drawing States ---
        if STATE == "MENU":
            screen.fill((25, 25, 35))
            screen.blit(font_title.render("TOWER DEFENSE", True, YELLOW), (WIDTH // 2 - 200, 60))
            draw_diamond(screen, WIDTH // 2 - 35, 133, 20, 24)
            screen.blit(font_small.render(f": {diamonds}", True, WHITE), (WIDTH // 2 - 15, 120))

            draw_interactive_button(screen, play_btn_rect, "START GAME", font_small, BTN_COLOR, BTN_HOVER,
                                    play_btn_rect.collidepoint(mx, my))
            draw_interactive_button(screen, menu_shop_btn_rect, "SHOP & BOXES", font_small, SHOP_COLOR, SHOP_HOVER,
                                    menu_shop_btn_rect.collidepoint(mx, my))
            draw_interactive_button(screen, menu_backpack_btn_rect, "BACKPACK", font_small, PURPLE, (170, 130, 240),
                                    menu_backpack_btn_rect.collidepoint(mx, my))
            draw_interactive_button(screen, exit_btn_rect, "EXIT", font_small, EXIT_COLOR, EXIT_HOVER,
                                    exit_btn_rect.collidepoint(mx, my))

        elif STATE == "GAME":
            draw_map(screen)
            draw_interactive_button(screen, game_to_menu_rect, "MENU", font_mini, EXIT_COLOR, EXIT_HOVER,
                                    game_to_menu_rect.collidepoint(mx, my))

            map_title = font_small.render(f"MAP: {CURRENT_MAP['name']}", True, WHITE)
            screen.blit(map_title, (WIDTH // 2 - map_title.get_width() // 2, 20))

            # Range highlight when building
            if my < HEIGHT - PANEL_HEIGHT and not selected_placed_tower:
                grid_x, grid_y = (mx // TILE_SIZE) * TILE_SIZE + 20, (my // TILE_SIZE) * TILE_SIZE + 20
                if (grid_x, grid_y) in occupied_cells or is_on_path(grid_x, grid_y) or is_on_decoration(grid_x, grid_y):
                    pygame.draw.circle(screen, (255, 0, 0, 100), (grid_x, grid_y), 20)
                else:
                    rng = TOWER_TYPES[selected_tower]["range"]
                    surface_alpha = pygame.Surface((rng * 2, rng * 2), pygame.SRCALPHA)
                    pygame.draw.circle(surface_alpha, (255, 255, 255, 60), (rng, rng), rng)
                    screen.blit(surface_alpha, (grid_x - rng, grid_y - rng))

            # Wave logic
            if wave_active:
                if enemies_spawned < (5 + wave * 3):
                    spawn_timer += 1
                    if spawn_timer >= max(10, 50 - wave * 2):
                        enemies.append(Enemy(wave))
                        enemies_spawned += 1
                        spawn_timer = 0
                elif not enemies:
                    wave_active = False
                    wave += 1
                    enemies_spawned = 0
                    reward_money = 100 + (wave * 10)
                    money += reward_money
                    diamonds += 20 + wave
                    # Show bonus on screen
                    FLOATING_TEXTS.append(
                        FloatingText(WIDTH // 2, HEIGHT // 2, f"Wave cleared! +${reward_money}", YELLOW))
                    save_all()

            # Update entities
            for e in enemies[:]:
                e.update()
                e.draw(screen)
                if e.target_waypoint >= len(CURRENT_MAP["path"]):
                    enemies.remove(e)
                    lives -= 1
                    if lives <= 0: STATE = "GAME_OVER"
                elif e.health <= 0:
                    enemies.remove(e)
                    money += e.reward
                    diamonds += 2
                    FLOATING_TEXTS.append(FloatingText(e.x, e.y, f"+${e.reward}", YELLOW))
                    for _ in range(5): PARTICLES.append(Particle(e.x, e.y, e.color))

            for t in towers:
                t.attack(enemies, screen)
                t.draw(screen)

            for p in PARTICLES[:]:
                p.update()
                p.draw(screen)
                if p.timer <= 0: PARTICLES.remove(p)

            for ft in FLOATING_TEXTS[:]:
                ft.update()
                ft.draw(screen)
                if ft.timer <= 0: FLOATING_TEXTS.remove(ft)

            # Tower upgrade menu
            if selected_placed_tower:
                t = selected_placed_tower
                surface_alpha = pygame.Surface((t.range * 2, t.range * 2), pygame.SRCALPHA)
                pygame.draw.circle(surface_alpha, (255, 255, 255, 60), (int(t.range), int(t.range)), int(t.range))
                screen.blit(surface_alpha, (t.x - t.range, t.y - t.range))

                px, py = upgrade_btn_rect.x - 10, upgrade_btn_rect.y - 25
                pygame.draw.rect(screen, (40, 40, 50), (px, py, 140, 90), border_radius=10)
                pygame.draw.rect(screen, WHITE, (px, py, 140, 90), 2, border_radius=10)
                screen.blit(font_mini.render(f"Level: {t.level}", True, WHITE), (px + 10, py + 5))

                upg_color = BTN_COLOR if money >= t.upgrade_cost else BTN_DISABLED
                draw_interactive_button(screen, upgrade_btn_rect, f"Upgrade: ${t.upgrade_cost}", font_mini, upg_color,
                                        BTN_HOVER if money >= t.upgrade_cost else BTN_DISABLED,
                                        upgrade_btn_rect.collidepoint(mx, my))
                draw_interactive_button(screen, sell_btn_rect, "Sell", font_mini, EXIT_COLOR, EXIT_HOVER,
                                        sell_btn_rect.collidepoint(mx, my))

            # Bottom panel
            pygame.draw.rect(screen, PANEL_BG, (0, HEIGHT - PANEL_HEIGHT, WIDTH, PANEL_HEIGHT))
            pygame.draw.line(screen, (80, 80, 90), (0, HEIGHT - PANEL_HEIGHT), (WIDTH, HEIGHT - PANEL_HEIGHT), 4)

            screen.blit(font_large.render(f"${money}", True, YELLOW), (20, HEIGHT - 80))
            screen.blit(font_small.render(f"Wave: {wave}", True, WHITE), (20, HEIGHT - 35))
            screen.blit(font_large.render(f"♥ {lives}", True, RED), (150, HEIGHT - 80))
            screen.blit(font_small.render(f"Tower: {TOWER_TYPES[selected_tower]['name']}", True, WHITE),
                        (150, HEIGHT - 35))

            draw_interactive_button(screen, in_game_backpack_btn_rect, "BASE", font_small, PURPLE, (170, 130, 240),
                                    in_game_backpack_btn_rect.collidepoint(mx, my))
            draw_interactive_button(screen, game_btn_rect, "ATTACK!" if wave_active else "NEXT WAVE", font_small,
                                    BTN_COLOR if not wave_active else BTN_DISABLED, BTN_HOVER,
                                    game_btn_rect.collidepoint(mx, my))

        elif STATE == "MENU_SHOP":
            screen.fill((25, 25, 35))
            screen.blit(font_title.render("SHOP", True, YELLOW), (WIDTH // 2 - 80, 10))
            draw_diamond(screen, 30, 30, 20, 24)
            screen.blit(font_small.render(f" : {diamonds}", True, WHITE), (45, 17))

            draw_interactive_button(screen, tab_gadgets_rect, "GADGETS / UPGRADES", font_tiny,
                                    SHOP_COLOR if shop_tab == "GADGETS" else (60, 60, 75),
                                    SHOP_HOVER if shop_tab == "GADGETS" else (100, 100, 120),
                                    tab_gadgets_rect.collidepoint(mx, my))
            draw_interactive_button(screen, tab_boxes_rect, "BOXES (GACHA)", font_mini,
                                    PURPLE if shop_tab == "BOXES" else (60, 60, 75),
                                    (170, 130, 240) if shop_tab == "BOXES" else (100, 100, 120),
                                    tab_boxes_rect.collidepoint(mx, my))

            if shop_tab == "GADGETS":
                for slot in gadget_slots:
                    rect, g_type = slot["rect"], slot["type"]
                    stats = GADGET_TYPES[g_type]
                    pygame.draw.rect(screen, (45, 45, 55), rect, border_radius=10)
                    pygame.draw.rect(screen, stats["color"], rect, 2, border_radius=10)
                    screen.blit(font_mini.render(stats["name"], True, WHITE), (rect.x + 8, rect.y + 6))
                    screen.blit(font_tiny.render(stats["desc"], True, (200, 200, 200)), (rect.x + 8, rect.y + 26))

                    act_rect = pygame.Rect(rect.x + 8, rect.bottom - 26, rect.width - 16, 20)
                    act_hover = act_rect.collidepoint(mx, my)

                    if g_type not in unlocked_gadgets:
                        can_buy = diamonds >= stats["unlock_cost"]
                        draw_interactive_button(screen, act_rect, f"BUY ♦ {stats['unlock_cost']}", font_tiny,
                                                BTN_COLOR if can_buy else RED, BTN_HOVER if can_buy else RED, act_hover)
                    else:
                        draw_interactive_button(screen, act_rect, "BOUGHT", font_tiny, (100, 100, 100),
                                                (100, 100, 100), False)

            elif shop_tab == "BOXES":
                pygame.draw.rect(screen, (100, 70, 40), box_normal_rect, border_radius=20)
                pygame.draw.rect(screen, WHITE, box_normal_rect, 4, border_radius=20)
                n_title = font_small.render("NORMAL", True, WHITE)
                screen.blit(n_title, (box_normal_rect.centerx - n_title.get_width() // 2, box_normal_rect.y + 20))
                screen.blit(font_tiny.render("Epic Chance: 2%", True, (200, 200, 200)),
                            (box_normal_rect.x + 20, box_normal_rect.y + 70))
                btn_n = pygame.Rect(box_normal_rect.x + 20, box_normal_rect.bottom - 60, 160, 40)
                n_color = BTN_COLOR if diamonds >= 500 else BTN_DISABLED
                draw_interactive_button(screen, btn_n, "OPEN (500♦)", font_mini, n_color,
                                        BTN_HOVER if diamonds >= 500 else BTN_DISABLED, btn_n.collidepoint(mx, my))

                pygame.draw.rect(screen, (80, 20, 120), box_premium_rect, border_radius=20)
                pygame.draw.rect(screen, GOLD, box_premium_rect, 3, border_radius=20)
                p_title = font_small.render("PREMIUM", True, GOLD)
                screen.blit(p_title, (box_premium_rect.centerx - p_title.get_width() // 2, box_premium_rect.y + 20))
                screen.blit(font_tiny.render("Legendary Chance: 25%", True, GOLD),
                            (box_premium_rect.x + 20, box_premium_rect.y + 70))
                btn_p = pygame.Rect(box_premium_rect.x + 20, box_premium_rect.bottom - 60, 160, 40)
                p_color = PURPLE if diamonds >= 2000 else BTN_DISABLED
                draw_interactive_button(screen, btn_p, "OPEN (2000♦)", font_mini, p_color,
                                        (170, 130, 240) if diamonds >= 2000 else BTN_DISABLED,
                                        btn_p.collidepoint(mx, my))

            promo_bg = (80, 80, 80) if active_input else (50, 50, 60)
            pygame.draw.rect(screen, promo_bg, promo_rect, border_radius=10)
            pygame.draw.rect(screen, YELLOW if active_input else WHITE, promo_rect, 3, border_radius=10)
            p_text = input_text if input_text else ("ENTER..." if active_input else "PROMO CODE")
            p_surf = font_small.render(p_text, True, WHITE)
            screen.blit(p_surf, p_surf.get_rect(center=promo_rect.center))

            draw_interactive_button(screen, back_to_menu_rect_shop, "BACK", font_small, (100, 100, 100),
                                    (130, 130, 130), back_to_menu_rect_shop.collidepoint(mx, my))

        elif STATE == "MENU_BACKPACK":
            screen.fill((25, 25, 35))
            screen.blit(font_title.render("INVENTORY BACKPACK", True, PURPLE), (WIDTH // 2 - 270, 10))
            draw_diamond(screen, 30, 30, 20, 24)
            screen.blit(font_small.render(f" : {diamonds}", True, WHITE), (45, 17))

            draw_interactive_button(screen, tab_bp_towers_rect, "TOWERS", font_mini,
                                    PURPLE if menu_backpack_tab == "TOWERS" else (60, 60, 75),
                                    (170, 130, 240) if menu_backpack_tab == "TOWERS" else (100, 100, 120),
                                    tab_bp_towers_rect.collidepoint(mx, my))
            draw_interactive_button(screen, tab_bp_gadgets_rect, "ACTIVE GADGETS", font_mini,
                                    SHOP_COLOR if menu_backpack_tab == "GADGETS" else (60, 60, 75),
                                    SHOP_HOVER if menu_backpack_tab == "GADGETS" else (100, 100, 120),
                                    tab_bp_gadgets_rect.collidepoint(mx, my))

            if menu_backpack_tab == "TOWERS":
                for slot in item_slots:
                    rect, t_type = slot["rect"], slot["type"]
                    stats = TOWER_TYPES[t_type]
                    is_hover = rect.collidepoint(mx, my)

                    bg_color = (60, 60, 75) if is_hover else (45, 45, 55)
                    rarity_color = RARITY_COLORS[stats["rarity"]]
                    border_color = BTN_COLOR if t_type in equipped_towers else (
                        rarity_color if t_type in unlocked_towers else RED)

                    pygame.draw.rect(screen, bg_color, rect, border_radius=15)
                    pygame.draw.rect(screen, border_color, rect, 3, border_radius=15)

                    name_s = font_mini.render(stats["name"], True, WHITE)
                    screen.blit(name_s, (rect.centerx - name_s.get_width() // 2, rect.y + 5))

                    if t_type in unlocked_towers:
                        Tower(rect.centerx, rect.y + 45, t_type).draw(screen)
                        screen.blit(font_tiny.render(f"Damage: {stats['damage']}", True, (200, 200, 200)),
                                    (rect.x + 10, rect.y + 75))
                        screen.blit(font_tiny.render(f"Range: {stats['range']}", True, (200, 200, 200)),
                                    (rect.x + 10, rect.y + 90))
                    else:
                        screen.blit(font_large.render("?", True, RED), (rect.centerx - 10, rect.y + 30))

                    act_rect = pygame.Rect(rect.x + 10, rect.bottom - 25, rect.width - 20, 20)
                    act_hover = act_rect.collidepoint(mx, my)

                    if t_type not in unlocked_towers:
                        act_text, act_col, act_hov = f"BUY ♦ {stats['unlock_cost']}", EXIT_COLOR, EXIT_HOVER
                    elif t_type in equipped_towers:
                        act_text, act_col, act_hov = "UNEQUIP", BTN_COLOR, BTN_HOVER
                    else:
                        act_text, act_col, act_hov = "EQUIP", SHOP_COLOR, SHOP_HOVER

                    draw_interactive_button(screen, act_rect, act_text, font_tiny, act_col, act_hov, act_hover)

            elif menu_backpack_tab == "GADGETS":
                for slot in gadget_slots:
                    rect, g_type = slot["rect"], slot["type"]
                    stats = GADGET_TYPES[g_type]

                    if g_type in unlocked_gadgets:
                        pygame.draw.rect(screen, (45, 45, 55), rect, border_radius=10)
                        border_col = BTN_COLOR if g_type in equipped_gadgets else stats["color"]
                        pygame.draw.rect(screen, border_col, rect, 4 if g_type in equipped_gadgets else 2,
                                         border_radius=10)
                        screen.blit(font_mini.render(stats["name"], True, WHITE), (rect.x + 8, rect.y + 6))
                        screen.blit(font_tiny.render(stats["desc"], True, (200, 200, 200)), (rect.x + 8, rect.y + 26))

                        act_rect = pygame.Rect(rect.x + 8, rect.bottom - 26, rect.width - 16, 20)
                        act_hover = act_rect.collidepoint(mx, my)

                        if g_type in equipped_gadgets:
                            draw_interactive_button(screen, act_rect, "DISABLE", font_tiny, EXIT_COLOR, EXIT_HOVER,
                                                    act_hover)
                        else:
                            draw_interactive_button(screen, act_rect, "ENABLE", font_tiny, BTN_COLOR, BTN_HOVER,
                                                    act_hover)
                    else:
                        pygame.draw.rect(screen, (30, 30, 40), rect, border_radius=10)
                        screen.blit(font_mini.render("???", True, (100, 100, 100)),
                                    (rect.centerx - 15, rect.centery - 10))

            draw_interactive_button(screen, back_to_menu_rect_bp, "MAIN MENU", font_small, (100, 100, 100),
                                    (130, 130, 130), back_to_menu_rect_bp.collidepoint(mx, my))

        elif STATE == "BOX_ANIMATION":
            anim_ticks += 1
            screen.fill((20, 20, 30))
            cx, cy = WIDTH // 2, HEIGHT // 2 - 50

            if anim_ticks < 100:
                shake_x = math.sin(anim_ticks) * 8 * (anim_ticks / 100)
                box_color = (100, 70, 40) if current_box_type == "NORMAL" else (80, 20, 120)
                b_rect = pygame.Rect(cx - 75 + shake_x, cy - 75, 150, 150)
                pygame.draw.rect(screen, box_color, b_rect, border_radius=15)
                pygame.draw.rect(screen, WHITE if current_box_type == "NORMAL" else GOLD, b_rect, 5, border_radius=15)
                screen.blit(font_large.render("?", True, WHITE), (cx - 10 + shake_x, cy - 20))

            elif anim_ticks < 150:
                radius = (anim_ticks - 100) * 15
                pygame.draw.circle(screen, WHITE, (cx, cy), int(radius))

            else:
                stats = TOWER_TYPES[won_item_id] if won_item_type == "TOWER" else GADGET_TYPES[won_item_id]
                rarity_col = RARITY_COLORS[stats["rarity"]]
                pygame.draw.circle(screen, rarity_col, (cx, cy), 120, 20)

                card_rect = pygame.Rect(cx - 100, cy - 120, 200, 240)
                pygame.draw.rect(screen, (40, 40, 50), card_rect, border_radius=20)
                pygame.draw.rect(screen, rarity_col, card_rect, 5, border_radius=20)

                t_title = font_large.render(stats["name"], True, WHITE)
                screen.blit(t_title, (cx - t_title.get_width() // 2, card_rect.y + 20))
                t_rarity = font_small.render(stats["rarity"], True, rarity_col)
                screen.blit(t_rarity, (cx - t_rarity.get_width() // 2, card_rect.y + 60))

                if won_item_type == "TOWER":
                    Tower(cx, cy + 30, won_item_id).draw(screen)
                else:
                    pygame.draw.rect(screen, stats["color"], (cx - 40, cy, 80, 50), border_radius=10)
                    pygame.draw.rect(screen, WHITE, (cx - 40, cy, 80, 50), 3, border_radius=10)
                    g_icon_text = font_mini.render("GADGET", True, WHITE)
                    screen.blit(g_icon_text, (cx - g_icon_text.get_width() // 2, cy + 15))

                if won_duplicate:
                    dup_text = font_small.render("DUPLICATE!", True, RED)
                    comp_text = font_mini.render(f"Compensation: +{won_compensation} ♦", True, YELLOW)
                    screen.blit(dup_text, (cx - dup_text.get_width() // 2, card_rect.bottom + 20))
                    screen.blit(comp_text, (cx - comp_text.get_width() // 2, card_rect.bottom + 50))
                else:
                    msg = "NEW TOWER!" if won_item_type == "TOWER" else "NEW GADGET!"
                    new_text = font_small.render(msg, True, (50, 255, 50))
                    screen.blit(new_text, (cx - new_text.get_width() // 2, card_rect.bottom + 20))

                draw_interactive_button(screen, claim_btn_rect, "CLAIM", font_small, BTN_COLOR, BTN_HOVER,
                                        claim_btn_rect.collidepoint(mx, my))

        elif STATE == "IN_GAME_BACKPACK":
            screen.fill((25, 25, 35))
            screen.blit(font_title.render("CHOOSE TOWER TO BUILD", True, PURPLE), (WIDTH // 2 - 320, 20))
            for i, t_type in enumerate(equipped_towers):
                rect = pygame.Rect(30 + (i % 5) * 148, 110 + (i // 5) * 145, 140, 135)
                rarity_color = RARITY_COLORS[TOWER_TYPES[t_type]["rarity"]]
                pygame.draw.rect(screen, (60, 60, 75) if rect.collidepoint(mx, my) else (45, 45, 55), rect,
                                 border_radius=15)
                pygame.draw.rect(screen, YELLOW if selected_tower == t_type else rarity_color, rect,
                                 4 if selected_tower == t_type else 2, border_radius=15)

                Tower(rect.centerx, rect.y + 45, t_type).draw(screen)
                name_s = font_mini.render(TOWER_TYPES[t_type]["name"], True, WHITE)
                screen.blit(name_s, (rect.centerx - name_s.get_width() // 2, rect.y + 70))

                act_rect = pygame.Rect(rect.x + 10, rect.bottom - 25, rect.width - 20, 20)
                act_hover = act_rect.collidepoint(mx, my)

                if selected_tower == t_type:
                    draw_interactive_button(screen, act_rect, "SELECTED", font_tiny, BTN_COLOR, BTN_HOVER, act_hover)
                else:
                    draw_interactive_button(screen, act_rect, f"SELECT: ${TOWER_TYPES[t_type]['cost']}", font_tiny,
                                            SHOP_COLOR, SHOP_HOVER, act_hover)

            draw_interactive_button(screen, back_to_game_rect, "RETURN TO BATTLE", font_small, EXIT_COLOR, EXIT_HOVER,
                                    back_to_game_rect.collidepoint(mx, my))

        elif STATE == "GAME_OVER":
            screen.fill((30, 0, 0))
            game_over_text = font_title.render("YOU LOST!", True, RED)
            wave_text = font_large.render(f"You reached wave: {wave}", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3 - 50))
            screen.blit(wave_text, (WIDTH // 2 - wave_text.get_width() // 2, HEIGHT // 2 - 20))
            draw_interactive_button(screen, game_over_menu_rect, "MAIN MENU", font_small, EXIT_COLOR, EXIT_HOVER,
                                    game_over_menu_rect.collidepoint(mx, my))

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()