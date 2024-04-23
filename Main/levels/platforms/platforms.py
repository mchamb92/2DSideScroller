import pygame
import csv

class TileMap:
    def __init__(self, csv_file, tile_size):
        """
        Initialize the TileMap with a CSV file path, tileset image path, and tile size.
        """
        self.tile_size = tile_size
        self.tilemap = self.load_csv(csv_file)
       # self.tileset = pygame.image.load(tileset_path).convert_alpha()

        print("Loaded tilemap with dimensions:", len(self.tilemap), "x", len(self.tilemap[0]))
   
    def load_csv(self, filepath):
        """
        Load and return the tilemap from a CSV file.
        """
        with open(filepath) as file:
            reader = csv.reader(file)
            return list(reader)

    def draw(self, display, camera_offset_x=0, camera_offset_y=0):
        """
        Draw the visible portion of the tilemap onto the specified display surface,
        offset by the camera position.
        """
       # print("Drawing tilemap...")
        for y, row in enumerate(self.tilemap):
            for x, tile in enumerate(row):
                if tile.isdigit():
                    tile = int(tile)
                    # Calculate the position of the tile in the tileset
                   # tile_x = (tile % (self.tileset.get_width() // self.tile_size)) * self.tile_size
                    #tile_y = (tile // (self.tileset.get_width() // self.tile_size)) * self.tile_size
                    # Calculate the position on the screen
                    screen_x = x * self.tile_size - camera_offset_x
                    screen_y = y * self.tile_size - camera_offset_y
                    # Blit the tile to the display
                   # display.blit(self.tileset, (screen_x, screen_y), (tile_x, tile_y, self.tile_size, self.tile_size))

        # Draw a red border around the entire tilemap for debugging
        border_color = (255, 0, 0)  # Red color
        visible_border_rect = pygame.Rect(
            camera_offset_x,  # left edge of the screen
            camera_offset_y,  # top edge of the screen
            self.tile_size * len(self.tilemap[0]),  # width of the entire tilemap
            self.tile_size * len(self.tilemap)      # height of the entire tilemap
        )
        pygame.draw.rect(display, border_color, visible_border_rect, 5)  # Border thickness of 1 pixel