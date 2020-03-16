import pygame
import math


class Simulation:

    def __init__(self):
        self.s_width = 1280
        self.s_height = 720

        self.color_rod = (0, 0, 255)
        self.color_bob = (255, 0, 0)
        self.rod_width = 5

        self.m1 = 4
        self.m2 = 4
        self.r1 = 300
        self.r2 = 125
        self.g = 9.8
        self.friction = 0.99
        self.time_step = 0.15

        """ Initial conditions """
        self.theta1 = math.pi / 2
        self.theta2 = math.pi / 2
        self.v1 = 0
        self.v2 = 0

        self.x0 = self.s_width // 2
        self.y0 = 0


    def run(self):
        pygame.init()      # Prepare the pygame module for use

        # Create surface of (width, height), and its window.
        main_surface = pygame.display.set_mode((self.s_width, self.s_height))

        clock = pygame.time.Clock()

        while True:
            ev = pygame.event.poll()    # Look for any event
            if ev.type == pygame.QUIT:  # Window close button clicked?
                break                   #   ... leave game loop

            dt = clock.tick(60)    # Limit frame rate to 60 FPS

            self.construct_frame(main_surface, dt)
            pygame.display.flip()

        pygame.quit()
    
    def construct_frame(self, surface, dt):
        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        surface.fill((0, 200, 255))
        
        # Calculate angular acceleration
        num1 = -self.g * (2 * self.m1 + self.m2) * math.sin(self.theta1)
        num2 = -self.m2 * self.g * math.sin(self.theta1 - 2 * self.theta2)
        num3 = -2 * math.sin(self.theta1 - self.theta2) * self.m2
        num4 = self.v2**2 * self.r2 + self.v1**2 * self.r1 * math.cos(self.theta1 - self.theta2)
        den = self.r1 * (2 * self.m1 + self.m2 - self.m2 * math.cos(2 * self.theta1 - 2 * self.theta2))
        acc1 = (num1 + num2 + num3 * num4) / den

        num1 = 2 * math.sin(self.theta1 - self.theta2);
        num2 = self.v1**2 * self.r1 * (self.m1 + self.m2);
        num3 = self.g * (self.m1 + self.m2) * math.cos(self.theta1);
        num4 = self.v2**2 * self.r2 * self.m2 * math.cos(self.theta1 - self.theta2);
        den = self.r2 * (2 * self.m1 + self.m2 - self.m2 * math.cos(2 * self.theta1 - 2 * self.theta2));
        acc2 = (num1 * (num2 + num3 + num4)) / den

        # Implement time component
        acc1 *= self.time_step
        acc2 *= self.time_step

        # Add accelerations to velocities
        self.v1 += acc1
        self.v2 += acc2
        self.v1 *= self.friction
        self.v2 *= self.friction

        # Add velocities to angles
        self.theta1 += self.v1
        self.theta2 += self.v2

        # Draw the sucker
        self.x1 = self.x0 + self.r1 * math.sin(self.theta1)
        self.y1 = self.y0 + self.r1 * math.cos(self.theta1)

        self.x2 = self.x1 + self.r2 * math.sin(self.theta2)
        self.y2 = self.y1 + self.r2 * math.cos(self.theta2)

        p0 = (int(self.x0), int(self.y0))
        p1 = (int(self.x1), int(self.y1))
        p2 = (int(self.x2), int(self.y2))

        r1 = math.sqrt(self.m1 / math.pi)
        r2 = math.sqrt(self.m2 / math.pi)

        pygame.draw.line(surface, self.color_rod, p0, p1, self.rod_width)
        pygame.draw.line(surface, self.color_rod, p1, p2, self.rod_width)
        pygame.draw.circle(surface, self.color_bob, p1, int(r1 * 20));
        pygame.draw.circle(surface, self.color_bob, p2, int(r2 * 20));



if __name__ == '__main__':
    sim = Simulation()
    sim.run()

