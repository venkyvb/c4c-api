## Cloud for Customer API Examples

**PLEASE NOTE THAT THIS PASE IS STILL UNDER CONSTRUCTION**

**Note this is not an offical repository from SAP Cloud for customer**. 

This repository is an attempt to provide a set of sample payloads for SAP Cloud for customer OData APIs. You can use these payloads to bootstrap your project. 

###Overview

####OData versions
If you are new to OData protocol, it is recommended that you go to http://www.odata.org/ to read and understand the basic aspects of this protocol. SAP Cloud for customer, specifically, **supports the V2.0 of the OData protocol** (with some additional enhancements and a few limitations), you can read about the version specific aspects [here](http://www.odata.org/documentation/odata-version-2-0/).

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
  * For Basic authentication this should be **Authorization: Basic _base64_encoded_value_of_username:password_**
  * For OAuth SAML bearer flow this should be **Authorization: Bearer _OAuth_token_** (note the space between Bearer and the actual OAuth token)

#####CSRF Token
For modifying methods (POST/PUT/PATCH) in addition to the Authorization header it is also mandatory to specify a CSRF token as well. Now the question arises as to how can you get a CSRF token. The following steps need to be undertaken to fetch a CSRF token that can be used to make the modifying calls:
  * First perform a GET to the service end-point (e.g. invoke the $metadata end-point https://myNNNNNN.crm.ondemand.com/sap/c4c/odata/v1/c4codata/$metadata). For this call, pass the header (in addition to the Authorization header) **X-CSRF-Token**. The value for this HTTP header should be **Fetch**.
  * The C4C server will respond back with the EDM metadata (of course since this is what is being requested by the GET call), in addition it would also send a **Response header** called **X-CSRF-Token** (same name as what was sent) and this will have a token value. The token value needs to be used for subsequent calls (like POST/PUT/PATCH).

#####Server side paging
For GET requests, if no query options are specified, the server enforces paging to provide better performance. Currently the page size is fixed at 1000 entries. However at the end of 1000 entries the server includes a **next** link that allows the caller to get the next 1000 entries. The link would be something like this: https://myNNNNNN.crm.ondemand.com/sap/c4c/odata/v1/c4codata/OpportunityCollection?$format=json&$skiptoken=1001 (in this specific case the OpportunityCollection entity set is being queried).

####Sample client
If you are looking for sample Java client that can be used for making OData calls to C4C you can go [here](https://github.com/venkyvb/ODataConsumerSample). Note that this sample uses Apache Olingo library to construct and read OData payloads.

###OData feature support
As mentioned above, SAP Cloud for customer supports V2 version of the OData protocol. Here we list the set of system query options that are supported by the C4C OData implementation. For sake of brevity, the initial part of the URL https://myNNNNNN.crm.ondemand.com/sap/c4c/odata/v1/c4codata is skipped in the following examples:


####System Query Options

Option | Example | Description
-------|---------|------------
$format  | /OpportunityCollection?$format=json | Returns Opportunity entries in JSON format with server side paging
$top |  /OpportunityCollection?$top=10 | Returns top 2 Opportunities. 'Top 2' is defined by server logic here
$skip | /OpportunityCollection?$skip=10 | Skips the first 10 entries and then returns the rest
$select | /OpportunityCollection?$select=OpportunityID,AccountID | Returns Opportunity entries but only 2 attributes OpportunityID and AccountID
$orderby | /OpportunityCollection?$orderby=CloseDate desc&$top=10 | First performs an orderby on the Opportunities and then selects the top 10 from that ordered list. Here **desc** means descending order.
$count | /OpportunityCollection/$count | Returns the total number of Opportunities
$inlinecount | /OpportunityCollection?$top=10&$inlinecount=allpages | Returns the top 10 opportunities and also returns the total number of opportunities.


#####$inlinecount response payload

XML response with inlinecount. The Element <m:count> contains the response to the $inlinecount.
```XML
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata" xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" xml:base="https://my306695.vlab.sapbydesign.com/sap/c4c/odata/c4codata/">
	<id>https://myNNNNNN.crm.ondemand.com/sap/c4c/odata/c4codata/OpportunityCollection</id>
	<title type="text">OpportunityCollection</title>
	<updated>2015-08-23T17:30:32Z</updated>
	<author>
		<name/>
	</author>
	<link href="OpportunityCollection" rel="self" title="OpportunityCollection"/>
	<m:count>39080</m:count>
	<entry>
		<id>https://myNNNNN.crm.ondemand.com/sap/c4c/odata/c4codata/OpportunityCollection('00163E03A0701ED28BCEC7F4AA474109')</id>
		<title type="text">OpportunityCollection('00163E03A0701ED28BCEC7F4AA474109')</title>
		<updated>2015-08-23T17:30:32Z</updated>
		....
```

JSON response with inlinecount. The attribute __count contains the response to the $inlinecount.
```JSON
{
  "d": {
    "__count": "39080", 
    "results": [
      {
        "AccountID": "10009", 
        "AccountName": {
          "__metadata": {
            "type": "http://sap.com/xi/AP/CRM/Global.ENCRYPTED_LONG_Name"
          }, 
          "content": "Primo Sustainable products", 
          "languageCode": "E"
        }, 
        ...
```

#####$filter

Option | Example | Description
-------|---------|------------
eq | /OpportunityCollection?$filter=AccountID eq '1001910' | Gets all Opportunity entries that matches the specified AccountID
endswith | /AccountCollection?$filter=endswith(AccountName,'LLC') | All accounts whose AccountName ends with 'LLC'. **_Note that the Property Name has to be specified first_**.
startswith | /AccountCollection?$filter=startswith(AccountName,'Porter') | All accounts whose AccountName starts with 'Porter'. **_Similar to endswith note that the Property Name has to be specified first_**.

For usage of $expand with $filter see the $expand section below.

#####$expand

C4C supports $expand option via Navigaton Properties. E.g. /AccountCollection?$top=10&$format=json&$expand=AccountMainAddress. Here AccountMainAddress is a Navigation Property defined in the EDM for the Account Entity (see the Entity defintion below).

```XML
			<EntityType Name="Account">
				<Key>
					<PropertyRef Name="ObjectID"/>
				</Key>
				<Property Name="ABCClassificationCode" Type="Edm.String" Nullable="true" MaxLength="1" FixedLength="true" sap:creatable="true" sap:updatable="true" sap:filterable="false"/>
				<Property Name="ABCClassificationCodeText" Type="Edm.String" Nullable="true" sap:creatable="false" sap:updatable="false" sap:filterable="false"/>
				<Property Name="AccountFormattedName" Type="Edm.String" Nullable="false" MaxLength="40" FixedLength="true" sap:creatable="false" sap:updatable="false" sap:filterable="false"/>
				<Property Name="AccountID" Type="Edm.String" Nullable="true" MaxLength="10" FixedLength="true" sap:creatable="true" sap:updatable="true" sap:filterable="false"/>
				<Property Name="AccountName" Type="Edm.String" Nullable="true" MaxLength="240" FixedLength="true" sap:creatable="false" sap:updatable="true" sap:filterable="false"/>
....
				<NavigationProperty Name="AccountMainAddress" Relationship="http://sap.com/xi/AP/CRM/Global.Account_AccountMainAddress" FromRole="Account" ToRole="AccountMainAddress"/>
				<NavigationProperty Name="AccountNotes" Relationship="http://sap.com/xi/AP/CRM/Global.Account_AccountNotes" FromRole="Account" ToRole="AccountNotes"/>
				<NavigationProperty Name="AccountRole" Relationship="http://sap.com/xi/AP/CRM/Global.Account_AccountRole" FromRole="Account" ToRole="AccountRole"/>
				<NavigationProperty Name="AccountSalesData" Relationship="http://sap.com/xi/AP/CRM/Global.Account_AccountSalesData" FromRole="Account" ToRole="AccountSalesData"/>
				<NavigationProperty Name="AccountTeam" Relationship="http://sap.com/xi/AP/CRM/Global.Account_AccountTeam" FromRole="Account" ToRole="AccountTeam"/>
				<NavigationProperty Name="ExternalIDMapping" Relationship="http://sap.com/xi/AP/CRM/Global.Account_ExternalIDMapping" FromRole="Account" ToRole="ExternalIDMapping"/>
			</EntityType>
```			

Note that C4C currently **DOES NOT** support the usage of properties from expanded navigations as part of $filter conditions. However what is possible is to 



  



  
  
  
  

  

  
 

 
  

  



