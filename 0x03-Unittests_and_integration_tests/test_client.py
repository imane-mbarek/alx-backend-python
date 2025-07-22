#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from unittest.mock import patch , Mock
from client import GithubOrgClient






class TestGithubOrgClient(unittest.TestCase):
      @parameterized.expand([
        ("google",),
        ("abc",)
    ])
      @patch('client.GithubOrgClient.get_json')
      def test_org(self, org_name, mock_get_json):

          # Préparer une fausse réponse de get_json
          expected_result={"login":org_name}
          mock_get_json.return_value = expected_result

          # Initialiser le client et appeler .org
          client = GithubOrgClient(org_name)
          result=client.org

          # Vérifier que le retour est correct
          self.assertEqual(result, expected_result)

          # Vérifier que get_json a été appelée une fois avec l’URL correcte
          mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
