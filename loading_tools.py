import os.path
import pygame as pg

class Loader:
    def __init__(self, main_dir):
        self.data_dir = os.path.join(main_dir, 'data')

    def load_image(self, name, colorkey=None, scale=1):
        """
        Load a single image and return it and a corresponding pygame rect. The image file must be located in a data
        directory
        :param name: The name of the file
        :param colorkey: An rgb colorkey to set as transparent background
        :param scale: The scale of the image
        :return:
        """
        fullname = os.path.join(self.data_dir, name)
        image = pg.image.load(fullname)

        size = image.get_size()
        size = (size[0] * scale, size[1] * scale)
        image = pg.transform.scale(image, size)

        image = image.convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image, image.get_rect()

    def load_images(self, names, colorkeys=None, scale=1):
        fullnames = [os.path.join(self.data_dir, name) for name in names]
        images = [pg.image.load(fullname) for fullname in fullnames]

        sizes = [image.get_size() for image in images]
        sizes = [(size[0] * scale, size[1] * scale) for size in sizes]
        images = [pg.transform.scale(image, size) for image, size in zip(images, sizes)]

        images = [image.convert() for image in images]
        if colorkeys is not None:
            for image, colorkey in zip(images, colorkeys):
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, pg.RLEACCEL)
        return images, images[0].get_rect()


    def load_sound(self, name):
        class NoneSound:
            def play(self):
                pass

        if not pg.mixer or not pg.mixer.get_init():
            return NoneSound()

        fullname = os.path.join(self.data_dir, name)
        sound = pg.mixer.Sound(fullname)

        return sound

    def load_font(self, name=None, size=20):
        fullname = os.path.join(self.data_dir, name)
        font = pg.font.Font(fullname, size)
        return font
