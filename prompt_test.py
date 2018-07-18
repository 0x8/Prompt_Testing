import coloredlogs
import threading
import logging
import sys
import os

LOG_LEVEL = 'DEBUG'
_LOG_LEVEL = eval('logging.'+LOG_LEVEL)

class CommandLineInterface:

    def __init__(self, **kwargs):
        """ Initialize CLI and prompt for action """ 
        # Arbitrary keyword arguments
        for key in kwargs:
            self.__dict__[key] = kwargs[key]
        
        # Local logging instance
        self.logger = logging.getLogger("prompt_test.CommandLineInterface")
        self.logger.setLevel(_LOG_LEVEL)

        coloredlogs.install(logger=self.logger, level=LOG_LEVEL)

        if 'prompt' not in kwargs.keys():
            self.prompt = '>>> '

        if 'welcome_msg' not in kwargs.keys():
            self.welcome_msg = 'Welcome to the prompt test!\n'

        if 'command_resolution' not in kwargs.keys():
            self.command_resolution = {
                'hello' : {
                    'function': 'say_hello',
                    'type': 'self_method',
                    'threadsafe': True,
                },
                'nickname': {
                    'function': 'set_nickname',
                    'type': 'self_method',
                    'threadsafe': False,
                },
                'goodbye' : {
                    'function': 'good_bye',
                    'type': 'self_method',
                    'threadsafe': True,
                },
            }
            if 'name' not in kwargs.keys():
                self.name = 'User'

        self.run_prompt(self.prompt)
    
    def say_hello(self):
        print('Hello, {}!'.format(self.name)) 

    def set_nickname(self):
        self.nickname = input('Please enter new nickname: ')
        print('Nickname changed to: ', self.nickname) 

    def run_prompt(self, prompt):
        """ Run the main command line prompt handling commands as they are typed """
        
        # Get logger
        logger = self.logger

        # Main Loop - Infinite While until user enters 'quit'
        while True:
            
            cmd = input(prompt)
            
            # Check that the user doesn't wish to quit
            if cmd == 'quit':
                break
            else:
                self.handle_cmd(cmd)

        # Post-loop cleanup
        print('Goodbye!')
        sys.exit(0)

    def handle_cmd(self, cmd):
        """ Handle the passed command from the prompt """

        # Get logger
        logger = self.logger

        if not self.command_resolution:
            logger.error('Somehow command_resolution is unset.')
            logger.error('Exiting execution')
            sys.exit(1)
        else:
            command_resolution = self.command_resolution
        
        if cmd in command_resolution.keys():
            if type(command_resolution[cmd]) == dict:
                # All dict resolutions should contain the following keys
                required_keys = [
                    'function',
                    'threadsafe',
                    'type',
                ]
                
                # Check for required keys
                if set(required_keys) - set(self.command_resolution[cmd].keys()):
                    # Missing required keys
                    required = set(required_keys)
                    provided = set(self.command_resolution[cmd].keys())
                    missing_keys = required - provided
                    logger.error('Command [{}] Missing Required Keys: [{}]'.format(cmd, missing_keys))
                    return 1

                logger.debug('Splitting command [{}] into atomic parts.'.format(cmd))
                command = command_resolution[cmd]
                threadsafe = command['threadsafe']
                cmd_type = command['type']
                target_function = command['function']
                
                # Get optional arguments to function
                if 'args' in command.keys():
                    logger.debug('Command has optional args, grabbing...')
                    args = command['args']
                else:
                    args = None

                # Evaluate type
                if cmd_type == 'self_method':
                    # Command is member of CLI class
                    logger.debug('Setting target of self_method')
                    target = eval('self.'+target_function)
                    
                    # Check for thread safety:
                    if threadsafe:
                        # Launch in new thread
                        logger.debug('Target is threadsafe, running in new thread.')
                        if args:
                            logger.debug('Running in thread with args')
                            wt = threading.Thread(target=target, args=(args))
                        else:
                            logger.debug('Running in thread without args')
                            wt = threading.Thread(target=target)
                        wt.start()
                        wt.join()

                    else:
                        # Not threadsafe so launch in main control flow
                        if args:
                            logger.debug('Calling target with args')
                            target(args)
                        else:
                            logger.debug('Calling target with no args')
                            target()

            else:
                self.__dict__[command_resolution[cmd]]()

        

if __name__ == '__main__':
    cli = CommandLineInterface()
