
"""
Class containing structured data containing symbol art information.
"""

__author__ = 'Alex Alkire'
__version__ = '0.1'
__license__ = 'MIT'

import cv2
import np

IMAGE_DISPLAY_SIZE = (512, 512)
COLOR_COMPENSATION = True

class SymbolArt:
    def __init__(self, buffer):
        print("B", buffer)
        self.layers = []
        self.name =""
        self.header = {
            'authorId': int.from_bytes(buffer[0:4], byteorder='little'),
            'layerCount': buffer[4],
            'height': buffer[5],
            'width': buffer[6],
            'sound': buffer[7]
        }
        for layer_index in range(0, self.header['layerCount']):
            value_a = int.from_bytes(buffer[16 + 16 * layer_index:20 + 16 * layer_index], byteorder='little')
            value_b = int.from_bytes(buffer[20 + 16 * layer_index:24 + 16 * layer_index], byteorder='little')
            layer = {
                'top_left': {
                    'x': buffer[8 + 16 * layer_index],
                    'y': buffer[9 + 16 * layer_index]
                },
                'bottom_left': {
                    'x': buffer[10 + 16 * layer_index],
                    'y': buffer[11 + 16 * layer_index]
                },
                'top_right': {
                    'x': buffer[12 + 16 * layer_index],
                    'y': buffer[13 + 16 * layer_index]
                },
                'bottom_right': {
                    'x': buffer[14 + 16 * layer_index],
                    'y': buffer[15 + 16 * layer_index]
                },
                'visible': (value_a >> 31) & 1 == 0,
                'textureIndex': (value_a >> 21) & 1023,
                'transparency': ((value_a >> 18) & 7) / 7,
                'colorR': int(((value_a >> 0) & 63) *4),
                'colorG': int(((value_a >> 6) & 63) *4),
                'colorB': int(((value_a >> 12) & 63) *4),
                # Probably unused..
                'colorX': int(((value_b >> 0) & 63)),
                'colorY': int(((value_b >> 6) & 63)),
                'colorZ': int(((value_b >> 12) & 63)),
            }
            self.layers.append(layer)
        if len(buffer)> 24+self.header['layerCount']*16:
            self.name = buffer[24+self.header['layerCount']*16:]
        pass

    """
    Retrieve this symbol art as a cv2 image array.
    """
    def get_as_image(self):
        base_img = cv2.imread('images/bg.png')
        base_img = cv2.resize(base_img, IMAGE_DISPLAY_SIZE)
        img_list = []
        for layer in self.layers:
            new_img = cv2.imread("images/" + str(layer['textureIndex'] + 1) + ".png", -1)
            color_mask = np.zeros((new_img.shape[0], new_img.shape[1], 4), np.float32)

            # Normalize RGB to be 0.0 - 1.0 values.
            r, g, b = layer['colorR'] / 255.0, layer['colorG'] / 255.0, layer['colorB'] / 255.0

            # Adjust colors to simulate PSO2 RGB values.  Without this colors will look darker ingame.
            if COLOR_COMPENSATION == True:
                color = tuple(reversed((
                    1,
                    (np.clip(r * 0.76 + 0.265 * r, 0, 1)),
                    (np.clip((g * 0.76 + 0.265) * g, 0, 1)),
                    (np.clip((b * 0.76 + 0.265) * b, 0, 1))
                )))

            else:
                color = tuple(reversed((1,r,g,b)))
            color_mask[:] = color
            new_img = np.multiply(new_img, color_mask)
            h, w, c = new_img.shape
            pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
            pts2 = np.float32([
                [layer['top_left']['x'] * 2, layer['top_left']['y'] * 2],
                [layer['top_right']['x'] * 2, layer['top_right']['y'] * 2],
                [layer['bottom_left']['x'] * 2, layer['bottom_left']['y'] * 2],
                [layer['bottom_right']['x'] * 2, layer['bottom_right']['y'] * 2]
            ])
            M = cv2.getPerspectiveTransform(pts1, pts2)
            new_img = cv2.warpPerspective(new_img, M, IMAGE_DISPLAY_SIZE)
            img_list.insert(0, new_img)
        for img in img_list:
            y1, y2 = 0, img.shape[0]
            x1, x2 = 0, img.shape[1]
            image_alpha = img[:, :, 3] / 255.0
            alpha_inverted = 1.0 - image_alpha
            for channel in range(0, 3):
                base_img[y1:y2, x1:x2, channel] = (image_alpha * img[:, :, channel] +
                                                   alpha_inverted * base_img[y1:y2, x1:x2, channel])
        return base_img
