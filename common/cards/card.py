# common/cards/card.py
import pygame
import pytweening
import cv2
import numpy as np
from enum import Enum, auto

from .helpers import MovingAverage, Tweener, wrapf, clamp, scale_and_clamp #Import helpers

class Card:

    TIME_TO_SNAP_TO_CURSOR_ON_PICKUP = 0.2  # Seconds
    MAX_CARD_ROTATION = 50  # Degrees

    class CardState(Enum):
        IDLE = auto()
        GRABBED = auto()

    def __init__(
        self,
        position: pygame.Vector2,
        card_size: pygame.Vector2,
        background_surface: pygame.Surface,
    ) -> None:
        self.position = position
        self.card_size = card_size
        self.background_surface = pygame.transform.scale(background_surface, self.card_size) # Scale background to match card size

        self.state = self.CardState.IDLE
        self.card_goal_position: pygame.Vector2 = position
        self.card_pickup_position: pygame.Vector2 = pygame.Vector2(0, 0)
        self.tweener_snap_to_mouse = Tweener(
            1.0, 0.0, self.TIME_TO_SNAP_TO_CURSOR_ON_PICKUP, pytweening.easeInCubic
        )
        self.average_velocity_x = MovingAverage(size=10)
        self.average_velocity_y = MovingAverage(size=10)
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)

        self.points = np.array(
            [
                [-self.card_size.x / 2, self.card_size.y / 2, 0],
                [self.card_size.x / 2, self.card_size.y / 2, 0],
                [self.card_size.x / 2, -self.card_size.y / 2, 0],
                [-self.card_size.x / 2, -self.card_size.y / 2, 0],
            ]
        )
        self.card_rotation = pygame.Vector2(0, 0)

        self.surface = pygame.Surface(self.card_size)

    def render(self, screen: pygame.Surface, delta: float) -> None:
        self.update_position_and_velocity(delta)
        self.update_card_rotation(delta)

        self.surface.fill("purple")  # Fill with a color in case background doesn't cover everything
        self.surface.blit(self.background_surface, (0, 0))

        points = self.get_screen_coord_points()

        self.blit_perspective_transformed_card_surface(screen, points)
        self.blit_card_outline(screen, points)

    def update_position_and_velocity(self, delta: float) -> None:
        self.tweener_snap_to_mouse.update(delta)

        if self.tweener_snap_to_mouse.is_finished():
            new_position = self.card_goal_position
        else:
            new_position = self.card_goal_position - (
                (self.tweener_snap_to_mouse.get_value())
                * (self.card_goal_position - self.card_pickup_position)
            )

        self.average_velocity_x.add((new_position.x - self.position.x) / delta)
        self.average_velocity_y.add((new_position.y - self.position.y) / delta)
        x_velocity = self.average_velocity_x.average()
        y_velocity = self.average_velocity_y.average()

        VELOCITY_EPSILON = 1
        self.velocity = pygame.Vector2(
            x_velocity if abs(x_velocity) > VELOCITY_EPSILON else 0,
            y_velocity if abs(y_velocity) > VELOCITY_EPSILON else 0,
        )

        self.position = new_position

    def update_card_rotation(self, delta: float) -> None:
        card_rotation_vector = pygame.Vector2(
            -self.velocity.x / 15, self.velocity.y / 15
        )

        ROTATION_EPSILON = 4
        if card_rotation_vector.magnitude() < ROTATION_EPSILON:
            card_rotation_vector = pygame.Vector2(0, 0)
        elif card_rotation_vector.magnitude() > self.MAX_CARD_ROTATION:
            card_rotation_vector = card_rotation_vector / (
                card_rotation_vector.magnitude() / self.MAX_CARD_ROTATION
            )

        self.card_rotation_degrees_y = card_rotation_vector.x
        self.card_rotation_degrees_x = card_rotation_vector.y

    @staticmethod
    def get_bounding_box_dimensions(points: np.ndarray) -> tuple[int, int]:
        if points.size == 0:
            return 0, 0

        min_x = np.min(points[:, 0])
        max_x = np.max(points[:, 0])
        min_y = np.min(points[:, 1])
        max_y = np.max(points[:, 1])

        width = max_x - min_x
        height = max_y - min_y

        return int(width), int(height)

    def rotate_points(
        self, points: list[np.ndarray], degrees_x: float, degrees_y: float
    ) -> np.ndarray:
        degrees_x = np.radians(degrees_x)
        degrees_y = np.radians(degrees_y)

        Rx = np.array(
            [
                [1, 0, 0],
                [0, np.cos(degrees_x), -np.sin(degrees_x)],
                [0, np.sin(degrees_x), np.cos(degrees_x)],
            ]
        )

        Ry = np.array(
            [
                [np.cos(degrees_y), 0, np.sin(degrees_y)],
                [0, 1, 0],
                [-np.sin(degrees_y), 0, np.cos(degrees_y)],
            ]
        )

        rotated_points = []
        for point in points:
            rotated_point = np.dot(Rx, point)
            rotated_point = np.dot(Ry, rotated_point)
            rotated_points.append(rotated_point)

        return np.array(rotated_points)

    def perspective_projection(self, points: np.ndarray, d: float) -> np.ndarray:
        projected_points = []
        for point in points:
            x, y, z = point
            x_p = x * d / (z + d)
            y_p = y * d / (z + d)
            projected_points.append([x_p, y_p])

        return np.array(projected_points)

    def get_screen_coord_points(self) -> np.ndarray: # Updated to use self.card_size
        points = []
        rotated_points = self.rotate_points(
            self.points, self.card_rotation_degrees_x, self.card_rotation_degrees_y
        )
        projected_points = self.perspective_projection(rotated_points, 150)
        for point in projected_points:
            points.append([point[0], point[1]])
        return np.array(points)
    def calculate_perspective_transform(
        self, src: np.ndarray, dst: np.ndarray
    ) -> np.ndarray:
        src_copy = src[:, :2].copy()
        src_copy += np.array([self.card_size.x / 2, self.card_size.y / 2])

        dst_copy = dst.copy()
        min_values = dst_copy.min(axis=0)

        dst_copy -= min_values

        return cv2.getPerspectiveTransform(
            src_copy.astype(np.float32), dst_copy.astype(np.float32)
        )

    def blit_perspective_transformed_card_surface(
        self, surface: pygame.Surface, points: np.ndarray
    ) -> None:
        transform = self.calculate_perspective_transform(self.points, points)

        transformed_surface = self.apply_perspective_transform(
            self.surface,
            transform,
            self.get_bounding_box_dimensions(points),
        )

        top_left_point = np.array([0, 0])
        top_left = self.transform_point(top_left_point, transform)

        surface.blit(
            transformed_surface,
            self.position - top_left + points[3],
        )

    def blit_card_outline(self, surface: pygame.Surface, points: np.ndarray) -> None:
        modified_points = points.tolist()
        modified_points[0][1] -= 1
        modified_points[1][0] -= 1
        modified_points[1][1] -= 1
        modified_points[2][0] -= 1
        for i in range(len(modified_points)):
            a, b = (modified_points[i], modified_points[(i + 1) % len(modified_points)])

            pygame.draw.line(
                surface,
                pygame.Color(0, 0, 0, 100),
                a + self.position,
                b + self.position,
                1,
            )

    def apply_perspective_transform(
        self, surface: pygame.Surface, matrix: np.ndarray, dst_size: tuple[int, int]
    ) -> pygame.Surface:
        src_array = pygame.surfarray.array3d(surface)
        src_array = np.swapaxes(src_array, 0, 1)

        x = np.zeros((src_array.shape[0], src_array.shape[1], 4), dtype=np.uint8)
        x += 255
        x[:, :, :3] = src_array

        dst_array = cv2.warpPerspective(
            x,
            matrix.astype(float),
            dst_size,
            flags=cv2.INTER_NEAREST,
        )

        a = np.ascontiguousarray(dst_array)
        return pygame.image.frombuffer(a.tobytes(), a.shape[1::-1], "RGBA")

    def transform_point(self, point: np.ndarray, matrix: np.ndarray) -> np.ndarray:
        point = np.array([[point]], dtype=np.float32)
        transformed_point = cv2.perspectiveTransform(point, matrix)
        return transformed_point[0][0]

    def get_clickable_rect(self) -> pygame.Rect:
        return pygame.rect.Rect(
            self.position[0] - self.card_size.x / 2,
            self.position[1] - self.card_size.y / 2,
            self.card_size.x,
            self.card_size.y,
        )

    def process_events(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.get_clickable_rect().collidepoint(event.pos):
                if self.state == self.CardState.IDLE:
                    self.transition_to_grabbed(event)
                    return True

        if event.type == pygame.MOUSEMOTION:
            if self.state == self.CardState.GRABBED:
                self.card_goal_position = pygame.Vector2(event.pos)
                return True

        if event.type == pygame.MOUSEBUTTONUP:
            if self.state == self.CardState.GRABBED:
                self.transition_to_idle()
                return True

        return False

    def transition_to_grabbed(self, event: pygame.event.Event) -> None:
        self.card_pickup_position = self.position
        self.card_goal_position = pygame.Vector2(event.pos)
        self.state = self.CardState.GRABBED
        from common.managers.managers import audio_manager # Import here to avoid circular imports
        audio_manager.play_sound("card_sound_5")
        self.tweener_snap_to_mouse.start()

    def transition_to_idle(self) -> None:
        self.state = self.CardState.IDLE
        from common.managers.managers import audio_manager # Import here to avoid circular imports
        audio_manager.play_sound("card_sound_4")