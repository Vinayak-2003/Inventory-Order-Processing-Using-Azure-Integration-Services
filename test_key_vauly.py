from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()

secret_client = SecretClient(vault_url="https://usecase-01.vault.azure.net/", credential=credential)

set_secret = secret_client.set_secret("secret-name", "secret-value")

print(set_secret.name)
print(set_secret.value)
print(set_secret.properties.version)

rec_secret = secret_client.get_secret("secret-name")

print(rec_secret.name)
print(rec_secret.value)