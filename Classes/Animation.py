import pygame

frames_tree = {
    "main": {
        "frames": [["./Assets/Images/Ships/Starship1.png", 20],
                   ["./Assets/Images/Ships/Starship1_frame1.png", 20],
                   ["./Assets/Images/Ships/Starship1_frame2.png", 20],
                   ["./Assets/Images/Ships/Starship1_frame3.png", 20],
                   ["./Assets/Images/Ships/Starship1_frame2.png", 20],
                   ["./Assets/Images/Ships/Starship1_frame1.png", 20]],
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
        if self.master.mass > 100:
            print(self.master.speed_x)