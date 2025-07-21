#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch , Mock 
from utils import get_json



class TestAccessNestedMap(unittest.TestCase):

      @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
      ])
      def test_access_nested_map(self,nested_map,path, expected):
        self.assertEqual(access_nested_map(nested_map,path),expected)



      @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
      ])
      def test_access_nested_map_exception(self,nested_map,path):
        with self.assertRaises(KeyError) as context:
           access_nested_map(nested_map,path)



      # Vérifie que le message de l'erreur est correct
        self.assertEqual(str(context.exception), f"'{path[-1]}'")
 

  
class TestGetJson(unittest.TestCase):
     def test_get_json(self,mock_get):
         test_cases=[("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
         ]

         for test_url ,test_payload in test_cases:
             # Création d'un faux objet response
             mock_response=Mock()
             mock_response.json.return_value=test_payload

              # On dit que requests.get(url) retournera ce mock
             mock_get.return_value=mock_response

             # Appel réel à notre fonction
             result = get_json(test_url)


             # Vérifie que la réponse est bien celle attendue
             self.assertEqual(result , test_payload)

             # Reset du mock pour le prochain test
             mock_get.reset_mock()

