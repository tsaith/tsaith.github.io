Title: Create a user account to deploy production on ubuntu
Date: 2015-03-30
Tags: linux
Category: Misc


On production server, it is a good practice to create a user account (named `deployer`) which is supposed to take care jobs of deployment. The steps are described as following.

- Log in the server as `root` via `ssh`
```
ssh SERVER_IP
```
- Add new user named `deployer`
```
adduser deployer
```

- Add `deployer` to group `sudo`
```
gpasswd -a deployer sudo
```

- Switch from `root` to `deployer`
```
su -l deployer
```

- Create `.ssh` directory and set proper access permission
```
mkdir ~/.ssh
chmod 700 ~/.ssh
```

- Copy the content of `id_rsa.pub` and paste it to `authorized_keys`

On local computer:
```
cat ~/.ssh/id_rsa.pub | pbcopy
```
On remote server:
```
vi ~/.ssh/authorized_keys
```
and paste the content of public key.

- Set proper access permission on `authorized_keys`
```
chmod 600 .ssh/authorized_keys
```

- Return to `root`
```
exit
```

- Disable `root` login through SSH
```
vi /etc/ssh/sshd_config
```
and modify the line of `PermitRootLogin` as
```
PermitRootLogin no
```

- Restart SSH
```
service ssh restart
```

- Open a new terminal on local computer and log in the server as `deployer`
```
ssh deployer@SERVER_IP
```

- Let `deployer` can use `sudo` without password
```
sudo visudo
```
Add following line at the end of file
```
deployer ALL=(ALL) NOPASSWD: ALL
```
Execute `Ctrl-x` -> `Y` -> `Enter` to save and exit file.
