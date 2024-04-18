import requests
import base64
from Cryptodome.Cipher import AES
from loguru import logger
import sys


logger.add(
    sys.stderr,
    colorize=True,
    format="<yellow>{time}</yellow> {level} <green>{message}</green>",
    filter="Infisical Client",
    level="INFO",
)


class InfisicalClient:
    base_url = "http://app.infisical.com"

    def __init__(self, infisical_token: str, environment: str = "dev"):
        self.token = infisical_token
        self.environment = environment

    def decrypt(self, ciphertext, iv, tag, secret):
        secret = bytes(secret, "utf-8")
        iv = base64.standard_b64decode(iv)
        tag = base64.standard_b64decode(tag)
        ciphertext = base64.standard_b64decode(ciphertext)

        cipher = AES.new(secret, AES.MODE_GCM, iv)
        cipher.update(tag)
        cleartext = cipher.decrypt(ciphertext).decode("utf-8")
        return cleartext

    def check_scopes(self, service_token_data: dict):
        if service_token_data.get("scopes"):
            for env in service_token_data.get("scopes"):
                if env["environment"] == self.environment:
                    service_token_data["environment"] = self.environment
                    logger.info(f"Token environment selected {self.environment}")
                    break
                else:
                    continue
        else:
            response = f"Invalid token for given environment: {self.environment}"
            logger.error(response)
            raise ValueError(response)
        return service_token_data

    def get_secrets(self) -> dict:
        "Return the dict with the secrets"
        service_token = self.token
        service_token_secret = service_token[service_token.rindex(".") + 1 :]

        # 1. Get your Infisical Token data
        service_token_data = requests.get(
            f"{self.base_url}/api/v2/service-token",
            headers={"Authorization": f"Bearer {service_token}"},
        ).json()
        service_token_data = self.check_scopes(service_token_data)
        # 2. Get secrets for your project and environment
        data = requests.get(
            f"{self.base_url}/api/v3/secrets",
            params={
                "environment": service_token_data["environment"],
                "workspaceId": service_token_data["workspace"],
            },
            headers={"Authorization": f"Bearer {service_token}"},
        ).json()

        encrypted_secrets = data["secrets"]

        # 3. Decrypt the (encrypted) project key with the key from your Infisical Token
        project_key = self.decrypt(
            ciphertext=service_token_data["encryptedKey"],
            iv=service_token_data["iv"],
            tag=service_token_data["tag"],
            secret=service_token_secret,
        )

        # 4. Decrypt the (encrypted) secrets
        secrets = {}
        for secret in encrypted_secrets:
            secret_key = self.decrypt(
                ciphertext=secret["secretKeyCiphertext"],
                iv=secret["secretKeyIV"],
                tag=secret["secretKeyTag"],
                secret=project_key,
            )

            secret_value = self.decrypt(
                ciphertext=secret["secretValueCiphertext"],
                iv=secret["secretValueIV"],
                tag=secret["secretValueTag"],
                secret=project_key,
            )

            secrets.update(
                {
                    secret_key: secret_value,
                }
            )
        return secrets
