## Cloud for Customer API Examples

**PLEASE NOTE THAT THIS PASE IS STILL UNDER CONSTRUCTION**

**Note this is not an offical repository from SAP Cloud for customer**. 

This repository is an attempt to provide a set of sample payloads for SAP Cloud for customer OData APIs. You can use these payloads to bootstrap your project. 

###Overview

####OData versions
If you are new to OData protocol in general it is recommended that you go to http://www.odata.org/ to read and understand the basic aspects of this protocol. SAP Cloud for customer, specifically, **supports the V2.0 of the OData protocol** (with some additional enhancements), you can read about the version specific aspects [here](http://www.odata.org/documentation/odata-version-2-0/).

####OData service catalog
You can use the OData Service Catalog https://myNNNNNN.crm.ondemand.com/sap/c4c/odata/v1/odataservicecatalog/ODataServiceCollection, available in your C4C tenant, to get a list of all services that are available for usage. This service would return both the SAP shipped standard OData services as well as the custom services that you may have modeled in your tenant using the OData Service Explorer (for more details around the OData Service Explorer, please refer to the Cloud for customer product documentation).

####Authentication
SAP Cloud for customer OData supports 2 authentication mechanisms:
  * Basic authentication
  * OAuth SAML bearer flow (you can find sample Java implementation of OAuth SAML bearer client [here](https://github.com/venkyvb/OAuthSAMLClient).)
  

####Making a Request

#####Formats
SAP Cloud for customer OData API's support request payloads in both Atom XML and JSON format. The default payload format is AtomXML. To use JSON payloads the following needs to be done:
  * For the GET requests - use the system query parameter **$format=json**. E.g. to get the above mentioed ODataServiceCollection in JSON format you have to use https://myNNNNNN.crm.ondemand.com/sap/c4c/odata/v1/odataservicecatalog/ODataServiceCollection?$format=json
  * For the POST/PATCH/PUT requests use the HTTP Content-Type header. (**Content-Type: application/json**)


#####Authentication
All requests should have an Authoriation header.
  * For Basic authentication this should be **Authorization: Basic <base64 encoded value of the username:password>**
  * For OAuth SAML bearer flow this should be **Authorization: Bearer <OAuth token>** (note the space between Bearer and the actual OAuth token)

#####CSRF Token
For modifying methods (POST/PUT/PATCH) in addition to the Authorization header it is also mandatory to specify a CSRF token as well. Now the question arises as to how can you get a CSRF token. The following steps need to be undertaken to fetch a CSRF token that can be used to make the modifying calls:
  * First perform a GET to the service end-point (e.g. invoke the $metadata end-point https://myNNNNNN.crm.ondemand.com/sap/c4c/odata/v1/c4codata/$metadata). For this call, pass the header (in addition to the Authorization header) **X-CSRF-Token**. The value for this HTTP header should be **Fetch**.
  * The C4C server will respond back with the EDM metadata (of course since this is what is being requested by the GET call), in addition it would also send a **Response header** called **X-CSRF-Token** (same name as what was sent) and this will have a token value. The token value needs to be used for subsequent calls (like POST/PUT/PATCH).

#####Server side paging
For GET requests, if no query options are specified, the server enforces paging to provide better performance. Currently the page size is fixed at 1000 entries. However at the end of 1000 entries the server includes a **next** link that allows the caller to get the next 1000 entries. The link would be something like this: https://myNNNNNN.crm.ondemand.com/sap/c4c/odata/v1/c4codata/OpportunityCollection?$format=json&$skiptoken=1001 (in this specific case the OpportunityCollection entity set is being queried).

###OData feature support


  



  
  
  
  

  

  
 

 
  

  



