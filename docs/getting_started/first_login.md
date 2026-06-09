# Welcome to your new account!

To ensure the security of your data and access to ilifu, you need to complete a few essential security steps during your first login. This guide will walk you through enabling One-Time Password (OTP) multi-factor authentication, updating your password, verifying your email, and adding an SSH key.

## Step 1: Set Up OTP Authentication (MFA)
Multi-Factor Authentication (MFA) adds an extra layer of security to your account. You will use an authenticator app (like Google Authenticator, 1Password, or Authy) on your mobile device to generate temporary codes.

1. Download an authenticator app from your mobile device's app store.

2. Log in to the [ilifu accounts dashboard](https://accounts.ilifu.ac.za) using your ilifu username and the temporary password provided to you.

3. On your computer screen, you will see a QR Code.

4. Open your mobile authenticator app and select Add an Account or click the + icon.

5. Scan the QR code on your computer screen using your phone's camera.

6. Your app will generate a 6-digit verification code.

7. Enter this 6-digit code into the prompt on your computer, add a device name for reference, then click Submit.

If you lose access to your phone, you will need to request that your OTP authentication is reset for your account by emailing a request to [support@ilifu.ac.za](mailto:support@ilifu.ac.za).

## Step 2: Update Your Temporary Password
For security reasons, the temporary password you were issued must be changed immediately upon your first successful login.

After enabling One-Time Password (OTP) MFA you will automatically be prompted to update your password.

1. Enter a new, strong password.

2. Confirm your new password and click Submit.

## Step 3: Verify Your Email Address

After updating your password, you must verify that your email address is correct. 

2. Check the inbox of the email address used to create your account.

3. Look for an email with the subject "Verify email".

4. Click the "Link to e-mail address verification" link inside the message.

You will be redirected to the secure login page with a confirmation message.

Note: If you haven’t received the email within 5 minutes, please check your Spam or Junk folder, or click "Resend Verification Email" on the login screen.

## Step 4: Add an SSH Key to Your Account
If you plan to interact with the ilifu platform via the command line or securely push code/data, you must link an SSH key to your profile.

### 1. Locate or Generate Your SSH Key
If you don't have an SSH key pair yet, open your local terminal and run the following command to generate one:

```bash
ssh-keygen -t ed25519 -a 256
```

#### Best practice guidance

Please follow these SSH key hygiene practices:

* Use separate SSH keys for different purposes, such as work, personal use, production access and code repositories.
* **Protect private keys with a strong passphrase.**
* Never share private keys with anyone.
* Never send private keys by email, chat, ticketing systems or file-sharing platforms.
* Do not store private keys in scripts, shared folders, source code repositories or documentation.
* Remove old or unused public keys from systems and services.
* Avoid SSH agent forwarding unless specifically required and approved.
* Review your ~/.ssh/config, shell history, Git remotes, scripts and automation files for references to old keys.
* Ensure private key files have restrictive permissions and are readable only by your user account.

### 2. Copy Your Public Key
Display and copy your public key (usually ending in .pub). Do not copy your private key.

**Mac/Linux**: 
```bash
cat ~/.ssh/id_ed25519.pub
```

**Windows** (Command Prompt):
```bash
type %userprofile%\.ssh\id_ed25519.pub
```

### 3. Add the Key into Your Profile
Use the [SSH key management tool](https://accounts.ilifu.ac.za/ssh_keys) or navigate to your account settings in the top right corner of the [ilifu accounts dashboard](https://accounts.ilifu.ac.za), Select Profile, and click Update SSH Keys.

Paste your copied public key into the SSH Key text field.

Click Add to save your key on your profile.

## Setup Complete!

You have successfully secured your account. You will now be to access ilifu services. On future logins, you will only need your new password for web-based services and the rotating 6-digit OTP code from your phone for both web-based services and access via SSH.

If you encounter any issues during this setup process, please contact the ilifu support team at [support@ilifu.ac.za](mailto:support@ilifu.ac.za).