# Automated Network Validation

This repository provides an automated process to checking the validity of network configuration files generated during lab sessions.

To use this repository, each student group need to:

1. Clone the main branch of this repository
2. Create a branch named after their group
3. Copy network device configuration to the branch
4. Commit and push the branch
5. Check if their configuration files have passed the checks

Instructors will also be able to view the results and advise students on how to fix any errors.


## Instructions for students:

Follow these instructions after completing all the lab required configuration steps:

1. Clone the main branch of this repository in the home directory:

   ```
   $ cd
   $ git clone --branch main https://github.com/DAL-INWK/Design_Fall_2022
   ```

2. Create a branch named after your lab and group numbers (use the format labX_gYY, where X is the lab number and YY is your group number) and checkout the branch:

   ```
   $ cd Design_Fall_2022
   $ git checkout -b lab1_g99
   ```

3. Copy network device configuration using Ansible:

   ```
   $ export ANSIBLE_HOST_KEY_CHECKING=False
   $ ansible-playbook -i inventory.txt play_backup.yml
   ```

   If the above process was successful (all routers report ok=1), then you will find a folder 'lab/configs' created in the repository. If the process failed, then it is likely that the SSH configuration on the network devices is not completed and you must follow the instructions in the lab assignment documents to configure SSH.

4. Commit the changes and push the branch:

   ```
   $ git add lab
   $ git status
    On branch lab1_g99
    Changes to be committed:
      (use "git reset HEAD <file>..." to unstage)

            new file:   lab/configs/R11.cfg
            new file:   lab/configs/R12.cfg
            new file:   lab/configs/R21.cfg
            new file:   lab/configs/R22.cfg
            new file:   lab/configs/R23.cfg
   $ git commit -m "add config files for group g99"
   $ git push --set-upstream origin lab1_g99
   ```

   Note: the last step may require a username/password

5. Check if your configuration files have passed the checks:

   - Go the github [repository](https://github.com/DAL-INWK/Design_Fall_2022)
   - click on 'barnches'   

   ![](img/branches.png)

   - Verify that you have a green checkmark in front of your branch. You can click on the checkmark to find details.

   ![](img/checks.png)

## Validation Process

This network validation process applies some CI/CD principles to check device configuration against some common configuration errors. The pipeline includes the following components:

![Pipeline](img/pipeline.png)

- [Ansible](https://www.ansible.com/): Network automation tool
- [Git](https://git-scm.com/): Revision control system
- [GitHub](https://github.com/): Cloud-based Git repository
- [Drone](https://www.drone.io/): Continuous integration platform
- [Batfish](https://www.batfish.org/): Network configuration analysis tool
- [Python](https://www.python.org/): Programming language for network automation
- [Docker](https://www.docker.com/): Platform for building, deploying, and managing containerized applications
