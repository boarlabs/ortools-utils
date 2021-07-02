


# Server Kickoff

okay where to start? 
I guess first I could apply/compile the changes on protos
on the client side I created the sample message list.
I did not create an RPC in the protos and did not include the stub, and client codes.
I could also add the standard service codes on the server to receive the request.
Then I guess I could start thinking what to do with the data.


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


**Question:** Why I wanted to work with betterprotos again? -> 
needed to have a miror python (natural) data structure
that I can more freely work with. Then I thought manually writing that many classes would be dull.
So had idea that this betterproto lib could generate the classes that are more python.
so far seems that the auto-generated classes can actually act as a normal class.
I decided to add some extension classes to  work with these auto classes.

I wanted to create the python objects directly from the proto messages.
I added the from_proto, methods, but there is some isssues.
I guess it is acting normall, if we want to treat it as a normal python object
but if we want to have it able to generate binaries, then it is not there yet.
Having these classes I can go without it for now.

But  I guess need to make an issue about this
Another issue is to move test file to its proper place and set it up.

so if I want to move on from this, then what is next?


# What happens at the server side when reading a request?

- we recive the proto message(s), each message is a model.

- we create a python miror of that object. (using the extension classes)

- now these proto-mirror objects, are really basic now. no  methods. 

- we need to add methods to them.

- in specific I need to add some searchability, index them someHow.

- Am thinking these indexing/searching would preferd to be genric. but again, if i could contain it to my specific needs, is wise.
  
- so these messages each, is an extended model; which could be one of the three models
  - concrete model -> no referes to other models, but others may refer to it. 
  - expression model: no refer to other models, but some refers to its own variables.
  - reference model: all is references to other models and variables.


- when we have a list of these objects, what should we do with them?

- should we add some method, like  "find_references" to each object? 
  - we have the list of the objects from messages already. we can create a method for them to search their references, and maybe replace the names with objects.
  

## how to convert name based references to some sort of pointer?

- so I have a concrete mipmodel, is that all that I need? do I still need to create any extra objects from it? (like those I had in the mip client library)
- One of the reasons that I couldn't use the old protos in the mipclient was that varaiable protos were added by value.
- So one thing that needs to be ivestigated here is that for these auto generated classes, do we have pass by value again?


## how to search all models based on the names?

- okay here I think again some sort of add-ons to these classes would be helpfull. but here we have both a list of objects in the first level and then some hierarchy under each, how to make it flat? if I use the tools I have so far, I guess we would have multiple dicts, i.e. one for each ExtendedMPModel object.


