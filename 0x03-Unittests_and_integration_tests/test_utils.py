#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))  # ajoute dossier courant en début de path

import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch , Mock 
from utils import get_json
from utils import memoize


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
    """Tests the get_json function.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Tests that get_json returns the expected result.
        """
        # Configure the mock to return a Mock object with a json method
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function
        result = get_json(test_url)

        # Test that the mocked get method was called exactly once with test_url
        mock_get.assert_called_once_with(test_url)

        # Test that the output of get_json is equal to test_payload
        self.assertEqual(result, test_payload)






class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()

            # Appel de a_property deux fois
            result1 = obj.a_property
            result2 = obj.a_property

            # Vérifie que le résultat est correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Vérifie que a_method n’a été appelé qu’une seule fois
            mock_method.assert_called_once()

