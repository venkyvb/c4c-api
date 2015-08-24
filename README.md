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
  

####SAP standard services vs. Custom services

SAP Cloud for customer product, offers an OData Service Explorer, using which one can view the standard servcies that are shipped by SAP (e.g. /c4codata/) as well as model tenant specific custom services. From an API point of view the custom services behave exactly the same way as a standard service does. Only the URL paths for the services are different:
  * Standard services have the URL path - https://myNNNNNN.crm.ondemand.com/sap/c4c/odata/v1/....
  * Custom services have the URL path - https://myNNNNNN.crm.ondemand.com/sap/c4c/odata/cust/v1/...
  

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
For GET requests, if no query options are specified, the server enforces paging to provide better performance. Currently the page size is fixed at 1000 entries. However at the end of 1000 entries the server includes a **next** link that allows the caller to get the next 1000 entries. The link would be something like this:
```
https://myNNNNNN.crm.ondemand.com/sap/c4c/odata/v1/c4codata/OpportunityCollection?$format=json&$skiptoken=1001 
```
(in this specific case the OpportunityCollection entity set is being queried).

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
	<id>https://myNNNNNN.crm.ondemand.com/sap/c4c/odata/v1/c4codata/OpportunityCollection</id>
	<title type="text">OpportunityCollection</title>
	<updated>2015-08-23T17:30:32Z</updated>
	<author>
		<name/>
	</author>
	<link href="OpportunityCollection" rel="self" title="OpportunityCollection"/>
	<m:count>39080</m:count>
	<entry>
		<id>https://myNNNNN.crm.ondemand.com/sap/c4c/odata/v1/c4codata/OpportunityCollection('00163E03A0701ED28BCEC7F4AA474109')</id>
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

For every entity (that is not a Header entity e.g. Account or Opportunity etc.) the C4C Odata framework implicitly generates a Navigation Property to the parent entity as well as a Navigation Property to the Header entity (if the parent entity is not a Header itself). If you consider the metadata below, the following can be seen:
  * Opportunity is the Header entity
  * OpportunityItem has the Opportunity as the Parent (as well as the Header) and 
  * OpportunityItemRevenuePlanReporting has OpportunityItem as the Parent and Opportunity as the Header entity

For each of the entities below, a Navigation Property is available that allows a given Entity type to navigate to the immediate parent e.g. OpportunityItemRevenuePlanReporting has a 
  * Navigation Property Opportunity that allows navigation to the Header and 
  * Navigation Property OpportunityItem that allows navigation to the Parent.

This pattern holds good for all OData services generated by C4C (both standard as well as custom services).

```XML
			<EntityType Name="Opportunity">
				<Key>
					<PropertyRef Name="ObjectID"/>
				</Key>
				<Property Name="ApprovalStatusCode" Type="Edm.String" Nullable="true" MaxLength="2" FixedLength="true" sap:creatable="false" sap:updatable="false" sap:filterable="false"/>
				<Property Name="ConsistencyStatusCode" Type="Edm.String" Nullable="true" MaxLength="2" FixedLength="true" sap:creatable="false" sap:updatable="false" sap:filterable="false"/>
				<Property Name="ID" Type="Edm.String" Nullable="true" MaxLength="35" FixedLength="true" sap:creatable="true" sap:updatable="true" sap:filterable="false"/>
				<Property Name="LifeCycleStatusCode" Type="Edm.String" Nullable="true" MaxLength="2" FixedLength="true" sap:creatable="false" sap:updatable="false" sap:filterable="false"/>
				<Property Name="Name" Type="Edm.String" Nullable="true" MaxLength="765" FixedLength="true" sap:creatable="true" sap:updatable="true" sap:filterable="false"/>
				<Property Name="ObjectID" Type="Edm.String" Nullable="true" MaxLength="70" FixedLength="true" sap:creatable="false" sap:updatable="false" sap:filterable="false"/>
				<Property Name="OriginTypeCode" Type="Edm.String" Nullable="true" MaxLength="3" FixedLength="true" sap:creatable="true" sap:updatable="true" sap:filterable="false"/>
				<Property Name="PhaseProgressEvaluationStatusCode" Type="Edm.String" Nullable="true" MaxLength="2" FixedLength="true" sap:creatable="false" sap:updatable="false" sap:filterable="false"/>
				<Property Name="PriorityCode" Type="Edm.String" Nullable="true" MaxLength="1" FixedLength="true" sap:creatable="true" sap:updatable="true" sap:filterable="false"/>
				<Property Name="ProcessingTypeCode" Type="Edm.String" Nullable="true" MaxLength="4" FixedLength="true" sap:creatable="true" sap:updatable="true" sap:filterable="false"/>
				<NavigationProperty Name="OpportunityItem" Relationship="cust.Opportunity_OpportunityItem" FromRole="Opportunity" ToRole="OpportunityItem"/>
			</EntityType>
			<EntityType Name="OpportunityItem">
				<Key>
					<PropertyRef Name="ObjectID"/>
				</Key>
				<Property Name="ID" Type="Edm.String" Nullable="true" MaxLength="10" FixedLength="true" sap:creatable="true" sap:updatable="true" sap:filterable="false"/>
				<Property Name="NetAmount" Type="cust.Amount" Nullable="true" sap:creatable="false" sap:updatable="false" sap:filterable="false"/>
				<Property Name="ObjectID" Type="Edm.String" Nullable="true" MaxLength="70" FixedLength="true" sap:creatable="false" sap:updatable="false" sap:filterable="false"/>
				<Property Name="ParentObjectID" Type="Edm.String" Nullable="true" MaxLength="70" FixedLength="true" sap:creatable="false" sap:updatable="false" sap:filterable="false"/>
				<Property Name="ProductID" Type="Edm.String" Nullable="true" MaxLength="60" FixedLength="true" sap:creatable="true" sap:updatable="true" sap:filterable="false"/>
				<Property Name="Quantity" Type="cust.Quantity" Nullable="true" sap:creatable="true" sap:updatable="true" sap:filterable="false"/>
				<NavigationProperty Name="Opportunity" Relationship="cust.Opportunity_OpportunityItem" FromRole="OpportunityItem" ToRole="Opportunity"/>
				<NavigationProperty Name="OpportunityItemRevenuePlanReporting" Relationship="cust.OpportunityItem_OpportunityItemRevenuePlanReporting" FromRole="OpportunityItem" ToRole="OpportunityItemRevenuePlanReporting"/>
			</EntityType>
			<EntityType Name="OpportunityItemRevenuePlanReporting">
				<Key>
					<PropertyRef Name="ObjectID"/>
				</Key>
				<Property Name="DistributionAmount" Type="cust.Amount" Nullable="true" sap:creatable="true" sap:updatable="true" sap:filterable="false"/>
				<Property Name="DistributionDate" Type="Edm.DateTime" Nullable="true" Precision="8" sap:creatable="true" sap:updatable="true" sap:filterable="false"/>
				<Property Name="ObjectID" Type="Edm.String" Nullable="true" MaxLength="70" FixedLength="true" sap:creatable="false" sap:updatable="false" sap:filterable="false"/>
				<Property Name="ParentObjectID" Type="Edm.String" Nullable="true" MaxLength="70" FixedLength="true" sap:creatable="false" sap:updatable="false" sap:filterable="false"/>
				<Property Name="ReportingCurrencyDistributionAmount" Type="cust.Amount" Nullable="true" sap:creatable="true" sap:updatable="true" sap:filterable="false"/>
				<Property Name="RevenuePartnerUUID" Type="Edm.Guid" Nullable="true" sap:creatable="true" sap:updatable="true" sap:filterable="false"/>
				<NavigationProperty Name="Opportunity" Relationship="cust.Opportunity_OpportunityItemRevenuePlanReporting" FromRole="OpportunityItemRevenuePlanReporting" ToRole="Opportunity"/>
				<NavigationProperty Name="OpportunityItem" Relationship="cust.OpportunityItem_OpportunityItemRevenuePlanReporting" FromRole="OpportunityItemRevenuePlanReporting" ToRole="OpportunityItem"/>
			</EntityType>
```			
Note that C4C currently **DOES NOT** support the usage of properties from expanded navigations as part of $filter conditions. In order to do this the only option available is to apply the $filter condition at the child entity collection and then use an $expand condition to navigate to either the Parent collection or to the Header collection. 
E.g. if the requirement is to get all Opportunities that have a certain Product, as a part of a single GET request, then the way of doing this would be to make the following call:
```
/OpportunityItemCollection?$format=json&$filter=ProductID eq 'P300104'&$expand=Opportunity
```

#####$search

From an OData version point of view $search is **NOT** part of OData V2 specification. However C4C OData API does support $search. This is one of the 'enhacements' that has been adopted over the V2 standard. Using the OData Service Explorer it is possible to flag entity attributes as being relevant for search. If flagged, $search can be done at the entity collection level. The following example outlines the usage of the $search:

```
https://myNNNNNN.crm.ondemand.com/sap/byd/odata/cust/v1/c4codata/CustomerCollection?$search='Porter'
```

####Support for other OData/HTTP operations

C4C OData API support the following OData/HTTP operations (in addition to GET):

Operation | Description
----------|------------
POST | Used to create entity instances
PUT | Used to **completely** replace/overwrite and existing entity instance
PATCH | Used to replace/overwrite existing entity instance. The key difference between PUT and PATCH is that PUT overwrites the complete entity whereas PATCH only updates **only** attributes of the entity that are part of the payload
$batch | Used to create/update multiple entities with explicit transaction boundaries specified via Changesets as a part of the payload


  



  
  
  
  

  

  
 

 
  

  



