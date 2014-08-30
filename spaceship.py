import commandline


def main():
    cmd = commandline.SpaceshipCommand('spaceship-terminal')
    cmd.cmdloop()

if __name__ == '__main__':
    main()
