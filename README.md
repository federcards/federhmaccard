FederHMACCard
=============

This repository includes the firmware and a python GUI program for
FederHMACCard, a simple HMAC generator on BASIC-programmed smartcards produced
by ZeitControl.

The card itself has 72 slots and can be loaded with secrets for HMAC
calculation. The secrets, once loaded, cannot be exported.

Since HMAC is used for generating TOTP-based login codes in various online
services, this card may be used as a TOTP code generator.

But it's also useful as a password generator. By providing a "seed" string,
it generates a pseudorandom string that is not predictable without knowing
the secret.

Thus the card constitutes an import role and improvement in centeralized
password management. Compare the card to a software password manager like
1Password or KeePass, where all passwords are stored under the same master
password and prone to a single point of failure(leaking the master password
would be disastrous), the card is a physical device that can not be easily
copied. Although there's still a master secret to be loaded onto the card, that
secret is not needed to be kept always available and may be stored safely (e.g.
in a locked safe or a bank).
