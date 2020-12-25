import logging

logger = logging.getLogger(__name__)


def transform_subject(subject, loop_size):
    value = 1

    for i in range(loop_size):
        value *= subject
        value = value % 20201227

    return value


def reverse_loop_size(subject, result):
    loop_size = 2
    value = subject

    while True:
        value *= subject
        value = value % 20201227

        if value == result:
            return loop_size

        loop_size += 1


def obtain_encryption_key(card_pk, door_pk):
    card_loop_size = reverse_loop_size(subject=7, result=card_pk)
    door_loop_size = reverse_loop_size(subject=7, result=door_pk)

    encryption_a = transform_subject(subject=door_pk, loop_size=card_loop_size)
    encryption_b = transform_subject(subject=card_pk, loop_size=door_loop_size)

    assert encryption_a == encryption_b

    return encryption_a
# def get_loop_size(key):
#     i = 1
#     subject = 1
#     value = 1
#     initial_value = 1
#
#     while True:
#         value = initial_value
#         while True:
#             value *= subject
#             value = value % 20201227
#
#             if value == key:
#                 return
#
#         i += 1
