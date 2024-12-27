# common/cards/animated_background.py
import random
import pygame

class Particle:
    def __init__(
        self,
        x: float,
        y: float,
        radius: int,
        color: pygame.Color,
        speed: float,
        lifespan: float,
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.lifespan = lifespan
        self.age = 0.0

    def update(self, delta):
        self.y += self.speed * delta
        self.age += delta

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class ParticleSystem:
    def __init__(self, x: float, y: float, colours: list[pygame.Color]):
        self.x = x
        self.y = y
        self.particles: list[Particle] = []
        self.spawn_rate = 20
        self.time_since_last_spawn = 0.0
        self.colours = colours

    def update(self, delta: float):
        self.time_since_last_spawn += delta
        if self.time_since_last_spawn >= 1.0 / self.spawn_rate:
            self.time_since_last_spawn -= 1.0 / self.spawn_rate
            self.particles.append(self.create_particle())

        for particle in self.particles:
            particle.update(delta)
            if particle.age >= particle.lifespan:
                self.particles.remove(particle)

    def create_particle(self):
        radius = random.randint(2, 10)
        color = random.choice(self.colours)
        speed = random.uniform(50, 100)
        lifespan = 3
        return Particle(
            self.x + random.randint(0, 60),
            self.y - radius,
            radius,
            color,
            speed,
            lifespan,
        )

    def render(self, surface: pygame.Surface):
        for particle in self.particles:
            particle.draw(surface)

class AnimatedBackground:
    DARK = pygame.Color(91, 110, 225)
    LIGHT = pygame.Color(99, 155, 255)
    WHITE = pygame.Color(255, 255, 255)

    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
        self.surface = pygame.surface.Surface(size)
        self.particle_system = ParticleSystem(0, 0, [self.DARK, self.LIGHT, self.WHITE])

    def render(self, delta: float) -> None:
        self.surface.fill(self.WHITE)
        self.particle_system.update(delta)
        self.particle_system.render(self.surface)

    def get_surface(self) -> pygame.Surface:
        return self.surface