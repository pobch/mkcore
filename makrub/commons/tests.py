from django.test import TestCase

# Create your tests here.
from .models import Room

# class RoomModelTest(TestCase):

#     def setUp(self):
#         Room.objects.create(name='test room',
#                             description='test descrip',
#                             user_id=6,
#                             account_id=9,
#                             documents='test doc')

#     def test_row_content(self):
#         room = Room.objects.get(id=1)
#         expected_content = (f'{room.name}', f'{room.description}', room.user_id, room.account_id, f'{room.documents}')
#         self.assertEqual(expected_content, ('test room', 'test descrip', 6, 9, 'test doc'))
