import factory
from . import models
from faker import Factory as FakerFactory
import random
import string

faker = FakerFactory.create()


def random_letter():
    string.letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return random.choice(string.letters)


class DeviceTypeFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.DeviceType

    name = factory.Faker('name')
    code = random_letter()


class DeviceBrandFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.DeviceBrand

    name = factory.Faker('name')


class DeviceFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Device

    device_type = DeviceTypeFactory.create()
    device_brand = DeviceBrandFactory.create()
    asset = random.randint(0, 1)
    ownership = random.choice(['CT', 'TW'])
    serial_number = faker.sentence(nb_words=4)
    model = faker.sentence(nb_words=2)
    purchase_date = faker.date_time()
