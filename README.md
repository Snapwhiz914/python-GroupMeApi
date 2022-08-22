# GroupMe API Python Wrapper

A simple python library that aims to encompass all features of GroupMe present in thier documentation in https://dev.groupme.com/docs/v3

### Use Cases

This library is not meant to be used to create a full fledged GroupMe client. It is meant to be used to automate GroupMe (for example, bots, automatic message sending/replying, etc.)

### Disclaimer

Because of the uses of this library, I will not be prioritzing it as much as I will other GroupMe projects, as it is simply an API wrapper.

### Documentation for this library

Every method in this library, unless otherwise stated below, will return one of the following:
 - An error (see error section)
 - A python object (see below)
 - A dictionary object that has the same structure as its corresponding API endpoint in the https://dev.groupme.com/docs/v3
 - True, if there is no return data stated in the offical docs and there wasn't an error raised before it is returned
 - generally, if the main message of a result is encompassed in a name, eg: "messages": [] will just be returned as [], and "between": True will just be returned as True. Refer to documentation so you know when this will happen

Methods that will return a different value than a dictionary object with the same structure as its corresponding API endpoint:
 - user.get_groups(): [Group object] (Note: [] means a list of objects)
 - user.get_former_groups(): [Group object]
 - user.create_group(): Group object
 - user.update_group(): Group object
 - group.add_members(): String (results id) (See documentation for its purpose)
 - user.change_owner(): Boolean (True for success, False if not) (Note: this method only supports changing the owner of one group at a time, unlike the endpoint stated in the offcial docs)
 - user.get_dms(): [DM object]
 - user.create_bot(): Bot object
 - user.get_bots(): [Bot object]
 - user.does_block_exist(): Boolean (True if exists, False if not)

### Future

 - The image service will be implemented soon
 - Maybe a websocket service for live events?
