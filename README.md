# Prompt Test
This project is an experiment of how simple command line interface prompts can be built in python
including an extensible method for adding command resolution later. This is a _test_ and as such
is quite far from perfect and likely doesn't even follow most of python's best practices.

Currently Broken (for sure):
    - Nickname is NOT threadsafe so it is not run in a thread however say_hello _is_ executed in a
      thread which for whatever reason is simply not updated following the call to nickname

    - There is no help or listing of commands. Sorry, you'll have to suffer through my code.
