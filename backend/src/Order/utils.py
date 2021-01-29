import random
import string


# function that generates a string randomly
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_generator(instance):
    print('in the function')
    order_id = random_string_generator()
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_id).exists()
    if qs_exists:
        unique_order_generator(instance)

    return order_id
