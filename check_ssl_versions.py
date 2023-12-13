import ssl

print("Supported SSL/TLS versions:")
for version in ssl.OPENSSL_VERSION.split():
    if version.startswith("OpenSSL"):
        print(version)
        break

supported_versions = ssl.OPENSSL_VERSION_INFO
print("Major version:", supported_versions[0])
print("Minor version:", supported_versions[1])
