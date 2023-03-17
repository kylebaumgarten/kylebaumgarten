# This Section covers a method of utilizing built in Maximo methods for external users to interact with Maximo #

**PLEASE NOTE: These methods require the invocation of an apikey too run, therefore, ensure that the apikey you use is protected from accessing other data points**

In the code linked, we will use a simple api call that will return either a 0 or 1 to the Maximo system depending on a choice selected.

The reason for this is to show effectively how it works at a base level and allow for future customization from others.

The format of this call to then make will then look something like:

https://HOSTURL/api/script/SCRIPTNAME?&response=1&apikey=APIKEYGOESHERE&id=SR106001