# SSH Keys

Access to ilifu is controlled through SSH public-private key pairs.

If you are a new user, you have likely just generated an SSH key pair, and sent your public key to our system through the webform.

## Managing your SSH public key

You are able to manage the SSH public keys associated with your ilifu account by using the [SSH key managment](https://usage.ilifu.ac.za/ssh_keys) service. Use this service if you would like to update your existing SSH key, or add to your current key(s). Note that you may have multiple keys corresponding to different devices, e.g., laptop, office desktop, or home desktop.

## Generating a new SSH key pair

In the event that you lose your SSH key pair, you can generate a new key pair by following these [instructions](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/). If you have lost your SSH key pair you will receive an error `Permission denied (publickey)` when trying to access the ilifu system via SSH. In this event, please generate a new SSH key pair and update the SSH public key associated with your ilifu profile using the [SSH key managment](https://usage.ilifu.ac.za/ssh_keys) service.

## SSH key issues and debugging

If you're hitting a `permission denied (publickey)` error it means that their is a mismatch between the SSH keys known to your ssh-agent on your local workstation and the keys associated with your ilifu account.

### Non-default SSH key name and path

If you generated the SSH key pair using non-default name and path (i.e. it is not at ~/.ssh/id_rsa or ~/.ssh/id_ed25519), you will need to specify the path to the correct SSH key when running the `ssh` command:

```bash
ssh -i /path/to/ssh/key <username>@slurm.ilifu.ac.za
```
The path should point to the private key file, i.e. the file that doesn't have the .pub suffix, example: `ssh -i ~/.ssh/ilifu_key jeremy@slurm.ilifu.ac.za`.

### Your ssh-agent doesn't know about your SSH key

It is possible the ssh-agent running on your local workstation does not know about the correct SSH keys. Check if the workstation ssh-agent knows about the existing keys by running:

```bash
ssh-add -L
```
This should list the public SSH keys that that ssh-agent knows about. The keys (at least one) should match the key associated with your ilifu account (i.e. the original SSH key provided in the access request form or a key added to your ilifu account since then). If there is nothing listed, you can use the above solution and specify the correct path to the SSH key with the `-i` parameter. 

If it indicates no ssh-agent is running, you can start the ssh-agent by running:
```bash
eval "$(ssh-agent -s)"
```

You can also add a key to the ssh-agent by running:
```bash
ssh-add /path/to/ssh/key
```

The path should point to the private key, i.e. the file that doesn't have the .pub suffix, example: `ssh-add ~/.ssh/id_rsa`.

If none of these solutions resolve the issue, we'd recommend generating a new SSH key pair, using the default naming convention, and add the new SSH public key to your ilifu profile using the [SSH key managment](https://usage.ilifu.ac.za/ssh_keys) tool.

### SSH key passphrase

If you are asked for a passphrase when sshing to ilifu services, this passphrase is a password you would have set when generating the SSH keys, and is not associated with your ilifu account password. If you do not remember the passphrase, you will need to generate a new SSH key pair and add the new SSH public key to your ilifu profile using the [SSH key managment](https://usage.ilifu.ac.za/ssh_keys) tool.