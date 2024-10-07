import paramiko
import sys

def try_passphrase(private_key_file, passphrase):
    """
    Try to decrypt the RSA private key with the given passphrase.
    """
    try:
        with open(private_key_file, 'r') as key_file:
            private_key = paramiko.RSAKey.from_private_key(key_file, password=passphrase)
            print(f"[+] Success! Passphrase found: {passphrase}")
            return True
    except paramiko.ssh_exception.PasswordRequiredException:
        print(f"[-] Passphrase required for {private_key_file}")
    except paramiko.ssh_exception.SSHException:
        print(f"[-] Incorrect passphrase: {passphrase}")
    return False

def brute_force_rsa_key(private_key_file, passphrase_list_file):
    """
    Try all passphrases from the passphrase list to decrypt the private key.
    """
    with open(passphrase_list_file, 'r') as file:
        passphrases = file.readlines()

    for passphrase in passphrases:
        passphrase = passphrase.strip()  # Remove any newline characters
        if try_passphrase(private_key_file, passphrase):
            break  # Stop if the correct passphrase is found

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <private_key_file> <passphrase_list_file>")
        sys.exit(1)

    private_key_file = sys.argv[1]
    passphrase_list_file = sys.argv[2]

    brute_force_rsa_key(private_key_file, passphrase_list_file)
