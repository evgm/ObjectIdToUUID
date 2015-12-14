import unittest
from uuid import UUID
from bson import ObjectId

from UUID_to_ObjectId import uuid_to_object_id
from ObjectId_to_UUID import object_id_to_uuid


class TestConversion(unittest.TestCase):

    _known_accordance = [
        ("f940bd03-55c3-11e3-a4b0-ce16e9596447", "52933322e4b0ce16e9596447"),
        ("509f9b83-4ab9-11e4-87a3-1447965aada8", "542e2bf3c7a31447965aada8"),
        ("2ecdb881-08be-11e4-b4ff-0b842d8af503", "53bf795574ff0b842d8af503"),
        ("aadf3303-4a9e-11e4-a4b0-fe6be46727c1", "542dff3ee4b0fe6be46727c1"),
        ("05c25b83-4a9a-11e4-a4b0-2ea09e306ed6", "542df773e4b02ea09e306ed6"),
        ("d53cea83-4ab6-11e4-a4b0-6e575e495bac", "542e27c9e4b06e575e495bac"),
        ("29f7ca83-023a-11e2-a4b0-c28df494ecb2", "50598c89e4b0c28df494ecb2")
    ]

    def testA(self):
        for pair in self._known_accordance:
            assert uuid_to_object_id(UUID(pair[0])) == ObjectId(pair[1])

    def testB(self):
        for pair in self._known_accordance:
            assert object_id_to_uuid(ObjectId(pair[1])) == UUID(pair[0])

if __name__ == "__main__":
    unittest.main()
