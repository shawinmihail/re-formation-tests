import pygame
import pygame_utils


class Copter:
    def __init__(self, id, x0, v0, mass, radius):
        """
        :param x0: numpy array
        :param v0: numpy array
        """
        self.id = id
        self.x = x0
        self.x_list = list()
        self.x_list.append(x0)
        self.v = v0
        self.mass = mass
        self.radius = radius

    def move(self, accel, dt):
        self.x = self.x + self.v * dt + accel * dt * dt / float(2)
        self.v = self.v + accel * dt

        self.x_list.append(self.x)


class CopterPainter:
    def __init__(self, copter, color, display, display_config, trj_visible=False):
        self.copter = copter
        self.color = color
        self.display = display
        self.font = pygame.font.Font('freesansbold.ttf', self.copter.radius)

        self.display_config = display_config
        self.trj_visible = trj_visible

    def get_text_objects(self, text):
        textSurface = self.font.render(text, True, (255, 255, 255))
        return textSurface, textSurface.get_rect()

    def draw(self):

        if self.trj_visible:
            # drawing line from prev pos to current

            n = len(self.copter.x_list)
            points = []
            for i in range(n):
                points.append(self.get_x_screen(self.copter.x_list[i]))

            pygame.draw.lines(self.display, self.color, False, points, 2)

        # drawing body
        pygame.draw.circle(self.display, self.color, self.get_x_screen(self.copter.x), self.copter.radius)

        TextSurf, TextRect = self.get_text_objects(str(self.copter.id))
        TextRect.center = self.get_x_screen(self.copter.x)
        self.display.blit(TextSurf, TextRect)


    def get_x_screen(self, x):
        return pygame_utils.transform_to_screen_system(x[0], x[1], self.display_config)




