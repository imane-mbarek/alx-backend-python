#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
      @parameterized.expand([
        ("google",),
        ("abc",)
      ])
      @patch('client.GithubOrgClient.get_json')
      def test_org(self, org_name, mock_get_json):

          # Préparer une fausse réponse de get_json
          expected_result = {"login": org_name}
          mock_get_json.return_value = expected_result

          # Initialiser le client et appeler .org
          client = GithubOrgClient(org_name)
          result = client.org

          # Vérifier que get_json a été appelée une fois avec l’URL correcte
          mock_get_json.assert_called_once_with(
          f"https://api.github.com/orgs/{org_name}")

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
        """Test GithubOrgClient.public_repos returns expected repo list"""
          test_payload = [
              {"name": "repo1"},
              {"name": "repo2"},
          ]
          mock_get_json.return_value = test_payload

          with patch(
                'client.GithubOrgClient._public_repos_url',
                new_callable=PropertyMock,
                return_value="https://api.github.com/orgs/testorg/repos"
          ) as mock_url:
              client = GithubOrgClient("testorg")
              repos = client.public_repos()
              self.assertEqual(repos, ["repo1", "repo2"])

              mock_get_json.assert_called_once()
              mock_url.assert_called_once()
