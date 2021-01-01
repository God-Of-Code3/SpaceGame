import pygame
import random
from Functions.Math import *

frames_tree = {
    "main": {
        "frames": [["./Assets/Images/Ships/Starship1_frame1.png", 20],
                   ["./Assets/Images/Ships/Starship1_frame2.png", 20],
                   ["./Assets/Images/Ships/Starship1_frame3.png", 20],
                   ["./Assets/Images/Ships/Starship1_frame2.png", 20],
                   ["./Assets/Images/Ships/Starship1_frame1.png", 20]],
        "next": "main"
    }
}
frames_tree2 = {
    "main": {
        "frames": [["./Assets/Images/Ships/Spaceship2.png", 20]],
        "next": "main"
    }
}

all_sprites = pygame.sprite.Group()


class Anim(pygame.sprite.Sprite):
    def __init__(self, group, cam, frames, master, width, height):
        super().__init__(group)
        self.cam = cam
        self.frames = self.upload_frames(frames)
        self.master = master
        self.width, self.height = width, height
        self.state = "main"
        self.frame = 0
        self.timer = 0
        self.step = 10
        self.image = self.get_current_image()
        self.rect = self.image.get_rect()

    def load_image(self, img):
        return pygame.image.load(img).convert_alpha()

    def upload_frames(self, frames):
        frames_images = dict()
        for st in frames:
            state = frames[st]
            current_state = dict()
            current_state["next"] = state["next"]
            current_state["frames"] = list()
            for frame in state["frames"]:
                current_state["frames"].append([self.load_image(frame[0]), frame[1]])
            frames_images[st] = current_state

        return frames_images

    def get_current_image(self):
        return self.frames[self.state]["frames"][self.frame][0]

    def get_current_time(self):
        return self.frames[self.state]["frames"][self.frame][1]

    def check_next(self):
        return self.frame >= len(self.frames[self.state]["frames"])

    def set_next_state(self):
        next_state = self.frames[self.state]["next"]
        self.timer = 0
        self.frame = 0
        self.state = next_state

    def set_current_image(self):
        self.image = self.get_current_image()
        self.timer = 0

    def update(self):
        if self.timer >= self.get_current_time():
            self.frame += 1
            if self.check_next():
                self.set_next_state()
            self.set_current_image()
        else:
            self.timer += self.step
        w, h = self.width * self.cam.zoom_value, self.height * self.cam.zoom_value
        self.image = pygame.transform.scale(self.image, (int(w), int(h)))
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.cam.size[0] / 2 + (self.master.x - self.cam.cam_pos[0]) * self.cam.zoom_value),
                            int(self.cam.size[1] / 2 + (self.master.y - self.cam.cam_pos[1]) * self.cam.zoom_value))


EXPL_CENTER_COLOR = (242, 250, 255)
EXPL_SECOND_COLOR = (255, 236, 0)
EXPL_THIRD_COLOR = (255, 170, 0)


class Explosion:
    def __init__(self, x, y, size, cam):
        self.step = 3
        self.size = size
        self.max_size = size
        self.expansion = 1
        self.particles = []
        self.circles = []
        self.x, self.y = x, y
        self.cam = cam
        for _ in range(200):
            self.add_particle()

    def add_circle(self):
        if self.size > 10:
            direction = random.randint(0, 360)
            dist = self.size + random.randint(-int(self.size * 0.1), int(self.size * 0.2))
            x = self.x + math.cos(direction * math.pi / 180) * dist
            y = self.y + math.sin(direction * math.pi / 180) * dist
            self.circles.append({"x": x, "y": y, "size": 1,
                                 "max_size": max(random.randint(int(self.size * 0.4), int(self.size * 0.6)), 1),
                                 "step": self.step, "expansion": 1})

    def add_particle(self):
        if self.size > 10:
            direction = random.randint(0, 360)
            speed = self.step * 2 * random.randint(0, 20) / 10
            speed_x = math.cos(direction * math.pi / 180) * speed
            speed_y = math.sin(direction * math.pi / 180) * speed
            self.particles.append({"x": self.x, "y": self.y, "speed": (speed_x, speed_y),
                                   "age": random.randint(10, 100)})

    def update(self, objects):
        self.size += self.step * self.expansion
        if self.size > self.max_size:
            self.expansion = -1
        if self.size < 1:
            self.size = 1
        if random.randint(0, 1000) < 500:
            self.add_circle()

        if random.randint(0, 1000) < 100 and self.size > 1:
            self.add_particle()

        for i in range(len(self.circles)):
            self.circles[i]["size"] += self.circles[i]["step"] * self.circles[i]["expansion"]
            if self.circles[i]["size"] > self.circles[i]["max_size"]:
                self.circles[i]["expansion"] = -1
            if self.circles[i]["size"] < 1:
                self.circles[i]["size"] = 1

        for i in range(len(self.particles)):
            self.particles[i]["x"] += self.particles[i]["speed"][0]
            self.particles[i]["y"] += self.particles[i]["speed"][1]
            self.particles[i]["age"] -= 1

        for obj in objects:
            if self.size * 5 - self.step * 5 < math.hypot(obj.x - self.x, obj.y - self.y) < self.size * 5 and \
                    self.expansion > 0:
                d = to_point(self.x, self.y, obj.x, obj.y)
                kick = self.size / self.max_size * 20
                """obj.speed_x += math.cos(math.pi / 180 * d) * kick
                obj.speed_y += math.sin(math.pi / 180 * d) * kick"""

        self.circles = list(filter(lambda x: x["size"] > 1, self.circles))
        self.particles = list(filter(lambda x: x["age"] > 0, self.particles))

    def draw(self, screen):
        r_circle = max(1, int(self.size * 5 * self.cam.zoom_value))
        f_circle = max(1, int(self.size * 0.5 * self.cam.zoom_value))
        s_circle = max(2, int(self.size * 0.6 * self.cam.zoom_value))
        t_circle = max(3, int(self.size * self.cam.zoom_value))
        circle_pos = (int(self.cam.size[0] / 2 + (self.x - self.cam.cam_pos[0]) * self.cam.zoom_value),
                      int(self.cam.size[1] / 2 + (self.y - self.cam.cam_pos[1]) * self.cam.zoom_value))

        def interpolate_color(c1, c2, w1, w2):
            interpolated_color = [0, 0, 0]
            for i in range(3):
                interpolated_color[i] = int((w1 / w2) * c2[i] +
                                            max((w2 - w1) / w2, 0) * c1[i])
                interpolated_color[i] = max(0, min(255, interpolated_color[i]))
            return interpolated_color

        if self.expansion > 0:
            col = interpolate_color(EXPL_CENTER_COLOR, EXPL_SECOND_COLOR, self.size, self.max_size)
        else:
            col = interpolate_color(EXPL_THIRD_COLOR, EXPL_CENTER_COLOR, self.size, self.max_size)

        pygame.draw.circle(screen, col, circle_pos, t_circle)
        """pygame.draw.circle(screen, EXPL_THIRD_COLOR, circle_pos, t_circle)
        pygame.draw.circle(screen, EXPL_SECOND_COLOR, circle_pos, s_circle)
        pygame.draw.circle(screen, EXPL_CENTER_COLOR, circle_pos, f_circle)"""

        if self.expansion > 0:
            pygame.draw.circle(screen, EXPL_CENTER_COLOR, circle_pos, r_circle, 2)

        for particle in self.particles:
            x, y = particle["x"], particle["y"]
            n = 5
            xl, yl = particle["x"] - particle["speed"][0] * n, particle["y"] - particle["speed"][1] * n
            circle_pos = (int(self.cam.size[0] / 2 + (xl - self.cam.cam_pos[0]) * self.cam.zoom_value),
                          int(self.cam.size[1] / 2 + (yl - self.cam.cam_pos[1]) * self.cam.zoom_value))
            circle_pos2 = (int(self.cam.size[0] / 2 + (x - self.cam.cam_pos[0]) * self.cam.zoom_value),
                           int(self.cam.size[1] / 2 + (y - self.cam.cam_pos[1]) * self.cam.zoom_value))
            circle = max(1, int(2 * self.cam.zoom_value))
            pygame.draw.line(screen, (255, 255, 255), circle_pos, circle_pos2, circle)

        for circle in self.circles:
            size = circle["size"]
            x, y = circle["x"], circle["y"]
            if size > 1:
                s_circle = max(2, int(size * 0.6 * self.cam.zoom_value))
                t_circle = max(3, int(size * self.cam.zoom_value))
                circle_pos = (int(self.cam.size[0] / 2 + (x - self.cam.cam_pos[0]) * self.cam.zoom_value),
                              int(self.cam.size[1] / 2 + (y - self.cam.cam_pos[1]) * self.cam.zoom_value))

                if circle["expansion"] > 0:
                    col = interpolate_color(EXPL_CENTER_COLOR, EXPL_SECOND_COLOR, circle["size"], circle["max_size"])
                else:
                    col = interpolate_color(EXPL_THIRD_COLOR, EXPL_SECOND_COLOR, circle["size"], circle["max_size"])

                """pygame.draw.circle(screen, (255, 0, 0), circle_pos, t_circle + int(2 * self.cam.zoom_value))
                pygame.draw.circle(screen, col, circle_pos, t_circle)"""
                pygame.draw.circle(screen, EXPL_THIRD_COLOR, circle_pos, t_circle)
                pygame.draw.circle(screen, EXPL_SECOND_COLOR, circle_pos, s_circle)
                #pygame.draw.circle(screen, EXPL_CENTER_COLOR, circle_pos, f_circle)

