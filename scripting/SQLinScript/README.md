# This Section covers a method of utilizing SQL statements with write access within automation scripts. #

**PLEASE NOTE: These methods can be highly dangerous and destructive to data if you are unsure of what you are doing.**

Review the syntax and start slowly to make sure it is creating desired output.
If the rest of this repository is use at your own risk, consider this super-duper use at your own risk.

## **What I use these methods in Scripts for:** ##
From experience, I find that the vast majority of business processes can be accomplished with standard Maximo scripting tools.

## **But what if it doesn't?** ##
Although fairly sophisticated, some functionality required is not accessible within Maximo, intentionally or otherwise.

## **What do we do then?** ##
I'm glad you asked. In case of an urgent business need, statements like these can be very powerful and useful.
### **Following the necessary precautions and ensuring your statement's correctness with the script pointing to the correct objects can be invaluable for writing typically read-only objects and fields** ###

## **Where do you use these statements?** ##
As stated above, I find that most needs can be accomplished via OOB maximo scripting functionality.
If something is especially funky, things like no access checks and other tools can be utilized.

**I have found that these statements are most useful when tasked with integrations requiring substantial logic**

## **Spare the Suspense, what is substantial logic?** ##
When I say substantial logic I mean logic that extends out of the scope of standard MIF possibilities (Enterprise Service, Object Structure, etc.) level scripting.
Imagine a situation where based on a value received in a csv, you would have to make a decision on what interface your data will actually enter. 

The kicker?

This data is agnostic to these differences and will be sent to the same endpoint.

**So what do you even do here?**

Curl up in a ball? Ask for the data to be cleaned up, placing the burden back on somebody else? 

Maybe a custom object and application will work? Although, if the same functionality as OOB objects is desired I hope you: 
1.) are on premise and have access to source code
2.) Know how to emulate said source code in Java because running a higher level scripting language over the top doesn't seem like the most efficient option.


**Maybe there's a better way, though?**

Maybe these newly learned sql statements can be used to route this data from a custom object into specified interface tables (which are typically read-only)

**That settles it! Let's use our newfound scripting skills to make something cool!**

Note: Read up on Enterprise Service scripting and its great capabilities in the other section of this Repo to avoid confusion.
