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

          # Vérifier que get_json a été appelée une fois avec l’URL correcte
          mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

          # Vérifier que le retour est correct
          self.assertEqual(result, expected_result)




     def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL from org"""
         with patch.object(GithubOrgClient, 'org', new_callable=Mock) as mock_org:
              expected_url = "https://api.github.com/orgs/google/repos"
              mock_org.return_value = {"repos_url": expected_url}

            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, expected_url)




      @patch('client.get_json')
      def test_public_repos(self, mock_get_json):
         # 👇 Simuler les données JSON retournées par get_json
         payload = [
            {'name': 'repo1'},
            {'name': 'repo2'}
         ]
         mock_get_json.return_value = payload

         # 👇 Simuler _public_repos_url avec un context manager
         with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
              mock_url.return_value = "https://api.github.com/orgs/google/repos"
              client = GithubOrgClient("google")
              result = client.public_repos()

            # ✅ Vérifie que le résultat est une liste des noms de repo
            self.assertEqual(result, ['repo1', 'repo2'])

            # ✅ Vérifi que les deux mocks ont bien été appelés
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/google/repos")
