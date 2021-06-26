


# Sever Kickoff

okay where to start? 
I guess first I could apply/compile the changes on protos
on the client side I created the sample message list.
I did not create an RPC in the protos and did not include the stub, and client codes.
I could also add the standard service codes on the server to receive the request.
Then I guess I could start thinking what to do with the data.

# Wiki Pages and docs

so the other day I was thinking about having a document like this
in the repo. well it is not certaily the norm.
the professional way is to put it in the code, docstrings, right?
but for someone like me that likes to wramble when working to keep track of my 
disperse thoughts, would that work?
(again I think that failed repo profaneDB can teach me a thing or two in this area.)

Anyways, I guess I couod put this in a docs directory, not important.
but the docs directory is more for code usage and API...
This is more like a blog.

and the drawing page has got too big. begs the question should create multiple files.

can't still clearlt see the value and advantage of wiki pages to in-repo docs.

# Client Left off works

okay I took care of both rpc, and client/server standard codes.
now the next main problem to tackle is what to do with the data in the server side.


So we get the data as a list, it is a list of models that can belong to 3 different kinds.
Should I just create 3 seperate list of these models to begin with?

I will need python mapping structures for the protos.

Then there is the task of finding the references

QQ: can we create the mapping python classes more nicely and automated?

the library that I thought would do this is called betterproto


# Exploring the BetterProto

okay so this library creates more clean python classes.
but I still don't want to rely on it for send/receive of messages

It is not still the same as python native class, is it though have restrictions?

so if we  get  the message with  Standard GRPC then how to convert it to a better proto
We cannot receive the message with the new library because of the error for starters
But even if There was no error I wouldn't still want to rely on it for compiling in binary purposes
I just like the data classes that are generated automatically potentially i.e. could convert the message into Jason
And then I guess these classes have a from Dictionary method
I could also you put the classic proto message into the new message fields
I guess there is no hard typing enforcing or whatever it is it allows you to Insert a classic proto into the field of the new proto
but it won't be useful since the type change and if you create a type and then put it in old classic message you are not using the new classes anyway.
I guess I could convert to Jason and back to proto
Or I could create some sort of generalized from Proto function that creates the new protocols directly from the old protos.


## How to convert Basic Proto Message to BetterProto classes?


The betterproto classes are very similar to the type of data classes that I like to work with, they have some data-type defenitions that not sure yet if they could be problematic.

So If those classes are my target data structure, the question is how to convert a classic proto messagae into them.

1- Easy and potentially inefficient way (?) convert the whole thing into dict and then back into the new classes.
- requires minimal coding.
-  maybe takes more compute to do an extra conversion.

2- (and this is a bad one) to create from_proto() methods for each class but then convert the relevant portion of the message to a dict and back to python class. I am guessing that in the dict reading method of the betterproto class a similar approach is likely to happen.

3- you would create a recurisve from_proto message that is passing the Old proto as inputs untill it gets to the basic types.

4- all of this additional methods would be best to be as Extenions.
So we can recompile freely.

## experiment with BetterProto conversion extension classes

So the idea was to create a set of extension classes that would convert a classic proto message to the new better proto message.

I could go like:
classic_proto --> dict --> betterproto
(wait does it really work? ->test-> yep works very fine)

