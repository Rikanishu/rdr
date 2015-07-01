# encoding: utf-8

from rdr.application import app
import imghdr
import os
from uuid import uuid4
from PIL import Image, ImageOps

from rdr.modules.files.models import Image as ImageModel


def save_image(image, directory, filename, extension):
    """
    Save PIL image object and return new ImageModel

    @rtype: rdr.modules.files.models.Image
    """
    root_path = app.config.get("ROOT_PATH")
    image_dir = os.path.join(root_path, 'public', 'media', directory, filename[0], filename[1])
    if not os.path.isdir(image_dir):
        os.makedirs(image_dir, 0774)
    image_path = os.path.join(image_dir, '%s.%s' % (filename, extension))
    image.save(image_path)
    path = '%s/%s/%s' % (directory, filename[0], filename[1])
    return ImageModel(name=filename, extension=extension, path=path)


class UnknownImageFormatException(Exception):
    pass


class InitializeImageException(Exception):
    pass


class ImageStorage(object):

    def __init__(self, fp, directory='storage', name=None):
        if isinstance(fp, ImageStorage):
            obj = fp
            self.fp = obj.fp
            self.directory = obj.directory
            self.image_type = obj.image_type
            self.name = obj.name
            self.image = obj.image.copy()
        else:
            self.fp = fp
            self.directory = directory
            self.image_type = imghdr.what(self.fp)
            if not self.image_type:
                raise UnknownImageFormatException('Unknown image')
            if self.image_type == 'jpeg':
                self.image_type = 'jpg'
            self.name = str(uuid4()) if name is None else name
            self._img = None


    @property
    def image(self):
        if self._img is None:
            self._img = Image.open(self.fp)
            if self._img is None:
                raise InitializeImageException("Error while image initialize")
        return self._img

    @image.setter
    def image(self, img):
        if img is None:
            raise InitializeImageException("Image cannot be a None instance")
        self._img = img

    def in_format(self, formats):
        if type(formats) != list:
            formats = [formats]
        return self.image_type in formats

    def copy(self):
        return ImageStorage(self)

    def crop(self, w, h):
        img = self.image
        rw, rh = img.size
        if rw < w or rh < h:
            self.paste(w, h)
        else:
            left = (rw - w) / 2
            top = (rh - h) / 2
            right = (rw + w) / 2
            bottom = (rh + h) / 2
            self.image = img.crop((left, top, right, bottom))
        return self

    def fit(self, w, h):
        img = self.image
        rw, rh = img.size
        if rw < w or rh < h:
            self.paste(w, h)
        else:
            self.image = ImageOps.fit(img, (w, h), Image.ANTIALIAS)
        return self

    def paste(self, w, h, bgcolor=(255, 255, 255, 0)):
        img = self.image
        rw, rh = img.size
        offset_y = max((h / 2) - (rh / 2), 0)
        offset_x = max((w / 2) - (rw / 2), 0)
        background = Image.new(mode='RGBA', size=(w, h), color=bgcolor)
        background.paste(self.image, (offset_x, offset_y))
        self.image = background
        return self

    def save(self):
        """
        @rtype: rdr.modules.files.models.Image
        """
        return save_image(self.image, self.directory, self.name, self.image_type)

    def save_thumbnail(self, thumbnail_name, opts=None):
        """
        @rtype: rdr.modules.files.models.Image
        """
        if opts:
            thumbnail = self.image.thumbnail(opts, Image.ANTIALIAS)
        else:
            thumbnail = self.image
        return save_image(thumbnail, self.directory, self.name + '-' + thumbnail_name, self.image_type)

    def thumbnail(self, thumbnail_name, opts=None):
        """

        """
        return self.save_thumbnail(thumbnail_name, opts)





