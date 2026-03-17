import math
import random

import pygame

# --- Window ---
WIDTH, HEIGHT = 1920, 1080
FPS = 60

# --- Player ---
PLAYER_RADIUS = 15
PLAYER_MAX_HP = 100
PLAYER_SPEED = 250.0  # px/s

# --- Enemy Spawn & Difficulty ---
BASE_SPAWN_MS = 560
MIN_SPAWN_MS = 64
GRID_SIZE = 72

# --- Grunt Enemy ---
GRUNT_RADIUS = 12
GRUNT_HP = 2
GRUNT_MIN_SPEED = 70.0
GRUNT_MAX_SPEED = 140.0
GRUNT_DAMAGE = 8
GRUNT_XP = 1

# --- Tank Enemy ---
TANK_RADIUS = 18
TANK_HP = 10
TANK_MIN_SPEED = 48.0
TANK_MAX_SPEED = 76.0
TANK_DAMAGE = 14
TANK_XP = 3

# --- Dash Enemy ---
DASH_RADIUS = 10
DASH_HP = 1
DASH_MIN_SPEED = 180.0
DASH_MAX_SPEED = 240.0
DASH_DAMAGE = 6
DASH_XP = 1

# --- Elite Enemy ---
ELITE_RADIUS = 22
ELITE_HP = 24
ELITE_MIN_SPEED = 72.0
ELITE_MAX_SPEED = 112.0
ELITE_DAMAGE = 18
ELITE_XP = 9

# --- Bullet ---
BULLET_SPEED = 420.0
BULLET_RADIUS = 4
BULLET_COOLDOWN_MS = 220
BULLET_RANGE = 520.0
BULLET_DAMAGE = 1

# --- XP ---
XP_ORB_RADIUS = 5
XP_PER_ORB = 1
LEVEL_UP_XP = 10

# --- Progression & Score ---
COMBO_WINDOW_MS = 2600
PASSIVE_SCORE_MS = 1000

# --- Colors ---
TEXT_COLOR = (220, 230, 240)
PLAYER_FLASH = (255, 150, 130)
NOVA_EFFECT_COLOR = (220, 180, 255)

GRUNT_COLOR = (220, 88, 76)
TANK_COLOR = (186, 70, 64)
DASH_COLOR = (238, 128, 78)
ELITE_COLOR = (186, 108, 238)
BULLET_COLOR = (130, 195, 255)
XP_COLOR = (235, 220, 110)


def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v


def abs_angle_delta(a, b):
    d = (a - b + math.pi) % (2.0 * math.pi) - math.pi
    return abs(d)


class Player:
    __slots__ = (
        "x",
        "y",
        "hp",
        "max_hp",
        "level",
        "xp",
        "xp_next",
        "hit_timer",
        "speed",
        "bullet_cooldown",
        "bullet_speed",
        "bullet_range",
        "bullet_damage",
        "pierce",
        "shot_count",
        "pickup_radius",
        "orb_pull_strength",
        "damage_reduction",
        "regen",
        "skills",
        "damage_multiplier",
        "score_multiplier",
        "xp_multiplier",
        "melee_level",
        "melee_cooldown",
        "melee_damage",
        "melee_range",
        "melee_arc",
        "melee_hit_limit",
        "nova_cooldown",
        "nova_damage",
        "nova_radius",
        "nova_level",
        "crit_chance",
        "crit_multiplier",
        "kill_heal",
        "hit_cooldown_ms",
        "aim_angle",
        "frenzy_timer",
        "frenzy_stacks",
    )

    def __init__(self):
        self.x = WIDTH * 0.5
        self.y = HEIGHT * 0.5

        self.hp = float(PLAYER_MAX_HP)
        self.max_hp = float(PLAYER_MAX_HP)
        self.level = 1
        self.xp = 0
        self.xp_next = LEVEL_UP_XP

        self.hit_timer = 0
        self.hit_cooldown_ms = 350

        self.speed = PLAYER_SPEED
        self.bullet_cooldown = BULLET_COOLDOWN_MS
        self.bullet_speed = BULLET_SPEED
        self.bullet_range = BULLET_RANGE
        self.bullet_damage = float(BULLET_DAMAGE)
        self.pierce = 0
        self.shot_count = 1

        self.pickup_radius = PLAYER_RADIUS + 32
        self.orb_pull_strength = 300.0

        self.damage_reduction = 0.0
        self.regen = 0.0

        self.crit_chance = 0.05
        self.crit_multiplier = 1.6
        self.kill_heal = 0.0

        self.skills = {}
        self.damage_multiplier = 1.0
        self.score_multiplier = 1.0
        self.xp_multiplier = 1.0
        self.melee_level = 0
        self.melee_cooldown = 0
        self.melee_damage = 0.0
        self.melee_range = 0.0
        self.melee_arc = 0.0
        self.melee_hit_limit = 0

        self.nova_level = 0
        self.nova_cooldown = 0
        self.nova_damage = 0.0
        self.nova_radius = 0

        self.aim_angle = -math.pi / 2
        self.frenzy_timer = 0
        self.frenzy_stacks = 0

    def move(self, dx, dy):
        self.x = clamp(self.x + dx, PLAYER_RADIUS, WIDTH - PLAYER_RADIUS)
        self.y = clamp(self.y + dy, PLAYER_RADIUS, HEIGHT - PLAYER_RADIUS)

    def gain_xp(self, amount):
        self.xp += amount
        gained_levels = []
        while self.xp >= self.xp_next:
            self.xp -= self.xp_next
            self.level += 1
            self.xp_next = int(self.xp_next * 1.19) + 3
            self.max_hp += 6
            self.hp = min(self.max_hp, self.hp + 8)
            # Keep late-game growth feeling strong.
            self.damage_multiplier *= 1.012
            self.xp_multiplier *= 1.004
            if self.level % 4 == 0:
                self.bullet_damage += 0.2
            gained_levels.append(self.level)
        return gained_levels


class Enemy:
    __slots__ = (
        "x",
        "y",
        "speed",
        "hp",
        "radius",
        "color",
        "damage",
        "max_hp",
        "kind",
        "xp_reward",
    )

    def __init__(self, x, y, speed, hp, radius, color, damage, kind, xp_reward):
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = float(hp)
        self.max_hp = float(hp)
        self.radius = radius
        self.color = color
        self.damage = damage
        self.kind = kind
        self.xp_reward = xp_reward

    def update(self, player, dt_s):
        dx = player.x - self.x
        dy = player.y - self.y
        d_sq = dx * dx + dy * dy
        if d_sq > 1e-6:
            inv_d = 1.0 / math.sqrt(d_sq)
            self.x += dx * inv_d * self.speed * dt_s
            self.y += dy * inv_d * self.speed * dt_s

    def draw_hp_bar(self, surface):
        if self.hp < self.max_hp:
            ratio = self.hp / self.max_hp
            bar_w = self.radius * 2
            bar_h = 5
            bar_x = self.x - self.radius
            bar_y = self.y - self.radius - bar_h - 3
            pygame.draw.rect(surface, (38, 38, 42), (bar_x, bar_y, bar_w, bar_h), border_radius=2)
            pygame.draw.rect(
                surface,
                (255, 74, 70),
                (bar_x, bar_y, int(bar_w * ratio), bar_h),
                border_radius=2,
            )


class Bullet:
    __slots__ = ("x", "y", "vx", "vy", "life", "damage", "pierce")

    def __init__(self, x, y, vx, vy, damage, pierce, life):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.damage = damage
        self.pierce = pierce

    def update(self, dt_s):
        self.x += self.vx * dt_s
        self.y += self.vy * dt_s
        self.life -= math.hypot(self.vx, self.vy) * dt_s
        return self.life > 0 and -20 <= self.x <= WIDTH + 20 and -20 <= self.y <= HEIGHT + 20


class XpOrb:
    __slots__ = ("x", "y", "value", "vx", "vy")

    def __init__(self, x, y, value=XP_PER_ORB):
        self.x = x
        self.y = y
        self.value = value
        self.vx = random.uniform(-70.0, 70.0)
        self.vy = random.uniform(-70.0, 70.0)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Vampire Survivors - Expanded")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.font = self.load_font(18)
        self.big_font = self.load_font(34)

        self.background = self.make_background_surface()
        self.sprites = self.make_sprite_cache()

        self.player = Player()
        self.enemies = []
        self.bullets = []
        self.orbs = []
        self.effects = []

        self.spawn_timer = 0
        self.shoot_timer = 0
        self.melee_timer = 0
        self.nova_timer = 0
        self.horde_timer = 0
        self.horde_active_ms = 0
        self.horde_count = 0
        self.elapsed_ms = 0

        self.running = True
        self.game_over = False
        self.leveling = False
        self.pending_levels = 0
        self.level_up_options = []
        self.last_level_options = []

        self.kill_count = 0
        self.score = 0
        self.best_score = 0
        self.combo_kills = 0
        self.longest_combo = 0
        self.combo_timer_ms = 0
        self.passive_score_timer = 0
        self.reroll_charges = 1

        self.skill_defs = self.make_skill_defs()

    def load_font(self, size):
        # Prefer CJK-capable fonts so Chinese text renders correctly on macOS/Windows/Linux.
        preferred_fonts = (
            "pingfangsc",
            "hiraginosansgb",
            "heiti sc",
            "stheiti",
            "songti sc",
            "arial unicode ms",
            "microsoft yahei ui",
            "microsoft yahei",
            "simhei",
            "simsun",
            "notosanscjk",
            "wenquanyizenhei",
            "arial",
        )

        available = set(pygame.font.get_fonts())

        def normalize(name):
            return "".join(ch for ch in name.lower() if ch.isalnum())

        for name in preferred_fonts:
            if normalize(name) in available:
                path = pygame.font.match_font(name)
                if path:
                    return pygame.font.Font(path, size)

        for name in preferred_fonts:
            path = pygame.font.match_font(name)
            if path:
                return pygame.font.Font(path, size)

        return pygame.font.SysFont("sans", size)

    def format_number(self, value):
        value = float(value)
        abs_v = abs(value)
        if abs_v >= 1_000_000_000:
            return f"{value / 1_000_000_000:.2f}B"
        if abs_v >= 1_000_000:
            return f"{value / 1_000_000:.2f}M"
        if abs_v >= 1_000:
            return f"{value / 1_000:.1f}K"
        return str(int(value))

    def make_background_surface(self):
        surf = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            t = y / max(1, HEIGHT - 1)
            r = int(14 + 18 * t)
            g = int(20 + 16 * t)
            b = int(30 + 20 * t)
            pygame.draw.line(surf, (r, g, b), (0, y), (WIDTH, y))

        grid = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for x in range(0, WIDTH, 40):
            alpha = 28 if x % 120 == 0 else 12
            pygame.draw.line(grid, (82, 104, 128, alpha), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 40):
            alpha = 28 if y % 120 == 0 else 12
            pygame.draw.line(grid, (82, 104, 128, alpha), (0, y), (WIDTH, y))

        vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(vignette, (0, 0, 0, 85), (0, 0, WIDTH, HEIGHT), width=56)

        surf.blit(grid, (0, 0))
        surf.blit(vignette, (0, 0))
        return surf

    def make_sprite_cache(self):
        return {
            "player": self.make_player_sprite(),
            "grunt": self.make_grunt_sprite(),
            "tank": self.make_tank_sprite(),
            "dash": self.make_dash_sprite(),
            "elite": self.make_elite_sprite(),
        }

    def make_player_sprite(self):
        size = 46
        c = size // 2
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        pygame.draw.circle(surf, (66, 220, 172, 52), (c, c), 21)
        body = [(c, 5), (size - 5, c), (c, size - 5), (5, c)]
        pygame.draw.polygon(surf, (74, 214, 170), body)
        pygame.draw.polygon(surf, (26, 78, 80), body, 2)

        pygame.draw.circle(surf, (230, 250, 240), (c, c), 7)
        pygame.draw.circle(surf, (72, 140, 126), (c, c), 3)
        pygame.draw.polygon(surf, (250, 236, 140), [(c, 9), (c - 5, 17), (c + 5, 17)])

        return surf

    def make_grunt_sprite(self):
        size = 34
        c = size // 2
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        body = [(c, 4), (size - 4, c), (c, size - 4), (4, c)]
        pygame.draw.polygon(surf, GRUNT_COLOR, body)
        pygame.draw.polygon(surf, (100, 40, 36), body, 2)

        pygame.draw.circle(surf, (245, 235, 235), (c - 5, c - 2), 3)
        pygame.draw.circle(surf, (245, 235, 235), (c + 5, c - 2), 3)
        pygame.draw.circle(surf, (65, 35, 35), (c - 5, c - 2), 1)
        pygame.draw.circle(surf, (65, 35, 35), (c + 5, c - 2), 1)

        return surf

    def make_tank_sprite(self):
        size = 46
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        hull = pygame.Rect(7, 10, 32, 26)
        core = pygame.Rect(12, 14, 22, 18)
        pygame.draw.rect(surf, TANK_COLOR, hull, border_radius=7)
        pygame.draw.rect(surf, (96, 38, 34), hull, 2, border_radius=7)
        pygame.draw.rect(surf, (120, 46, 42), core, border_radius=4)
        pygame.draw.line(surf, (238, 180, 160), (12, 23), (34, 23), 3)
        pygame.draw.circle(surf, (245, 220, 200), (16, 20), 2)
        pygame.draw.circle(surf, (245, 220, 200), (30, 20), 2)

        return surf

    def make_dash_sprite(self):
        size = 30
        c = size // 2
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        body = [(c, 3), (size - 3, size - 7), (c, size - 12), (3, size - 7)]
        pygame.draw.polygon(surf, DASH_COLOR, body)
        pygame.draw.polygon(surf, (124, 62, 34), body, 2)
        pygame.draw.circle(surf, (255, 230, 180), (c, c - 1), 2)

        return surf

    def make_elite_sprite(self):
        size = 52
        c = size // 2
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        pygame.draw.circle(surf, (220, 160, 255, 56), (c, c), 23)
        body = [(c, 4), (size - 7, c), (c, size - 4), (7, c)]
        pygame.draw.polygon(surf, ELITE_COLOR, body)
        pygame.draw.polygon(surf, (92, 54, 132), body, 3)

        pygame.draw.circle(surf, (255, 238, 182), (c, c), 7)
        pygame.draw.circle(surf, (118, 78, 160), (c, c), 3)
        pygame.draw.line(surf, (255, 238, 182), (c - 12, c + 12), (c + 12, c + 12), 2)
        pygame.draw.circle(surf, (255, 196, 128), (c - 9, c - 6), 2)
        pygame.draw.circle(surf, (255, 196, 128), (c + 9, c - 6), 2)

        return surf
    def make_skill_defs(self):
        return {
            "rapid": {
                "name": "速射",
                "soft_cap": 6,
                "base_desc": "攻击间隔缩短",
                "mastery_desc": "精通：进一步提速并强化全局伤害",
                "weight": 1.2,
                "tag": "offense",
            },
            "power": {
                "name": "劲射",
                "soft_cap": 6,
                "base_desc": "子弹伤害提高",
                "mastery_desc": "精通：每级继续叠加额外伤害",
                "weight": 1.1,
                "tag": "offense",
            },
            "pierce": {
                "name": "穿透",
                "soft_cap": 4,
                "base_desc": "子弹穿透更多敌人",
                "mastery_desc": "精通：周期性追加穿透并附加伤害",
                "weight": 0.95,
                "tag": "offense",
            },
            "multi": {
                "name": "多重射击",
                "soft_cap": 4,
                "base_desc": "额外发射子弹",
                "mastery_desc": "精通：继续扩展子弹数量上限",
                "weight": 0.9,
                "tag": "offense",
            },
            "range": {
                "name": "远射",
                "soft_cap": 5,
                "base_desc": "射程和弹速提升",
                "mastery_desc": "精通：继续提升射程和弹速",
                "weight": 0.9,
                "tag": "offense",
            },
            "crit": {
                "name": "弱点打击",
                "soft_cap": 4,
                "base_desc": "暴击率和暴伤提升",
                "mastery_desc": "精通：暴击属性继续成长",
                "weight": 0.85,
                "tag": "offense",
            },
            "blade": {
                "name": "近战斩击",
                "soft_cap": 6,
                "base_desc": "周期触发前方扇形近战",
                "mastery_desc": "精通：继续强化斩击伤害/范围/频率",
                "weight": 1.0,
                "tag": "offense",
            },
            "swift": {
                "name": "疾行",
                "soft_cap": 5,
                "base_desc": "移动速度提高",
                "mastery_desc": "精通：继续提升移速与机动性",
                "weight": 0.95,
                "tag": "utility",
            },
            "magnet": {
                "name": "磁吸",
                "soft_cap": 5,
                "base_desc": "扩大拾取并增强吸附",
                "mastery_desc": "精通：扩大吸附范围并提升经验增益",
                "weight": 0.88,
                "tag": "utility",
            },
            "tough": {
                "name": "坚韧",
                "soft_cap": 6,
                "base_desc": "最大生命提高",
                "mastery_desc": "精通：继续提升生命上限和续航",
                "weight": 1.0,
                "tag": "defense",
            },
            "regen": {
                "name": "再生",
                "soft_cap": 5,
                "base_desc": "持续回复生命",
                "mastery_desc": "精通：持续提高回复速度",
                "weight": 0.92,
                "tag": "defense",
            },
            "guard": {
                "name": "护盾",
                "soft_cap": 4,
                "base_desc": "减伤并延长无敌帧",
                "mastery_desc": "精通：减伤继续提高",
                "weight": 0.9,
                "tag": "defense",
            },
            "siphon": {
                "name": "汲取",
                "soft_cap": 4,
                "base_desc": "击杀回复生命",
                "mastery_desc": "精通：击杀回血继续提高",
                "weight": 0.84,
                "tag": "defense",
            },
            "nova": {
                "name": "新星",
                "soft_cap": 5,
                "base_desc": "周期爆发范围伤害",
                "mastery_desc": "精通：新星进一步提高伤害和频率",
                "weight": 0.78,
                "tag": "special",
            },
        }

    def current_spawn_interval(self):
        minutes = self.elapsed_ms / 60000.0
        pressure = 1.0 + 0.10 * minutes + 0.035 * self.player.level + 0.008 * self.combo_kills
        if self.horde_active_ms > 0:
            pressure *= 1.45
        interval = BASE_SPAWN_MS / (pressure ** 0.76)
        return max(MIN_SPAWN_MS, int(interval))

    def current_difficulty(self):
        minutes = self.elapsed_ms / 60000.0
        level_factor = (self.player.level ** 1.05) * 0.026
        time_factor = (minutes ** 1.10) * 0.16
        score_factor = math.log1p(self.score / 9000.0) * 0.11 if self.score > 0 else 0.0
        combo_factor = min(1.2, self.combo_kills * 0.017)
        horde_factor = 0.28 if self.horde_active_ms > 0 else 0.0
        return 1.0 + level_factor + time_factor + score_factor + combo_factor + horde_factor

    def current_combo_multiplier(self):
        return 1.0 + min(3.0, self.combo_kills * 0.06)

    def current_frenzy_multiplier(self):
        if self.player.frenzy_timer <= 0 or self.player.frenzy_stacks <= 0:
            return 1.0
        return 1.0 + min(1.6, self.player.frenzy_stacks * 0.11)

    def current_shoot_cooldown(self):
        frenzy_speed = 1.0 + (self.current_frenzy_multiplier() - 1.0) * 0.75
        return max(22, int(self.player.bullet_cooldown / frenzy_speed))

    def current_melee_cooldown(self):
        if self.player.melee_cooldown <= 0:
            return 0
        frenzy_speed = 1.0 + (self.current_frenzy_multiplier() - 1.0) * 0.55
        return max(36, int(self.player.melee_cooldown / frenzy_speed))

    def horde_cycle_ms(self):
        minutes = self.elapsed_ms / 60000.0
        return max(25000, int(62000 - minutes * 2500))

    def horde_duration_ms(self):
        minutes = self.elapsed_ms / 60000.0
        return int(14000 + min(14000, minutes * 750))

    def current_damage_boost(self):
        # Dynamic catch-up: if enemies pile up, player gains burst damage.
        pressure = max(0, len(self.enemies) - 120)
        crowd_bonus = 1.0 + min(1.4, pressure * 0.0042)
        return crowd_bonus * self.current_frenzy_multiplier()

    def current_defense_boost(self):
        pressure = max(0, len(self.enemies) - 130)
        return max(0.72, 1.0 - pressure * 0.0022)

    def current_xp_drop_multiplier(self):
        minutes = self.elapsed_ms / 60000.0
        return 1.0 + min(2.2, 0.08 * minutes + 0.006 * self.player.level)

    def add_score(self, base_points, x=None, y=None):
        difficulty_multiplier = 1.0 + min(4.0, math.log1p(self.current_difficulty()) * 0.55)
        combo_multiplier = self.current_combo_multiplier()
        gain = int(base_points * combo_multiplier * difficulty_multiplier * self.player.score_multiplier)
        gain = max(1, gain)
        self.score += gain
        self.best_score = max(self.best_score, self.score)
        if x is not None and y is not None:
            self.effects.append(
                {
                    "type": "score",
                    "x": x,
                    "y": y,
                    "text": f"+{self.format_number(gain)}",
                    "life": 700,
                    "max_life": 700,
                }
            )
        return gain

    def add_survival_score(self):
        seconds = self.elapsed_ms // 1000
        base = 6 + self.player.level // 3 + seconds // 50
        self.add_score(base)

    def update_combo_state(self, dt_ms):
        if self.combo_timer_ms <= 0:
            return
        self.combo_timer_ms = max(0, self.combo_timer_ms - dt_ms)
        if self.combo_timer_ms == 0:
            self.combo_kills = 0

    def spawn_enemy(self):
        minutes = self.elapsed_ms / 60000.0
        enemy_cap = int(220 + self.player.level * 6 + minutes * 26)
        if self.horde_active_ms > 0:
            enemy_cap = int(enemy_cap * 1.45)
        if len(self.enemies) >= enemy_cap and random.random() < 0.52:
            return

        edge = random.randint(0, 3)
        if edge == 0:
            x, y = random.uniform(0, WIDTH), -24
        elif edge == 1:
            x, y = WIDTH + 24, random.uniform(0, HEIGHT)
        elif edge == 2:
            x, y = random.uniform(0, WIDTH), HEIGHT + 24
        else:
            x, y = -24, random.uniform(0, HEIGHT)

        difficulty = self.current_difficulty()
        hp_scale = difficulty ** 0.84
        speed_scale = 1.0 + (minutes ** 0.72) * 0.12 + (self.player.level ** 0.62) * 0.012
        damage_scale = 1.0 + (minutes ** 0.84) * 0.08 + (self.player.level ** 0.70) * 0.018

        elite_chance = min(0.22, 0.015 + 0.0015 * minutes + self.player.level * 0.0009)
        tank_chance = min(0.46, 0.11 + 0.0032 * (minutes ** 1.24) + self.player.level * 0.0024)
        dash_chance = min(0.34, 0.07 + 0.0030 * (minutes ** 1.20) + self.player.level * 0.0022)
        if self.horde_active_ms > 0:
            elite_chance = min(0.38, elite_chance * 1.9)
            tank_chance = min(0.60, tank_chance * 1.25)
            dash_chance = min(0.45, dash_chance * 1.18)
        roll = random.random()

        if roll < elite_chance:
            speed = random.uniform(ELITE_MIN_SPEED, ELITE_MAX_SPEED) * (speed_scale * 1.05)
            hp = max(16, int(ELITE_HP * (difficulty ** 0.95)))
            damage = max(2, int(ELITE_DAMAGE * (damage_scale * 1.10)))
            enemy = Enemy(
                x,
                y,
                speed,
                hp,
                ELITE_RADIUS,
                ELITE_COLOR,
                damage,
                kind="elite",
                xp_reward=ELITE_XP,
            )
        elif roll < elite_chance + tank_chance:
            speed = random.uniform(TANK_MIN_SPEED, TANK_MAX_SPEED) * speed_scale
            hp = max(7, int(TANK_HP * hp_scale))
            damage = max(1, int(TANK_DAMAGE * damage_scale))
            enemy = Enemy(
                x,
                y,
                speed,
                hp,
                TANK_RADIUS,
                TANK_COLOR,
                damage,
                kind="tank",
                xp_reward=TANK_XP,
            )
        elif roll < elite_chance + tank_chance + dash_chance:
            speed = random.uniform(DASH_MIN_SPEED, DASH_MAX_SPEED) * speed_scale
            hp = max(1, int(DASH_HP * (0.9 + 0.28 * hp_scale)))
            damage = max(1, int(DASH_DAMAGE * damage_scale))
            enemy = Enemy(
                x,
                y,
                speed,
                hp,
                DASH_RADIUS,
                DASH_COLOR,
                damage,
                kind="dash",
                xp_reward=DASH_XP,
            )
        else:
            speed = random.uniform(GRUNT_MIN_SPEED, GRUNT_MAX_SPEED) * speed_scale
            hp = max(1, int(GRUNT_HP * hp_scale))
            damage = max(1, int(GRUNT_DAMAGE * damage_scale))
            enemy = Enemy(
                x,
                y,
                speed,
                hp,
                GRUNT_RADIUS,
                GRUNT_COLOR,
                damage,
                kind="grunt",
                xp_reward=GRUNT_XP,
            )

        self.enemies.append(enemy)

    def spawn_xp_orbs(self, x, y, total_xp):
        scaled = max(1, int(round(total_xp * self.current_xp_drop_multiplier())))
        remaining = scaled
        while remaining > 0:
            if remaining >= 3 and random.random() < 0.32:
                value = 3
            else:
                value = 2 if remaining >= 2 and random.random() < 0.45 else 1
            value = min(value, remaining)
            self.orbs.append(XpOrb(x + random.uniform(-8, 8), y + random.uniform(-8, 8), value))
            remaining -= value

    def on_enemy_killed(self, enemy):
        self.kill_count += 1
        self.combo_kills += 1
        self.longest_combo = max(self.longest_combo, self.combo_kills)
        self.combo_timer_ms = COMBO_WINDOW_MS

        base_points = {
            "grunt": 14,
            "dash": 20,
            "tank": 34,
            "elite": 72,
        }.get(enemy.kind, 14)
        bonus_points = int(enemy.max_hp * 1.8 + enemy.damage * 0.6)
        self.add_score(base_points + bonus_points, enemy.x, enemy.y)

        if enemy.kind == "elite":
            self.player.frenzy_stacks = min(10, self.player.frenzy_stacks + 2)
            self.player.frenzy_timer = max(self.player.frenzy_timer, 9000)
            self.reroll_charges += 1
            self.effects.append(
                {
                    "type": "score",
                    "x": enemy.x,
                    "y": enemy.y - 26,
                    "text": "精英击破！狂热+2 重随+1",
                    "life": 1200,
                    "max_life": 1200,
                }
            )

        if self.combo_kills > 0 and self.combo_kills % 15 == 0:
            self.reroll_charges += 1
            self.effects.append(
                {
                    "type": "score",
                    "x": enemy.x,
                    "y": enemy.y - 20,
                    "text": "连杀奖励 +1 重随",
                    "life": 1000,
                    "max_life": 1000,
                }
            )

        self.spawn_xp_orbs(enemy.x, enemy.y, enemy.xp_reward)
        if self.player.kill_heal > 0:
            self.player.hp = min(self.player.max_hp, self.player.hp + self.player.kill_heal)

    def trigger_nova(self):
        px, py = self.player.x, self.player.y
        radius_sq = self.player.nova_radius * self.player.nova_radius
        survivors = []
        nova_damage = max(
            1, int(self.player.nova_damage * self.player.damage_multiplier * self.current_damage_boost())
        )

        for enemy in self.enemies:
            if (enemy.x - px) * (enemy.x - px) + (enemy.y - py) * (enemy.y - py) <= radius_sq:
                enemy.hp -= nova_damage
                if enemy.hp <= 0:
                    self.on_enemy_killed(enemy)
                    continue
            survivors.append(enemy)

        self.enemies = survivors
        self.effects.append(
            {
                "type": "nova",
                "x": px,
                "y": py,
                "radius": self.player.nova_radius,
                "life": 260,
                "max_life": 260,
            }
        )

    def auto_shoot(self):
        if not self.enemies:
            return

        px, py = self.player.x, self.player.y
        nearest = min(self.enemies, key=lambda e: (e.x - px) * (e.x - px) + (e.y - py) * (e.y - py))

        dx = nearest.x - px
        dy = nearest.y - py
        d_sq = dx * dx + dy * dy
        if d_sq < 1e-6:
            return

        base_angle = math.atan2(dy, dx)
        self.player.aim_angle = base_angle

        count = self.player.shot_count
        spread = 0.17
        offset = -0.5 * (count - 1)
        for i in range(count):
            angle = base_angle + (offset + i) * spread
            vx = math.cos(angle) * self.player.bullet_speed
            vy = math.sin(angle) * self.player.bullet_speed
            self.bullets.append(
                Bullet(
                    px,
                    py,
                    vx,
                    vy,
                    self.player.bullet_damage,
                    self.player.pierce,
                    self.player.bullet_range,
                )
            )

    def update_player(self, dt_ms):
        dt_s = dt_ms / 1000.0
        keys = pygame.key.get_pressed()

        # Support both WASD and arrow keys for movement.
        move_x = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(
            keys[pygame.K_a] or keys[pygame.K_LEFT]
        )
        move_y = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(
            keys[pygame.K_w] or keys[pygame.K_UP]
        )
        if move_x and move_y:
            move_x *= 0.70710678
            move_y *= 0.70710678

        dx = move_x * self.player.speed * dt_s
        dy = move_y * self.player.speed * dt_s
        self.player.move(dx, dy)

        if move_x or move_y:
            self.player.aim_angle = math.atan2(move_y, move_x)

        if self.player.regen > 0 and self.player.hp > 0:
            self.player.hp = min(self.player.max_hp, self.player.hp + self.player.regen * dt_s)

        if self.player.hit_timer > 0:
            self.player.hit_timer = max(0, self.player.hit_timer - dt_ms)

        if self.player.frenzy_timer > 0:
            self.player.frenzy_timer = max(0, self.player.frenzy_timer - dt_ms)
            if self.player.frenzy_timer == 0:
                self.player.frenzy_stacks = 0

    def update_enemies(self, dt_s):
        for enemy in self.enemies:
            enemy.update(self.player, dt_s)

    def update_bullets(self, dt_s):
        alive = []
        for bullet in self.bullets:
            if bullet.update(dt_s):
                alive.append(bullet)
        self.bullets = alive

    def update_orbs(self, dt_s):
        if not self.orbs:
            return

        px, py = self.player.x, self.player.y
        pickup_sq = self.player.pickup_radius * self.player.pickup_radius
        pull_radius = self.player.pickup_radius * 4.6
        pull_sq = pull_radius * pull_radius

        remaining_orbs = []
        gained_levels = []

        damping = max(0.0, 1.0 - 4.2 * dt_s)

        for orb in self.orbs:
            dx = px - orb.x
            dy = py - orb.y
            d_sq = dx * dx + dy * dy

            if d_sq <= pickup_sq:
                xp_gain = max(1, int(round(orb.value * self.player.xp_multiplier)))
                gained_levels.extend(self.player.gain_xp(xp_gain))
                continue

            if d_sq <= pull_sq and d_sq > 1e-6:
                inv_d = 1.0 / math.sqrt(d_sq)
                accel = self.player.orb_pull_strength * (1.0 + 120.0 / (math.sqrt(d_sq) + 40.0))
                orb.vx += dx * inv_d * accel * dt_s
                orb.vy += dy * inv_d * accel * dt_s

            orb.vx *= damping
            orb.vy *= damping
            orb.x += orb.vx * dt_s
            orb.y += orb.vy * dt_s
            remaining_orbs.append(orb)

        self.orbs = remaining_orbs

        if gained_levels:
            self.pending_levels += len(gained_levels)
            self.reroll_charges += sum(1 for level in gained_levels if level % 4 == 0)
            if len(gained_levels) >= 2:
                self.add_score(24 * len(gained_levels))
            if not self.leveling:
                self.start_level_up()

    def trigger_melee_slash(self):
        if self.player.melee_level <= 0 or not self.enemies:
            return

        px, py = self.player.x, self.player.y
        nearest = min(self.enemies, key=lambda e: (e.x - px) * (e.x - px) + (e.y - py) * (e.y - py))
        slash_angle = math.atan2(nearest.y - py, nearest.x - px)
        self.player.aim_angle = slash_angle

        slash_range = max(24.0, self.player.melee_range)
        slash_arc = max(math.radians(45), self.player.melee_arc)
        arc_half = slash_arc * 0.5
        max_hits = max(1, int(self.player.melee_hit_limit))
        base_damage = max(
            1.0, self.player.melee_damage * self.player.damage_multiplier * self.current_damage_boost()
        )

        enemy_grid = self.build_enemy_grid()
        cell_r = int((slash_range + 28) // GRID_SIZE) + 1
        cx = int(px // GRID_SIZE)
        cy = int(py // GRID_SIZE)

        dead_indices = set()
        hit_count = 0
        stop = False

        for gx in range(cx - cell_r, cx + cell_r + 1):
            if stop:
                break
            for gy in range(cy - cell_r, cy + cell_r + 1):
                if stop:
                    break
                for enemy_i in enemy_grid.get((gx, gy), ()):
                    if enemy_i in dead_indices:
                        continue
                    enemy = self.enemies[enemy_i]
                    dx = enemy.x - px
                    dy = enemy.y - py
                    d_sq = dx * dx + dy * dy
                    reach = slash_range + enemy.radius
                    if d_sq > reach * reach:
                        continue

                    enemy_angle = math.atan2(dy, dx)
                    if abs_angle_delta(enemy_angle, slash_angle) > arc_half:
                        continue

                    damage = base_damage
                    if random.random() < min(0.75, self.player.crit_chance * 0.75):
                        damage = max(damage + 1.0, damage * (1.0 + self.player.crit_multiplier * 0.45))
                        self.effects.append(
                            {
                                "type": "spark",
                                "x": enemy.x,
                                "y": enemy.y,
                                "life": 120,
                                "max_life": 120,
                            }
                        )

                    enemy.hp -= max(1, int(damage))
                    if d_sq > 1e-6:
                        inv_d = 1.0 / math.sqrt(d_sq)
                        knock = 12.0 + min(18.0, self.player.melee_level * 0.5)
                        enemy.x += dx * inv_d * knock
                        enemy.y += dy * inv_d * knock

                    hit_count += 1
                    if enemy.hp <= 0:
                        dead_indices.add(enemy_i)

                    if hit_count >= max_hits:
                        stop = True
                        break

        if dead_indices:
            survivors = []
            for i, enemy in enumerate(self.enemies):
                if i in dead_indices:
                    self.on_enemy_killed(enemy)
                else:
                    survivors.append(enemy)
            self.enemies = survivors

        self.effects.append(
            {
                "type": "slash",
                "x": px,
                "y": py,
                "angle": slash_angle,
                "arc": slash_arc,
                "radius": slash_range,
                "life": 150,
                "max_life": 150,
            }
        )

    def update_melee(self, dt_ms):
        if self.player.melee_level <= 0 or self.player.melee_cooldown <= 0:
            self.melee_timer = 0
            return

        cooldown = self.current_melee_cooldown()
        if cooldown <= 0:
            self.melee_timer = 0
            return

        if not self.enemies:
            self.melee_timer = min(cooldown, self.melee_timer + dt_ms)
            return

        self.melee_timer += dt_ms
        while self.melee_timer >= cooldown:
            self.melee_timer -= cooldown
            self.trigger_melee_slash()

    def build_enemy_grid(self):
        grid = {}
        for i, enemy in enumerate(self.enemies):
            key = (int(enemy.x // GRID_SIZE), int(enemy.y // GRID_SIZE))
            if key in grid:
                grid[key].append(i)
            else:
                grid[key] = [i]
        return grid

    def handle_collisions(self):
        px, py = self.player.x, self.player.y

        # Bullets vs enemies (grid acceleration)
        if self.bullets and self.enemies:
            enemy_grid = self.build_enemy_grid()
            dead_indices = set()

            for bullet in self.bullets:
                if bullet.life <= 0:
                    continue

                bx = int(bullet.x // GRID_SIZE)
                by = int(bullet.y // GRID_SIZE)
                checked = set()

                hit_stopped = False
                for gx in range(bx - 1, bx + 2):
                    for gy in range(by - 1, by + 2):
                        for enemy_i in enemy_grid.get((gx, gy), ()):  # nearby only
                            if enemy_i in dead_indices or enemy_i in checked:
                                continue
                            checked.add(enemy_i)

                            enemy = self.enemies[enemy_i]
                            rr = enemy.radius + BULLET_RADIUS
                            if (bullet.x - enemy.x) * (bullet.x - enemy.x) + (bullet.y - enemy.y) * (
                                bullet.y - enemy.y
                            ) <= rr * rr:
                                damage = (
                                    bullet.damage
                                    * self.player.damage_multiplier
                                    * self.current_damage_boost()
                                )
                                if random.random() < self.player.crit_chance:
                                    damage = max(damage + 1.0, damage * self.player.crit_multiplier)
                                    self.effects.append(
                                        {
                                            "type": "spark",
                                            "x": enemy.x,
                                            "y": enemy.y,
                                            "life": 120,
                                            "max_life": 120,
                                        }
                                    )

                                enemy.hp -= max(1, int(damage))
                                if enemy.hp <= 0:
                                    dead_indices.add(enemy_i)

                                if bullet.pierce > 0:
                                    bullet.pierce -= 1
                                else:
                                    bullet.life = 0
                                    hit_stopped = True
                                    break

                        if hit_stopped:
                            break
                    if hit_stopped:
                        break

            if dead_indices:
                survivors = []
                for i, enemy in enumerate(self.enemies):
                    if i in dead_indices:
                        self.on_enemy_killed(enemy)
                    else:
                        survivors.append(enemy)
                self.enemies = survivors

            self.bullets = [bullet for bullet in self.bullets if bullet.life > 0]

        # Enemies vs player
        pr = PLAYER_RADIUS
        for enemy in self.enemies:
            rr = enemy.radius + pr
            if (enemy.x - px) * (enemy.x - px) + (enemy.y - py) * (enemy.y - py) <= rr * rr:
                if self.player.hit_timer == 0:
                    dmg = int(enemy.damage * (1.0 - self.player.damage_reduction))
                    dmg = int(max(1, dmg * self.current_defense_boost()))
                    dmg = max(1, dmg)
                    self.player.hp -= dmg
                    self.player.hit_timer = self.player.hit_cooldown_ms
                    if self.player.hp <= 0:
                        self.player.hp = 0
                        self.best_score = max(self.best_score, self.score)
                        self.game_over = True
                        return

    def update_effects(self, dt_ms):
        if not self.effects:
            return
        remaining = []
        for fx in self.effects:
            fx["life"] -= dt_ms
            if fx["life"] > 0:
                remaining.append(fx)
        self.effects = remaining

    def draw_effects(self):
        for fx in self.effects:
            life_ratio = fx["life"] / fx["max_life"]
            if fx["type"] == "nova":
                progress = 1.0 - life_ratio
                radius = max(8, int(fx["radius"] * progress))
                alpha = int(220 * life_ratio)
                surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, (*NOVA_EFFECT_COLOR, alpha), (radius, radius), radius, 4)
                self.screen.blit(surf, (fx["x"] - radius, fx["y"] - radius))

            elif fx["type"] == "spark":
                radius = max(2, int(8 * life_ratio))
                alpha = int(255 * life_ratio)
                surf = pygame.Surface((radius * 2 + 8, radius * 2 + 8), pygame.SRCALPHA)
                c = radius + 4
                pygame.draw.circle(surf, (255, 238, 160, alpha), (c, c), radius)
                pygame.draw.circle(surf, (255, 175, 120, alpha), (c, c), max(1, radius - 1), 1)
                self.screen.blit(surf, (fx["x"] - c, fx["y"] - c))

            elif fx["type"] == "slash":
                radius = int(fx["radius"])
                alpha = int(220 * life_ratio)
                width = max(2, int(10 * life_ratio))
                size = radius * 2 + 20
                surf = pygame.Surface((size, size), pygame.SRCALPHA)
                c = size // 2
                rect = pygame.Rect(10, 10, radius * 2, radius * 2)
                start = fx["angle"] - fx["arc"] * 0.5
                end = fx["angle"] + fx["arc"] * 0.5
                color = (255, 216, 160, alpha)
                pygame.draw.arc(surf, color, rect, start, end, width)
                tip_x = c + int(math.cos(end) * radius)
                tip_y = c + int(math.sin(end) * radius)
                pygame.draw.circle(surf, (255, 236, 180, alpha), (tip_x, tip_y), max(1, width - 1))
                self.screen.blit(surf, (fx["x"] - c, fx["y"] - c))

            elif fx["type"] == "score":
                rise = int((1.0 - life_ratio) * 26)
                alpha = int(255 * life_ratio)
                text_surface = self.font.render(fx["text"], True, (255, 236, 170))
                text_surface.set_alpha(alpha)
                self.screen.blit(text_surface, (fx["x"] - text_surface.get_width() // 2, fx["y"] - rise))

    def skill_weight(self, key):
        meta = self.skill_defs[key]
        level = self.player.skills.get(key, 0)
        soft_cap = meta["soft_cap"]
        mastery_depth = max(0, level - soft_cap)

        weight = meta["weight"] * (1.0 + 0.18 * level)

        if key in self.last_level_options:
            weight *= 0.62

        hp_ratio = self.player.hp / self.player.max_hp if self.player.max_hp else 0.0
        if hp_ratio < 0.45 and meta["tag"] == "defense":
            weight *= 1.85
        if hp_ratio < 0.35 and key in ("guard", "tough", "regen", "siphon"):
            weight *= 1.35

        if self.player.shot_count >= 3 and key in ("power", "pierce", "rapid", "crit"):
            weight *= 1.28
        if self.player.shot_count >= 3 and key == "blade":
            weight *= 1.12
        if len(self.enemies) > 120 and meta["tag"] == "offense":
            weight *= 1.35
        if len(self.enemies) > 180 and key in ("rapid", "power", "multi", "blade", "nova"):
            weight *= 1.45

        if self.player.nova_level == 0 and self.player.level >= 4 and key == "nova":
            weight *= 1.45
        if self.player.melee_level == 0 and self.player.level >= 2 and key == "blade":
            weight *= 1.30

        if key == "rapid" and self.player.bullet_cooldown <= 95:
            weight *= 0.40
        if key == "multi" and self.player.shot_count >= 6:
            weight *= 0.45
        if key == "guard" and self.player.damage_reduction >= 0.32:
            weight *= 0.70
        if key == "blade" and self.player.melee_level > 0 and self.player.melee_cooldown <= 120:
            weight *= 0.58
        if mastery_depth > 0:
            weight *= max(0.28, 0.75 / (1.0 + mastery_depth * 0.07))

        return max(0.05, weight)

    def weighted_pick(self, options):
        weights = [self.skill_weight(key) for key in options]
        total = sum(weights)
        if total <= 0:
            return random.choice(options)

        target = random.uniform(0.0, total)
        cumulative = 0.0
        for key, weight in zip(options, weights):
            cumulative += weight
            if target <= cumulative:
                return key

        return options[-1]

    def roll_level_up_options(self, previous=None):
        available = list(self.skill_defs.keys())
        if not available:
            return []

        count = min(3, len(available))

        best = []
        for _ in range(4):
            pool = available[:]
            current = []
            for _ in range(count):
                choice = self.weighted_pick(pool)
                current.append(choice)
                pool.remove(choice)

            if not previous or len(available) <= count or set(current) != set(previous):
                best = current
                break
            best = current

        self.last_level_options = best[:]
        return best

    def start_level_up(self):
        self.leveling = True
        self.level_up_options = self.roll_level_up_options(previous=self.level_up_options)

    def mastery_preview_text(self, key):
        depth = max(1, self.player.skills.get(key, 0) - self.skill_defs[key]["soft_cap"] + 1)
        if key == "rapid":
            nxt = max(34, int(self.player.bullet_cooldown * 0.985))
            return f"精通{depth}：冷却进一步降低 -> {nxt}ms，全局伤害 +2.0%"
        if key == "power":
            return f"精通{depth}：子弹伤害 +0.55，全局伤害 +2.0%"
        if key == "pierce":
            if depth % 3 == 0:
                return f"精通{depth}：额外穿透 +1，并附带伤害成长"
            return f"精通{depth}：附加伤害 +0.24，全局伤害 +2.0%"
        if key == "multi":
            return f"精通{depth}：周期增加子弹数（上限12）"
        if key == "range":
            return f"精通{depth}：射程 +25，弹速 +12"
        if key == "crit":
            return f"精通{depth}：暴击率 +2%，暴伤 +0.05"
        if key == "blade":
            next_cd = max(54, int(self.player.melee_cooldown * 0.975))
            return f"精通{depth}：斩击伤害 +1.3，冷却 {int(self.player.melee_cooldown)}ms -> {next_cd}ms"
        if key == "swift":
            return f"精通{depth}：移速 +10"
        if key == "magnet":
            return f"精通{depth}：拾取 +12，经验倍率继续成长"
        if key == "tough":
            return f"精通{depth}：最大生命 +6，并回复4点"
        if key == "regen":
            return f"精通{depth}：每秒回血 +0.12"
        if key == "guard":
            return f"精通{depth}：减伤 +1.5%，并延长无敌帧"
        if key == "siphon":
            return f"精通{depth}：击杀回血 +0.35"
        if key == "nova":
            return f"精通{depth}：新星伤害/范围提升，冷却进一步缩短"
        return f"精通{depth}：全局成长提升"

    def skill_preview_text(self, key):
        level = self.player.skills.get(key, 0)
        soft_cap = self.skill_defs[key]["soft_cap"]
        if level >= soft_cap:
            return self.mastery_preview_text(key)

        if key == "rapid":
            cur = int(self.player.bullet_cooldown)
            nxt = max(54, int(self.player.bullet_cooldown * 0.87))
            return f"冷却 {cur}ms -> {nxt}ms"
        if key == "power":
            return f"伤害 {self.player.bullet_damage:.1f} -> {self.player.bullet_damage + 1.5:.1f}"
        if key == "pierce":
            return f"穿透 {self.player.pierce} -> {self.player.pierce + 1}"
        if key == "multi":
            return f"子弹数 {self.player.shot_count} -> {min(9, self.player.shot_count + 1)}"
        if key == "range":
            return (
                f"射程 {int(self.player.bullet_range)} -> {int(self.player.bullet_range + 90)}，"
                f"弹速 {int(self.player.bullet_speed)} -> {int(self.player.bullet_speed + 55)}"
            )
        if key == "crit":
            chance = int(self.player.crit_chance * 100)
            next_chance = int(min(0.65, self.player.crit_chance + 0.10) * 100)
            return f"暴击率 {chance}% -> {next_chance}%，暴伤 +0.25"
        if key == "blade":
            if self.player.melee_level == 0:
                return "解锁：自动扇形斩击（前方）"
            next_cd = max(95, int(self.player.melee_cooldown * 0.88))
            next_dmg = self.player.melee_damage + 3.1
            next_range = int(self.player.melee_range + 10)
            return (
                f"斩击伤害 {self.player.melee_damage:.1f} -> {next_dmg:.1f}，"
                f"冷却 {int(self.player.melee_cooldown)}ms -> {next_cd}ms，范围 -> {next_range}"
            )
        if key == "swift":
            return f"移速 {int(self.player.speed)} -> {int(self.player.speed + 25)}"
        if key == "magnet":
            return "拾取半径 +22，吸附强度 x1.15"
        if key == "tough":
            return f"最大生命 {int(self.player.max_hp)} -> {int(self.player.max_hp + 10)}"
        if key == "regen":
            return f"每秒回血 {self.player.regen:.1f} -> {self.player.regen + 0.3:.1f}"
        if key == "guard":
            reduction = int(self.player.damage_reduction * 100)
            next_reduction = int(min(0.5, self.player.damage_reduction + 0.04) * 100)
            return f"减伤 {reduction}% -> {next_reduction}%，无敌帧更长"
        if key == "siphon":
            return f"击杀回复 {self.player.kill_heal:.1f} -> {self.player.kill_heal + 0.8:.1f}"
        if key == "nova":
            if self.player.nova_level == 0:
                return "解锁：7秒冷却，范围伤害"
            return (
                f"伤害 {self.player.nova_damage} -> {self.player.nova_damage + 4}，"
                f"范围 {self.player.nova_radius} -> {self.player.nova_radius + 24}"
            )
        return self.skill_defs[key]["base_desc"]
    def apply_skill(self, key):
        prev_level = self.player.skills.get(key, 0)
        level = prev_level + 1
        self.player.skills[key] = level
        soft_cap = self.skill_defs[key]["soft_cap"]

        if level <= soft_cap:
            if key == "rapid":
                self.player.bullet_cooldown = max(54, int(self.player.bullet_cooldown * 0.87))
            elif key == "power":
                self.player.bullet_damage += 1.5
            elif key == "pierce":
                self.player.pierce += 1
            elif key == "multi":
                self.player.shot_count = min(9, self.player.shot_count + 1)
            elif key == "range":
                self.player.bullet_range += 90
                self.player.bullet_speed += 55
            elif key == "crit":
                self.player.crit_chance = min(0.65, self.player.crit_chance + 0.10)
                self.player.crit_multiplier += 0.25
            elif key == "blade":
                self.player.melee_level = level
                if level == 1 or self.player.melee_cooldown <= 0:
                    self.player.melee_cooldown = 760
                    self.player.melee_damage = 7.0
                    self.player.melee_range = 92.0
                    self.player.melee_arc = math.radians(118)
                    self.player.melee_hit_limit = 4
                else:
                    self.player.melee_cooldown = max(95, int(self.player.melee_cooldown * 0.88))
                    self.player.melee_damage += 3.1
                    self.player.melee_range += 10.0
                    self.player.melee_arc = min(math.radians(190), self.player.melee_arc + math.radians(9))
                    if level % 2 == 0:
                        self.player.melee_hit_limit = min(18, self.player.melee_hit_limit + 1)
            elif key == "swift":
                self.player.speed += 25
            elif key == "magnet":
                self.player.pickup_radius += 22
                self.player.orb_pull_strength *= 1.15
            elif key == "tough":
                self.player.max_hp += 10
                self.player.hp = min(self.player.max_hp, self.player.hp + 10)
            elif key == "regen":
                self.player.regen += 0.3
            elif key == "guard":
                self.player.damage_reduction = min(0.5, self.player.damage_reduction + 0.04)
                self.player.hit_cooldown_ms = min(900, self.player.hit_cooldown_ms + 40)
            elif key == "siphon":
                self.player.kill_heal += 0.8
            elif key == "nova":
                self.player.nova_level = level
                if level == 1:
                    self.player.nova_cooldown = 6200
                    self.player.nova_damage = 6.0
                    self.player.nova_radius = 108
                else:
                    self.player.nova_cooldown = max(900, int(self.player.nova_cooldown * 0.86))
                    self.player.nova_damage += 4.0
                    self.player.nova_radius += 24
            return

        self.apply_mastery_bonus(key, level - soft_cap)

    def apply_mastery_bonus(self, key, mastery_level):
        self.player.damage_multiplier *= 1.020
        self.player.score_multiplier *= 1.018

        if mastery_level % 5 == 0:
            self.reroll_charges += 1

        if key == "rapid":
            self.player.bullet_cooldown = max(28, int(self.player.bullet_cooldown * 0.98))
        elif key == "power":
            self.player.bullet_damage += 0.55
        elif key == "pierce":
            self.player.bullet_damage += 0.24
            if mastery_level % 3 == 0:
                self.player.pierce += 1
        elif key == "multi":
            if mastery_level % 3 == 0:
                self.player.shot_count = min(15, self.player.shot_count + 1)
            else:
                self.player.bullet_damage += 0.20
        elif key == "range":
            self.player.bullet_range += 38
            self.player.bullet_speed += 18
        elif key == "crit":
            self.player.crit_chance = min(0.92, self.player.crit_chance + 0.03)
            self.player.crit_multiplier += 0.08
        elif key == "blade":
            self.player.melee_level = max(self.player.melee_level + 1, self.player.skills.get("blade", 0))
            if self.player.melee_cooldown <= 0:
                self.player.melee_cooldown = 760
                self.player.melee_damage = max(self.player.melee_damage, 7.0)
                self.player.melee_range = max(self.player.melee_range, 92.0)
                self.player.melee_arc = max(self.player.melee_arc, math.radians(118))
                self.player.melee_hit_limit = max(self.player.melee_hit_limit, 4)
            self.player.melee_cooldown = max(54, int(self.player.melee_cooldown * 0.975))
            self.player.melee_damage += 1.3
            if mastery_level % 3 == 0:
                self.player.melee_range += 3.0
            if mastery_level % 4 == 0:
                self.player.melee_arc = min(math.radians(240), self.player.melee_arc + math.radians(5))
            if mastery_level % 6 == 0:
                self.player.melee_hit_limit = min(24, self.player.melee_hit_limit + 1)
        elif key == "swift":
            self.player.speed += 10
        elif key == "magnet":
            self.player.pickup_radius += 12
            self.player.orb_pull_strength *= 1.05
            self.player.xp_multiplier *= 1.01
        elif key == "tough":
            self.player.max_hp += 6
            self.player.hp = min(self.player.max_hp, self.player.hp + 4)
        elif key == "regen":
            self.player.regen += 0.12
        elif key == "guard":
            self.player.damage_reduction = min(0.80, self.player.damage_reduction + 0.015)
            self.player.hit_cooldown_ms = min(1200, self.player.hit_cooldown_ms + 8)
        elif key == "siphon":
            self.player.kill_heal += 0.35
        elif key == "nova":
            self.player.nova_level += 1
            if self.player.nova_cooldown <= 0:
                self.player.nova_cooldown = 6200
                self.player.nova_damage = max(self.player.nova_damage, 6.0)
                self.player.nova_radius = max(self.player.nova_radius, 108)
            self.player.nova_cooldown = max(360, int(self.player.nova_cooldown * 0.95))
            self.player.nova_damage += 1.8
            self.player.nova_radius += 10

    def choose_level_up(self, choice_index):
        chosen = False
        if self.level_up_options and 0 <= choice_index < len(self.level_up_options):
            key = self.level_up_options[choice_index]
            self.apply_skill(key)
            chosen = True

        if chosen:
            self.add_score(42 + self.player.level * 2)

        self.pending_levels = max(0, self.pending_levels - 1)
        if self.pending_levels > 0:
            self.start_level_up()
        else:
            self.leveling = False
            self.level_up_options = []

    def reroll_level_up(self):
        if self.reroll_charges <= 0 or not self.level_up_options:
            return
        prev = self.level_up_options[:]
        self.level_up_options = self.roll_level_up_options(previous=prev)
        self.reroll_charges -= 1

    def draw_world(self):
        self.screen.blit(self.background, (0, 0))

        if self.horde_active_ms > 0:
            pulse = 20 + int((self.horde_active_ms % 360) / 18)
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (130, 36, 36, 44), (0, 0, WIDTH, HEIGHT), width=pulse)
            self.screen.blit(overlay, (0, 0))

        for orb in self.orbs:
            r = XP_ORB_RADIUS + min(2, orb.value - 1)
            pygame.draw.circle(self.screen, XP_COLOR, (int(orb.x), int(orb.y)), r)
            pygame.draw.circle(self.screen, (255, 246, 180), (int(orb.x), int(orb.y)), max(1, r - 2), 1)

        for bullet in self.bullets:
            px = bullet.x - bullet.vx * 0.018
            py = bullet.y - bullet.vy * 0.018
            pygame.draw.line(self.screen, (90, 140, 220), (px, py), (bullet.x, bullet.y), 2)
            pygame.draw.circle(self.screen, BULLET_COLOR, (int(bullet.x), int(bullet.y)), BULLET_RADIUS)

        for enemy in self.enemies:
            sprite = self.sprites.get(enemy.kind)
            if sprite is not None:
                rect = sprite.get_rect(center=(int(enemy.x), int(enemy.y)))
                self.screen.blit(sprite, rect)
            else:
                pygame.draw.circle(self.screen, enemy.color, (int(enemy.x), int(enemy.y)), enemy.radius)
            enemy.draw_hp_bar(self.screen)

        player_sprite = self.sprites["player"]
        angle_deg = -math.degrees(self.player.aim_angle) - 90
        rotated = pygame.transform.rotozoom(player_sprite, angle_deg, 1.0)
        rect = rotated.get_rect(center=(int(self.player.x), int(self.player.y)))
        self.screen.blit(rotated, rect)

        if self.player.hit_timer > 0:
            pulse = 4 + int((self.player.hit_timer % 180) / 45)
            pygame.draw.circle(
                self.screen,
                PLAYER_FLASH,
                (int(self.player.x), int(self.player.y)),
                PLAYER_RADIUS + pulse,
                2,
            )

        self.draw_effects()

    def draw_ui(self):
        hp_ratio = self.player.hp / self.player.max_hp if self.player.max_hp else 0.0
        xp_ratio = self.player.xp / self.player.xp_next if self.player.xp_next else 0.0

        panel = pygame.Surface((430, 258), pygame.SRCALPHA)
        panel.fill((8, 12, 20, 186))
        self.screen.blit(panel, (14, 12))

        # HP
        pygame.draw.rect(self.screen, (60, 70, 84), (28, 28, 250, 16), border_radius=4)
        pygame.draw.rect(self.screen, (82, 210, 130), (28, 28, int(250 * hp_ratio), 16), border_radius=4)
        hp_text = self.font.render(
            f"HP {int(self.player.hp)}/{int(self.player.max_hp)}", True, TEXT_COLOR
        )
        self.screen.blit(hp_text, (290, 24))

        # XP
        pygame.draw.rect(self.screen, (60, 70, 84), (28, 52, 250, 12), border_radius=4)
        pygame.draw.rect(self.screen, (112, 166, 242), (28, 52, int(250 * xp_ratio), 12), border_radius=4)
        lv_text = self.font.render(f"等级 {self.player.level}", True, TEXT_COLOR)
        self.screen.blit(lv_text, (290, 48))

        sec = self.elapsed_ms // 1000
        time_text = self.font.render(
            f"时间 {sec // 60:02d}:{sec % 60:02d}   击杀 {self.kill_count}   敌人 {len(self.enemies)}",
            True,
            TEXT_COLOR,
        )
        self.screen.blit(time_text, (28, 76))

        score_text = self.font.render(
            f"分数 {self.format_number(self.score)}   最高 {self.format_number(self.best_score)}",
            True,
            (238, 228, 176),
        )
        self.screen.blit(score_text, (28, 100))

        combo_mult = self.current_combo_multiplier()
        if self.combo_kills > 1:
            combo_sec = self.combo_timer_ms / 1000.0
            combo_text = self.font.render(
                f"连杀 {self.combo_kills}x   倍率 x{combo_mult:.2f}   倒计时 {combo_sec:.1f}s",
                True,
                (255, 188, 124),
            )
        else:
            combo_text = self.font.render("连杀 0x   倍率 x1.00", True, (188, 206, 225))
        self.screen.blit(combo_text, (28, 122))

        diff_text = self.font.render(
            f"难度系数 {self.current_difficulty():.2f}   重随 R: {self.reroll_charges}",
            True,
            (198, 214, 230),
        )
        self.screen.blit(diff_text, (28, 144))

        boost_text = self.font.render(
            f"火力补正 x{self.current_damage_boost():.2f}   抗压减伤 x{self.current_defense_boost():.2f}",
            True,
            (236, 204, 166),
        )
        self.screen.blit(boost_text, (28, 164))

        frenzy_text = self.font.render(
            f"狂热层数 {self.player.frenzy_stacks}  倍率 x{self.current_frenzy_multiplier():.2f}",
            True,
            (252, 188, 132),
        )
        self.screen.blit(frenzy_text, (28, 184))

        if self.horde_active_ms > 0:
            horde_sec = self.horde_active_ms / 1000.0
            horde_text = self.font.render(
                f"狂潮进行中 第{self.horde_count}波  剩余 {horde_sec:.1f}s",
                True,
                (255, 148, 130),
            )
        else:
            wait_sec = max(0.0, (self.horde_cycle_ms() - self.horde_timer) / 1000.0)
            horde_text = self.font.render(
                f"下波狂潮倒计时 {wait_sec:.1f}s",
                True,
                (188, 206, 225),
            )
        self.screen.blit(horde_text, (28, 204))

        if self.player.melee_level > 0 and self.player.melee_cooldown > 0:
            melee_cd = max(1, self.current_melee_cooldown())
            ready_ratio = min(1.0, self.melee_timer / melee_cd)
            pygame.draw.rect(self.screen, (64, 60, 54), (28, 228, 250, 10), border_radius=4)
            fill_color = (236, 160, 102) if ready_ratio >= 1.0 else (180, 120, 90)
            pygame.draw.rect(self.screen, fill_color, (28, 228, int(250 * ready_ratio), 10), border_radius=4)
            melee_text = self.font.render(
                f"近战 Lv {self.player.melee_level} 伤害 {self.player.melee_damage:.1f} 充能 {int(ready_ratio * 100)}%",
                True,
                (245, 210, 170),
            )
            self.screen.blit(melee_text, (290, 222))
        else:
            melee_text = self.font.render("近战：未解锁", True, (164, 176, 190))
            self.screen.blit(melee_text, (28, 222))

        # Skill summary
        right_panel = pygame.Surface((340, 180), pygame.SRCALPHA)
        right_panel.fill((8, 12, 20, 170))
        self.screen.blit(right_panel, (WIDTH - 354, 12))

        title = self.font.render("当前流派", True, (220, 235, 248))
        self.screen.blit(title, (WIDTH - 340, 20))

        y = 46
        top_skills = sorted(self.player.skills.items(), key=lambda item: item[1], reverse=True)[:7]
        for key, level in top_skills:
            name = self.skill_defs[key]["name"]
            soft_cap = self.skill_defs[key]["soft_cap"]
            if level <= soft_cap:
                label = f"{name} Lv {level}/{soft_cap}"
            else:
                label = f"{name} 精通 {level - soft_cap}"
            txt = self.font.render(label, True, (178, 202, 220))
            self.screen.blit(txt, (WIDTH - 340, y))
            y += 21

    def draw_level_up(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 10, 16, 210))
        self.screen.blit(overlay, (0, 0))

        title = self.big_font.render("升级选择", True, (236, 244, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 96))

        hint = self.font.render("按 1-3 选择，按 R 重随（超过软上限进入精通）", True, (182, 200, 216))
        self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 142))

        reroll = self.font.render(f"可用重随: {self.reroll_charges}", True, (208, 220, 232))
        self.screen.blit(reroll, (WIDTH // 2 - reroll.get_width() // 2, 166))

        if not self.level_up_options:
            no_option = self.font.render("技能池为空，按 1 继续", True, TEXT_COLOR)
            self.screen.blit(no_option, (WIDTH // 2 - no_option.get_width() // 2, 234))
            return

        tag_color = {
            "offense": (106, 70, 60),
            "defense": (58, 88, 72),
            "utility": (60, 74, 102),
            "special": (92, 68, 106),
        }

        card_w = 740
        card_h = 104
        start_y = 204
        gap = 116

        for i, key in enumerate(self.level_up_options, start=1):
            meta = self.skill_defs[key]
            rank = self.player.skills.get(key, 0)
            soft_cap = meta["soft_cap"]
            color = tag_color.get(meta["tag"], (64, 64, 64))

            x = (WIDTH - card_w) // 2
            y = start_y + (i - 1) * gap

            pygame.draw.rect(self.screen, (16, 20, 28), (x, y, card_w, card_h), border_radius=10)
            pygame.draw.rect(self.screen, color, (x + 4, y + 4, card_w - 8, card_h - 8), 2, border_radius=8)

            if rank < soft_cap:
                rank_text = f"Lv {rank + 1}/{soft_cap}"
                brief = meta["base_desc"]
            else:
                rank_text = f"精通 {rank - soft_cap + 1}"
                brief = meta["mastery_desc"]
            title_text = self.font.render(f"{i}. {meta['name']}  {rank_text}", True, (230, 240, 250))
            desc_text = self.font.render(self.skill_preview_text(key), True, (176, 198, 216))
            brief_text = self.font.render(brief, True, (156, 176, 194))

            self.screen.blit(title_text, (x + 24, y + 18))
            self.screen.blit(desc_text, (x + 24, y + 45))
            self.screen.blit(brief_text, (x + 24, y + 71))

    def draw_game_over(self):
        msg = self.big_font.render("游戏结束", True, (250, 102, 96))
        rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        self.screen.blit(msg, rect)

        score_line = self.font.render(
            f"本局分数 {self.format_number(self.score)}   最高分 {self.format_number(self.best_score)}",
            True,
            (255, 224, 164),
        )
        score_rect = score_line.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 18))
        self.screen.blit(score_line, score_rect)

        combo_line = self.font.render(f"最长连杀 {self.longest_combo}", True, (232, 206, 186))
        combo_rect = combo_line.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 46))
        self.screen.blit(combo_line, combo_rect)

        horde_line = self.font.render(f"经历狂潮波次 {self.horde_count}", True, (232, 180, 164))
        horde_rect = horde_line.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
        self.screen.blit(horde_line, horde_rect)

        sub = self.font.render("按 R 重新开始，按 ESC 退出", True, TEXT_COLOR)
        rect2 = sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 98))
        self.screen.blit(sub, rect2)

    def draw(self):
        self.draw_world()
        self.draw_ui()

        if self.leveling:
            self.draw_level_up()

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()
    def reset(self):
        self.best_score = max(self.best_score, self.score)

        self.player = Player()
        self.enemies = []
        self.bullets = []
        self.orbs = []
        self.effects = []

        self.spawn_timer = 0
        self.shoot_timer = 0
        self.melee_timer = 0
        self.nova_timer = 0
        self.horde_timer = 0
        self.horde_active_ms = 0
        self.horde_count = 0
        self.elapsed_ms = 0

        self.game_over = False
        self.leveling = False
        self.pending_levels = 0
        self.level_up_options = []
        self.last_level_options = []

        self.kill_count = 0
        self.score = 0
        self.combo_kills = 0
        self.longest_combo = 0
        self.combo_timer_ms = 0
        self.passive_score_timer = 0
        self.reroll_charges = 1

    def run(self):
        while self.running:
            dt_ms = self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                    if self.game_over and event.key == pygame.K_r:
                        self.reset()

                    if self.leveling:
                        if event.key in (pygame.K_1, pygame.K_KP1):
                            self.choose_level_up(0)
                        elif event.key in (pygame.K_2, pygame.K_KP2):
                            self.choose_level_up(1)
                        elif event.key in (pygame.K_3, pygame.K_KP3):
                            self.choose_level_up(2)
                        elif event.key == pygame.K_r:
                            self.reroll_level_up()

            if not self.game_over and not self.leveling:
                dt_s = dt_ms / 1000.0
                self.elapsed_ms += dt_ms
                self.spawn_timer += dt_ms
                self.shoot_timer += dt_ms
                self.passive_score_timer += dt_ms
                self.update_combo_state(dt_ms)

                if self.horde_active_ms > 0:
                    self.horde_active_ms = max(0, self.horde_active_ms - dt_ms)
                else:
                    self.horde_timer += dt_ms
                    if self.horde_timer >= self.horde_cycle_ms():
                        self.horde_timer = 0
                        self.horde_active_ms = self.horde_duration_ms()
                        self.horde_count += 1
                        self.effects.append(
                            {
                                "type": "score",
                                "x": self.player.x,
                                "y": self.player.y - 70,
                                "text": f"第{self.horde_count}波 狂潮来袭！",
                                "life": 1200,
                                "max_life": 1200,
                            }
                        )

                while self.passive_score_timer >= PASSIVE_SCORE_MS:
                    self.passive_score_timer -= PASSIVE_SCORE_MS
                    self.add_survival_score()

                if self.player.nova_level > 0:
                    self.nova_timer += dt_ms

                spawn_interval = self.current_spawn_interval()
                while self.spawn_timer >= spawn_interval:
                    self.spawn_timer -= spawn_interval
                    self.spawn_enemy()
                    spawn_interval = self.current_spawn_interval()

                shoot_cd = self.current_shoot_cooldown()
                while self.shoot_timer >= shoot_cd:
                    self.shoot_timer -= shoot_cd
                    self.auto_shoot()
                    shoot_cd = self.current_shoot_cooldown()

                if self.player.nova_level > 0 and self.nova_timer >= self.player.nova_cooldown:
                    self.nova_timer -= self.player.nova_cooldown
                    self.trigger_nova()

                self.update_player(dt_ms)
                self.update_enemies(dt_s)
                self.update_bullets(dt_s)
                self.update_melee(dt_ms)
                self.handle_collisions()
                self.update_orbs(dt_s)

            self.update_effects(dt_ms)
            self.draw()

        pygame.quit()


def main():
    Game().run()


if __name__ == "__main__":
    main()
